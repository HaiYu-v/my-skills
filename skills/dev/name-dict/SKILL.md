---
name: name-dict
description: 当需要为变量名、数据库字段、接口参数、DTO属性、文件名、组件名、HTML标签ID/Class、常量、枚举或业务字段进行标准化命名时使用。适用于统一项目命名规范、避免语义混乱、生成可维护的实体属性名、建立团队命名词典、规范前后端字段映射等场景。核心目标是基于“前缀 + 词根 + 后缀”的结构化规则，将业务语义拆解为场景修饰（前缀）、核心对象（词根）、字段性质（后缀），确保命名具备可读性、可扩展性、一致性与可搜索性。使用时需优先查询和维护 docs/naming.md 中的命名字典，避免重复造词、缩写歧义和跨模块命名冲突，保证同一业务概念在数据库、后端、前端、接口文档中的命名统一。
---

## 我的要求
- 创建一个实体属性命名的参考字典, 在`docs/naming.md`中维护
- 只维护前缀, 词根 和后缀表

## 命名结构
```txt
[前缀] + [词根] + [后缀]
```
词根是必要的,前缀和后缀是可选的

示例
- user_id
- live_user_cnt
- pre_order_total_amt
- video_play_avg_duration


## 命名词典维护（docs/naming.md）参考

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

| 后缀      | 含义      | 示例        |
| ------- | ------- | ------------   |
| _id     | 主键/关联ID | user_id     |
| _no     | 编号      | order_no     |
| _cnt    | 数量      | order_cnt    |
| _inc    | 增量      | fans_inc     |
| _total  | 总量      | sales_total  |
| _avg    | 平均值    | stay_avg     |
| _amt    | 金额      | order_amt    |
| _rate   | 比率      | refund_rate  |
| _pct    | 百分比    | profit_pct   |
| _at     | 时间      | created_at   |
| _date   | 日期      | stat_date    |
| _flag   | 标记      | enable_flag  |
| _status | 状态      | order_status |
| _type   | 类型      | source_type  |
| _json   | JSON字段  | enable_flag  |


