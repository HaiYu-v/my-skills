---
name: py-model-create
description: 根据用户提供的字段列表，快速生成规范的 Pydantic BaseModel 类（Python）。当用户提到"生成 pydantic 类/模型"、"帮我写个 BaseModel"、"模板生成 py 类"、"生成 model 代码"、给出字段列表或数据库表结构并希望输出 Python 类时，必须使用此 skill。支持各种字段类型的默认值规范，生成带有 ConfigDict(extra="forbid") 的标准模板。
---

# Pydantic BaseModel 模板生成

## 目标

根据用户提供的字段信息，生成规范的 Pydantic v2 `BaseModel` 类，所有字段都有正确的类型注解和默认值。

---

## 生成规范

### 参考代码

```python
from pydantic import BaseModel, ConfigDict
# 按需导入：from datetime import datetime, date, timedelta, timezone

class Xxx(BaseModel):
    model_config = ConfigDict(extra="forbid")  # 禁止多余字段

    field_name: type = default_value
    ...
```

- 类名使用 **PascalCase**（大驼峰）
- 必须包含 `model_config = ConfigDict(extra="forbid")`
- 字段顺序与用户输入保持一致

---

## 字段类型 → 默认值映射表

| 字段类型 | Python 类型注解 | 默认值 | 说明 |
|---------|--------------|--------|------|
| 整数 / int | `int` | `0` | |
| 浮点 / float / double /Decimal | `int` | `0` | **用整数替代浮点数** |
| 字符串 / str | `str` | `""` | |
| 布尔 / bool | `bool` | `False` | |
| 列表 / list / array | `list` | `[]` 用 `field(default_factory=list)` | 需导入 `from pydantic import Field` |
| 字典 / dict | `dict` | `{}` 用 `field(default_factory=dict)` | 需导入 `from pydantic import Field` |
| datetime | `datetime` | `datetime(1970, 1, 1, tzinfo=timezone.utc)` | 需导入 `from datetime import datetime, timezone` |
| date | `date` | `date(1970, 1, 1)` | 需导入 `from datetime import date` |
| 自定义类 / 对象 | `Optional[ClassName]` | `None` | 需导入 `from typing import Optional` |
| 枚举 / Enum | `Optional[EnumName]` | `None` | |

> **注意**：list 和 dict 类型必须使用 `Field(default_factory=...)` 而不是直接 `= []` 或 `= {}`，避免 Pydantic 共享默认值问题。

---

## 字段类型识别规则

用户可能用中文或英文描述字段类型，按以下规则识别：

- `id`, `_id`, `count`, `num`, `level`, `lv`, `page`, `size`, `age`, `year`, `month`, `day` → `int`
- `name`, `title`, `desc`, `url`, `path`, `code`, `key`, `token`, `text`, `content` → `str`
- `price`, `rate`, `ratio`, `score`, `weight`, `amount` → `int`（浮点用整数替代）
- `tags`, `items`, `list`, `ids`, `names` → `list`
- `data`, `meta`, `info`, `extra`, `config` → `dict`
- `created_at`, `updated_at`, `deleted_at`, `_time`, `_datetime` → `datetime`
- `created_date`, `_date` → `date`
- `is_`, `has_`, `can_`, `enable`, `active`, `flag` → `bool`
- 其他引用类型 → `Optional[ClassName] = None`

---


## 注意事项

- **不要**直接写 `= []` 或 `= {}`，必须用 `Field(default_factory=...)`
- 浮点字段, 金额字段 一律用 `int` 类型**，默认值 `0`
- 导入语句按 stdlib → pydantic → 本地 的顺序排列
- 若字段类型不明确，优先推断为 `str`，并在代码注释中标注"类型待确认"
- 若用户给出的是数据库表 DDL、JSON 样例或已有代码，提取字段后同样应用上述规则