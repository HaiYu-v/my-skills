---
name: analysis-db
description: 读取项目代码，分析数据库各表的使用情况，输出结构化的表状态报告。当用户想了解数据库中哪些表在用、哪些废弃、每张表关联哪些文件/界面/项目时使用。触发词：数据库使用情况、表分析、表状态、db audit、哪些表在用、数据库梳理。
---

# DB Schema Audit

分析项目代码，产出每个数据库/每张表的状态报告。

---

## 输出格式（每张表）

| 字段 | 说明 | 取值 |
|------|------|------|
| 表名 | 原始表名 | — |
| 介绍 | ddl的comment后的内容 | — |
| 状态 | 使用 / 弃用 / 不清楚 | 判断依据见下方 |
| 备注 | 建表注释或推断用途 | — |
| 主要阶段 | 可多选 | 底层表 / 业务表 / 爬虫结果表 / 中间临时表 |
| 涉及主要文件 | 最相关的 1 个文件路径 | — |
| 涉及主要界面 | 最相关的 1 个页面/路由 | — |
| 涉及主要项目 | 最相关的 1 个子项目/模块 | — |

---

## 分析步骤

### 1. 收集表清单

使用下面的sql, 获取某个库下的所有表的name和comment

```bash
SELECT
    TABLE_NAME,
    TABLE_COMMENT
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'tiktok_media'
ORDER BY TABLE_NAME;
```

### 2. 判断表状态

- **使用**：近期代码中有 SELECT/INSERT/UPDATE/DELETE，或 ORM 模型被 Service 引用
- **弃用**：仅有建表 SQL，无任何业务代码引用；或文件名含 `old`/`bak`/`deprecated`
- **不清楚**：有模型定义但引用极少，或仅在注释中提及

```bash
# 搜索表名在代码中的引用（替换 TABLE_NAME）
grep -rn "TABLE_NAME" --include="*.java" --include="*.php" --include="*.py" --include="*.vue" --include="*.xml" . | grep -v "\.sql:" | wc -l
```

### 3. 推断主要阶段

| 阶段 | 判断特征 |
|------|----------|
| 底层表 | 存储原始数据，被多处读取，几乎不被写入业务逻辑 |
| 业务表 | 有对应的 Service/Controller CRUD，关联前端界面 |
| 爬虫结果表 | 表名含 `raw`/`spider`/`crawl`/`tiktok`/`creator`，由 Python 脚本写入 |
| 中间临时表 | 表名含 `tmp`/`temp`/`mid`，用于 ETL 中转 |

### 4. 定位关联文件/界面/项目

```bash
# 找引用最多的文件
grep -rln "TABLE_NAME" --include="*.java" --include="*.php" --include="*.py" . | head -5

# 找前端路由/页面
grep -rn "TABLE_NAME\|api_endpoint" --include="*.vue" --include="*.ts" src/ | head -5
```

- **涉及主要文件**：引用次数最多的那个文件（Service/Mapper/Model 优先）
- **涉及主要界面**：最相关的 Vue 页面或路由路径
- **涉及主要项目**：所属子模块（如 `kol_outreach`、`collab_lab_script`、`admin`）

---

## 输出示例

```
## 数据库: kol_outreach

| 表名 | 备注 | 状态 | 主要阶段 | 主要文件 | 主要界面 | 主要项目 |
|------|------|------|----------|----------|----------|----------|
| campaign | 推广活动 | 使用 | 业务表 | CampaignService.java | /campaign/list | kol_outreach |
| campaign_creator | 活动-创作者关联 | 使用 | 业务表 | CampaignCreatorMapper.xml | /campaign/detail | kol_outreach |
| tiktok_media_raw | TikTok 原始媒体数据 | 使用 | 爬虫结果表 | solidify_daily.py | — | collab_lab_script |
| tmp_creator_mid | 创作者中间处理表 | 不清楚 | 中间临时表 | soli_creator.py | — | collab_lab_script |
| message_old | 旧消息表 | 弃用 | — | — | — | — |
```

---

## 注意事项

- 如果数据库较多（>3个），先列出库名让用户确认分析范围
- ClickHouse 表重点看 Python 脚本的 `INSERT INTO` 和 `CREATE TABLE`
- 表名模糊时，备注填推断用途并加 `(推断)` 标注
- 最终以 Markdown 表格输出，便于复制到文档