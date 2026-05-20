---
name: data-init
description: 使用 Python faker 库生成测试数据的 skill。当用户需要为数据库生成测试数据、seed 数据、mock 数据、数据填充、初始化数据，或提到 faker、造数据时，必须使用此 skill。尤其适用于有实体关系（一对多、多对多）的场景，能保证外键引用正确性。即使用户只是说"帮我生成一些测试数据"也应触发此 skill。
---

# Faker 测试数据生成器

## 约定

- 每张表生成 **100~1000 条**数据（视表的重要性决定，主表多、关联表适量）
- 数据库连接信息（host、port、账号密码）**由用户自己填写**，脚本中留占位注释
- 输出目录：`docs/init/`，每张表一个文件 `seed_{table_name}.py` + 主入口 `seed_all.py`

---

## 工作流程

### 第一步：读取项目文档

按顺序读取，**不可跳过**：

1. **实体关系图**（`docs/entity/` 目录所有文件）
   - 识别所有实体（表）及关系类型：一对一、一对多、多对多
   - 确定外键依赖顺序

2. **SQL 表结构**（`docs/sql/` 目录所有文件）
   - 记录字段名、类型、约束（NOT NULL、UNIQUE、DEFAULT）
   - 注意枚举值、长度限制、主键类型（自增 vs UUID）

### 第二步：分析依赖顺序

**被依赖的表先生成**，多对多中间表最后生成。

```
示例：users → orders → order_items
                ↑
            products
```

### 第三步：编写生成脚本

**脚本模板**：

```python
from faker import Faker
import random

fake = Faker('zh_CN')  # 国际化项目用 ['zh_CN', 'en_US']
Faker.seed(42)
random.seed(42)

TARGET_COUNT = 500  # 按表调整，100~1000
BATCH_SIZE = 500    # 批量插入大小
```

**外键处理**：先生成父表并保存 ID 列表，子表用 `random.choice()` 引用：

```python
generated_user_ids = []

def seed_users(db):
    rows = []
    for i in range(1, TARGET_COUNT + 1):
        rows.append([i, fake.name(), fake.unique.email()])
        generated_user_ids.append(i)
    db.execute("INSERT INTO users (id, name, email) VALUES (%s, %s, %s)", rows)
```

**多对多中间表**：用 `set` 去重避免唯一约束冲突：

```python
def seed_user_roles(db, user_ids, role_ids):
    pairs = set()
    rows = []
    target = min(TARGET_COUNT, len(user_ids) * len(role_ids))
    while len(pairs) < target:
        pair = (random.choice(user_ids), random.choice(role_ids))
        if pair not in pairs:
            pairs.add(pair)
            rows.append(list(pair))
    db.execute("INSERT INTO user_roles (user_id, role_id) VALUES (%s, %s)", rows)
```

**数据真实性要求**：
- 枚举字段：`random.choice(['active', 'inactive', ...])`
- 金额字段：`round(random.uniform(10, 9999), 2)`
- 时间字段：保证 `created_at <= updated_at`，范围在近 2 年内
- 状态联动字段：保证业务逻辑一致（如订单状态与支付状态匹配）
- UNIQUE 字段：使用 `fake.unique.xxx()` 或手动去重

### 第四步：生成主入口 `seed_all.py`

```python
from seed_users import seed_users
from seed_orders import seed_orders
# ... 按依赖顺序 import

from base_module import BaseMS  # 或 BaseCK

db = MS('your_db_key')  # 用户自行配置

if __name__ == '__main__':
    seed_users(db)
    seed_orders(db)
    # ...
    print("Done!")
```

### 第五步：汇报结果

生成完毕后告知用户：
- 生成了哪些文件、各表预计行数、执行顺序
- 运行方式：`python docs/init/seed_all.py`
- **列出所有无法确定取值的字段**，明确询问用户

---

## 数据库操作

### ClickHouse — `BaseCK`

```python
from base_module import BaseCK

db_list = {
    'ck_main': {
        'host': '',    # 用户填写
        'port': 9000,
        'user': '',
        'passwd': '',
        'db': '',
    },
}

class CK(BaseCK):
    def __init__(self, dbname):
        super().__init__(db_list.get(str(dbname)))
```

### MySQL — `BaseMS`

```python
from base_module import BaseMS

db_list = {
    'ms_main': {
        'host': '',    # 用户填写
        'port': 3306,
        'user': '',
        'passwd': '',
        'db': '',
        'charset': 'utf8mb4',
    },
}

class MS(BaseMS):
    def __init__(self, dbname):
        super().__init__(db_list.get(str(dbname)))
```

### 常用 API

| 方法 | 用途 | 返回值 |
|------|------|--------|
| `execute(sql, data=[])` | 写操作，`data` 为二维列表时批量执行 | - |
| `queryAll(sql, *, bind_data=[])` | 查多行 | `list[list]` |
| `queryAll_dict(sql, *, bind_data=[])` | 查多行（字段名为 key） | `list[dict]` |
| `queryColumn(sql, *, bind_data=[])` | 查单列 | `list[str]` |
| `queryRow(sql, *, bind_data=[])` | 查单行 | `tuple \| False` |
| `queryScalar(sql, *, bind_data=[])` | 查单值 | `any \| False` |

**批量写入示例**：

```python
db.execute("INSERT INTO user (name, age) VALUES (%s, %s)", [
    ["张三", 18],
    ["李四", 20],
])
```

**带参数查询示例**：

```python
rows = db.queryAll_dict("SELECT * FROM user WHERE age > %s", bind_data=[18])
```