---
name: name-dict
description: 提供一个前缀,词根, 后缀的字典,用于全局实体属性命名的规范。当提到 创建实体规范, 实体属性定义规范时使用
---

## 我的要求
- 创建一个实体属性命名的参考字典, 在`docs/naming.md`中维护
- 只维护前缀, 词根 和后缀三个表格, 不要出现其它多余的内容和描述

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


>注意: 给出的前缀,词根和后缀表是提供参考, 并非必须, 具体请根据业务场景和需求进行定义
