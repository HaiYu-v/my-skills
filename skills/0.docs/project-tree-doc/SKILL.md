---
name: project-tree-doc
description: 为项目生成可视化的树结构文档，支持扫描真实目录或根据用户描述手动构建。当用户想要展示、记录或分享项目目录结构时使用。触发词包括：项目结构、目录树、tree文档、文件结构、项目文档树、generate tree、project structure、文件树、模块结构图。即使用户只是上传了文件列表或描述了目录布局，也应主动触发此skill来生成美观的树形文档。
---

# Project Tree Doc Skill

为项目生成带注释的可视化目录树文档，支持 emoji 图标、模块分组标题和中文注释。

## 两种使用模式

### 模式 A：扫描真实目录（推荐）

用户提供了实际的项目路径时，用脚本自动扫描。

```bash
python /home/claude/project-tree-doc/scripts/scan_tree.py \
  --root /path/to/project \
  --output /mnt/user-data/outputs/project_tree.md \
  [--ignore node_modules,__pycache__,.git,dist,build] \
  [--max-depth 5]
```

扫描完成后，在生成的 Markdown 基础上**补充注释**（见下方注释规范）。

### 模式 B：手动构建（用户粘贴结构或口头描述）

用户粘贴了 `tree` 命令输出、文件列表，或直接描述了目录结构时，直接生成带格式和注释的 Markdown。

---

## 输出格式规范

### 1. 文件头

```markdown
# 项目名称 - 目录结构

> 简短的项目描述（一句话）

**生成时间**：YYYY-MM-DD  
**根目录**：`/path/to/project/`
```

### 2. 树结构主体

使用标准树形符号：`├──` `│` `└──` `    `（4空格缩进）

**分组标题**（模块/层级分隔）：

```
│
├── 🎯 主执行脚本
├── file1.py           # 注释
```

**emoji 图标选用参考**：

| 图标 | 含义 |
|------|------|
| 🎯   | 主入口 / 核心脚本 |
| 📂   | 重要子目录 |
| 🗄️   | 数据库 / 存储 |
| 🔧   | 工具类 / 配置 |
| 📦   | 模型 / 数据结构 |
| 🚀   | 任务 / 调度 |
| 🧪   | 测试 |
| 📝   | 文档 |
| 🌐   | API / 网络 |

### 3. 注释规范

- 每个文件/目录的注释跟在 `#` 后，对齐（用空格填充）
- 注释要简洁：**说明职责，而不是重复文件名**
- `__init__.py` 统一注释为 `# 模块初始化文件`
- 目录本身：在目录行末或子树上方的分组标题中说明

### 4. 文件尾（可选）

```markdown
---

## 快速导航

- [模块A](#模块a)
- [模块B](#模块b)
```

---

## 生成步骤

1. **确认信息**：项目名、根路径或结构内容、是否有特殊模块需要重点标注
2. **扫描或解析**：运行脚本 / 解析用户提供的结构
3. **识别模块边界**：找出主要功能分组，插入分组标题行
4. **补充注释**：根据文件名和上下文推断每个文件的职责
5. **输出 Markdown**：保存到 `/mnt/user-data/outputs/<project>_tree.md`
6. **呈现给用户**：调用 `present_files`

---

## 示例输出片段

````markdown
# kol_analysis - 目录结构

> TikTok KOL 数据分析平台：爬虫调度、数据固化、图片存储一体化管道

**生成时间**：2025-06-12  
**根目录**：`kol_analysis/dev/`

```
kol_analysis/dev/
├── __init__.py            # 模块初始化文件
│
├── 🎯 主执行脚本
├── dispatch.py            # 发布爬虫任务（达人、视频、TikTok Shop）
├── solidify.py            # 固化原始爬虫数据到分析表
├── schedule.py            # APScheduler 定时任务调度器（主入口）
├── quality.py             # 数据质检脚本，异常时发送企微告警
├── save_img.py            # 批量保存图片并上传到 COS
├── test.py                # 临时测试与数据迁移脚本
│
├── 📂 db/                 # 数据库连接层
│   ├── __init__.py
│   ├── ck.py              # ClickHouse 连接配置
│   └── ms.py              # MySQL 连接配置
│
├── 📂 model/              # 数据模型层
│   ├── __init__.py
│   ├── creator.py         # 达人数据模型
│   └── tkshop/            # TikTok Shop 相关模型
│       └── tkshop_creator_task.py
│
└── 📂 util/               # 工具类
    └── url_util.py        # URL 有效期判断工具
```
````

---

## 常见问题处理

**目录层级很深**：默认展示到第 4 层，更深的目录折叠并标注 `# ... (N files)`

**文件很多**：同类文件可合并展示，如 `model_*.py (8 files)  # 各实体数据模型`

**用户没提供注释**：根据文件名和所在目录推断，主动生成合理注释；不确定时标注 `# TODO: 待补充`

**用户只想要纯文本树（不要 Markdown）**：直接输出 plain text，不加代码块包裹
