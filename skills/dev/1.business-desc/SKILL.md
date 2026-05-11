---
name: business-desc
description: 当用户需要进行业务实体抽象、领域模型设计、ER 实体关系梳理、数据库实体文档编写、属性命名规范制定、业务对象标准化、领域驱动设计（DDD）基础建模时使用。适用于新项目建模、原型转实体、业务分析、数据库设计前置、接口 DTO 实体统一、跨团队命名规范建设等场景。
---

# 核心目标
建立统一、可维护、可扩展的业务实体文档体系，确保：
- 实体定义清晰
- 属性语义统一
- 命名规则标准化
- 实体关系明确
- 前后端/数据库/API 使用一致
- 支持后续建表、接口设计、代码生成


# 一、文档目录规范

## 实体文档目录
- 所有实体文档统一存放于：`docs/entity/`
- 一个实体一个 Markdown 文件
- 文件命名规则：
  - `实体名.md`
  - 使用业务英文名，采用 PascalCase 或 UpperCamelCase（推荐）
  - 示例：
    - `User.md`
    - `Order.md`
    - `Product.md`
    - `LiveRoom.md`

## 公共规范文档
- `docs/naming.md`：属性命名规范（前缀 / 词根 / 后缀）
- `docs/entity/index.md`：实体总目录（实体清单 + 关系总览）
- `docs/entity/enum.md`：枚举值统一定义


# 二、单个实体文档标准结构（强制）

```md
# 实体名称（中文 + 英文）

## 1. 实体定义
- 实体名称：
- 英文名称：
- 核心作用：
- 所属业务域：
- 实体说明：
- 是否核心实体：
- 生命周期：

## 2. 业务场景
- 创建场景：
- 修改场景：
- 删除场景：
- 查询场景：
- 状态流转：

## 3. 属性列表
| 属性名 | 中文名 | 类型 | 必填 | 默认值 | 示例 | 说明 |
|--------|--------|------|------|--------|------|------|

## 4. 核心主键
- 主键：
- 唯一键：
- 业务唯一键：
- 外键：

## 5. 实体关系
| 关系类型 | 目标实体 | 关系说明 |
|----------|----------|----------|
| 1:1      |          |          |
| 1:N      |          |          |
| N:N      |          |          |

## 6. 状态字段
| 状态字段 | 状态值 | 含义 |


## 8. 安全规则
- 脱敏字段：
- 禁止更新字段：
- 审计字段：


## 10. 数据库映射建议
- 表名：
- 索引建议：
- 分区建议：
````

# 三、实体设计原则

## 必须包含
### mysql
* id（主键）
* created_at（创建时间）
* updated_at（更新时间）

### clickhouse
* created_at（创建时间）



# 四、实体关系设计规范

## 关系分类

* One-to-One（1:1）
* One-to-Many（1:N）
* Many-to-Many（N:N）
* 聚合关系（Aggregation）
* 组合关系（Composition）

## 要求

* 必须标注外键字段
* 必须说明依赖方向
* 必须说明删除策略：
  * CASCADE
  * SET NULL
  * RESTRICT
* 必须说明业务归属

# 五、实体属性命名规范（核心）

## 基础规范

* 全部使用：`snake_case`命名
* 禁止拼音
* 禁止模糊命名：
  * ❌ data
  * ❌ info
  * ❌ value
  * ❌ temp
* 必须语义明确：
  * ✅ user_id
  * ✅ order_total_amt

## 命名结构
```txt
[前缀] + [词根] + [后缀]
```
## 示例

* user_id
* live_user_cnt
* pre_order_total_amt
* video_play_avg_duration

# 六、命名词典维护（docs/naming.md）

## 1. 前缀表（修饰业务场景）

| 前缀     | 含义 | 示例             |
| ------ | -- | -------------- |
| pre_   | 前置 | pre_order_amt  |
| post_  | 后置 | post_sale_cnt  |
| live_  | 直播 | live_user_cnt  |
| video_ | 视频 | video_play_cnt |
| temp_  | 临时 | temp_file_path |
| ext_   | 扩展 | ext_info_json  |

## 2. 词根表（核心业务对象）

| 词根      | 含义   |
| ------- | ---- |
| user    | 用户   |
| order   | 订单   |
| product | 产品   |
| sku     | 库存单元 |
| live    | 直播   |
| video   | 视频   |
| media   | 媒体   |
| brand   | 品牌   |

## 3. 后缀表（字段性质）

| 后缀      | 含义      | 示例           |
| ------- | ------- | ------------ |
| _id     | 主键/关联ID | user_id      |
| _no     | 编号      | order_no     |
| _cnt    | 数量      | order_cnt    |
| _inc    | 增量      | fans_inc     |
| _total  | 总量      | sales_total  |
| _avg    | 平均值     | stay_avg     |
| _amt    | 金额      | order_amt    |
| _rate   | 比率      | refund_rate  |
| _pct    | 百分比     | profit_pct   |
| _at     | 时间      | created_at   |
| _date   | 日期      | stat_date    |
| _flag   | 标记      | enable_flag  |
| _status | 状态      | order_status |
| _type   | 类型      | source_type  |

## 4. 保留规则

* JSON字段：`*_json`
* 枚举字段：`*_type`
* 状态字段：`*_status`
* 时间字段：
  * 时间点：`*_at`
  * 日期：`*_date`


# 七、字段分类标准

## 标准字段层级

* 基础字段（id/name/type/status）
* 业务字段（订单、用户、产品）
* 统计字段（cnt/avg/total）
* 审计字段（created/updated）
* 扩展字段（ext/json）

# 八、禁止事项

* 禁止同义字段并存：

  * ❌ user_id / uid
* 禁止无单位金额：

  * ❌ price
  * ✅ price_amt
* 禁止时间歧义：

  * ❌ time
  * ✅ created_at
* 禁止布尔模糊：

  * ❌ enable
  * ✅ is_enabled

# 九、交付物

输出必须包含：

* 实体文档（docs/entity/*.md）
* naming.md
* enum.md
* er.md
* index.md
* change-log.md

# 十、最终目标

通过该规范可直接支撑：

* 原型分析
* 数据库建模
* 建表 SQL
* OpenAPI DTO
* 前端 TypeScript Interface
* 后端 Entity / VO / DTO
* 数据仓库指标字段统一

