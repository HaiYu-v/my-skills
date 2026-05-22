---
name: ck-ddl-create
description: |
  为后端开发和数据库设计人员生成MySQL建表 DDL SQL 语句。当用户需要建表、设计表结构、生成 CREATE TABLE 语句，或描述业务实体要求输出 SQL 时，必须使用此 skill。即使用户只说"帮我建个表"、"设计一下这个表结构"、"写个建表语句"也要触发此 skill。
---

## 我的要求
- 如果无法得知数据库类型，请先询问用户

## 输出规范

### 通用规则
- 所有表必须添加与业务场景匹配、与表名含义一致的**中文表备注**
- 每个字段必须添加与字段含义匹配、与字段名对应准确的**中文字段备注**
- 根据业务合理性添加主键、非空、唯一、默认值等约束，无需额外说明
- 优先选择符合业务场景的常见字段类型，避免生僻或兼容性差的类型
- 枚举值字段在备注中说明取值含义，如：`0-否，1-是`


---

## ClickHouse 建表规范

### 类型选择
| 场景 | 推荐类型 |
|------|---------|
| 主键/业务ID（字符串） | `String` |
| 主键/业务ID（数值） | `UInt64` |
| 小整数标志位（0/1） | `UInt8` |
| 普通整数 | `UInt32` / `Int32` |
| 大整数/金额（分） | `UInt64` / `Int64` |
| 浮点 | `Float64` |
| 时间 | `DateTime` |
| 可空字段 | `Nullable(Type)`，如 `Nullable(String)` |

### ClickHouse 注意事项
- ClickHouse **不支持** `NOT NULL` 关键字，非 Nullable 字段默认即为非空，不要写 `NOT NULL`
- 可空字段使用 `Nullable(Type)` 声明，并可设 `DEFAULT NULL`
- 非空字段使用 `DEFAULT 默认值` 而非 `NOT NULL`
- 业务实体表必须有 `create_time` 
  - `create_time` 加 `DEFAULT now()`
- 必须指定 `ENGINE`，分析场景优先使用 `ReplacingMergeTree`
- `PARTITION BY` 选低基数字段（如市场ID、日期月份）
- `ORDER BY` 即主键，选择查询最频繁的过滤/聚合字段组合

### ClickHouse 示例
```sql
-- 创建店铺信息表
CREATE TABLE `shop` (
    `shop_id`        String          DEFAULT ''    COMMENT '店铺ID',
    `unique_key`     String          DEFAULT ''    COMMENT '唯一键',
    `market_id`      UInt32          DEFAULT 0     COMMENT '所属站点ID',
    `name`           String          DEFAULT ''    COMMENT '店铺名称',
    `place`          Nullable(String) DEFAULT NULL  COMMENT '店铺地址',
    `is_official`    UInt8           DEFAULT 0     COMMENT '是否官方店：0-否，1-是',
    `url`            Nullable(String) DEFAULT NULL  COMMENT '店铺链接',
    `sold_total`     UInt64          DEFAULT 0     COMMENT '总销量',
    `gmv_total`      UInt64          DEFAULT 0     COMMENT '总销售额（分）',
    `created_at`     DateTime        DEFAULT now() COMMENT '创建时间'
)
ENGINE = ReplacingMergeTree(created_at)
PARTITION BY (market_id)
ORDER BY (is_official, shop_id)
SETTINGS index_granularity = 4096
COMMENT '店铺信息表';
```

> 注意: 1.clickhouse 不需要update_time 2.没有提到软删除,就不要加dr字段
---

