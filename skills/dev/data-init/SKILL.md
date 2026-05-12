---
name: data-init
description: 使用 Python faker 库生成测试数据的 skill。当用户需要为数据库生成测试/假数据、初始化数据、seed 数据，或提到 faker、测试数据、mock 数据、数据填充时，必须使用此 skill。尤其适用于有实体关系（一对多、多对多）的场景，需要保证外键引用正确性。
---

# Faker 测试数据生成器

## 工作流程

### 第一步：读取项目文档

按以下顺序读取文档，**不要跳过**：

1. **读取实体关系图** (`@docs/entity` 目录下所有文件)
   - 识别所有实体（表）
   - 梳理关系类型：一对一、一对多、多对多
   - 确定外键依赖顺序（哪些表必须先生成）

2. **读取 SQL 表结构** (`@docs/sql` 目录下所有文件)
   - 记录每张表的字段名、类型、约束（NOT NULL、UNIQUE、DEFAULT 等）
   - 记录枚举值、长度限制
   - 注意自增主键 vs UUID 主键

### 第二步：分析依赖顺序

构建生成顺序，原则：**被依赖的表先生成**

```
示例依赖链：
users → orders → order_items
         ↑
      products
```

多对多中间表最后生成，依赖两端表都生成完毕。

### 第三步：编写生成脚本

**输出目录**：`docs/init/`

**文件命名规范**：
- 每张表一个文件：`seed_{table_name}.py`
- 主入口文件：`seed_all.py`（按依赖顺序调用各脚本）

**代码规范**：

```python
from faker import Faker
import random
import json
from datetime import datetime, timedelta

fake = Faker('zh_CN')  # 根据项目语言选择，国际化项目用 ['zh_CN', 'en_US']
Faker.seed(42)         # 固定随机种子，保证可重复性
random.seed(42)

BATCH_SIZE = 1000      # 批量插入大小，避免内存溢出
TARGET_COUNT = 10000   # 每表目标行数
```

**外键处理策略**：
- 先生成父表数据，将生成的 ID 列表保存到变量/文件
- 子表生成时从父表 ID 列表中 `random.choice()` 取值
- 多对多中间表：从两端各取 ID，注意去重避免唯一约束冲突

```python
# 示例：保存已生成的 ID 供子表使用
generated_user_ids = []

def seed_users():
    users = []
    for i in range(1, TARGET_COUNT + 1):
        users.append({
            'id': i,
            'name': fake.name(),
            'email': fake.unique.email(),
            ...
        })
        generated_user_ids.append(i)
    return users
```

**数据真实性要求**：
- 枚举字段：使用 `random.choice([...])` 从实际枚举值中选取
- 金额字段：`round(random.uniform(min, max), 2)`
- 时间字段：保证 `created_at <= updated_at`，时间范围合理（近 2 年内）
- 状态流转字段：保证逻辑一致（如订单状态与支付状态匹配）

**多对多处理**：

```python
# 示例：user_roles 中间表，避免重复组合
def seed_user_roles(user_ids, role_ids):
    pairs = set()
    records = []
    target = min(TARGET_COUNT, len(user_ids) * len(role_ids))
    
    while len(pairs) < target:
        pair = (random.choice(user_ids), random.choice(role_ids))
        if pair not in pairs:
            pairs.add(pair)
            records.append({'user_id': pair[0], 'role_id': pair[1]})
    return records
```

### 第四步：生成主入口文件

`docs/init/seed_all.py` 需要：
1. 按依赖顺序调用各 seed 函数
2. 支持两种输出模式（在文件顶部用常量控制）：
   - **SQL 模式**：生成 `.sql` 文件，适合直接导入数据库
   - **Python 直连模式**：使用数据库驱动直接插入

```python
OUTPUT_MODE = 'sql'  # 'sql' 或 'db'
DB_CONFIG = {        # OUTPUT_MODE='db' 时使用
    'host': 'localhost',
    'database': 'your_db',
    ...
}
```

### 第五步：输出说明

生成完毕后，向用户汇报：
- 生成了哪些文件
- 各表预计行数
- 执行顺序
- 如何运行：`python docs/init/seed_all.py`
- 如有特殊字段无法确定取值，明确列出并询问

## 注意事项

- **不要**在脚本里硬编码数据库连接密码，用环境变量或提示用户填写
- 如果字段含义不明确，优先从字段名+类型推断，实在无法判断时才询问用户
- UNIQUE 字段使用 `fake.unique.xxx()` 或手动保证唯一性
- 自增主键不需要手动生成（SQL 模式除外，SQL 中需要显式写入以维持外键引用）


## 数据库操作
- clickhouse 使用 `from base_module import BaseCK`
- mysql 使用 `from base_module import BaseMS`

### BaseCK
``` py
from base_module import BaseCK
db_list = {
    'ck_21': {
        'host': ip,
        'port': 端口, 
        'user': 账号,
        'passwd': 密码,
        'db': 库名,
    },
}
class CK(BaseCK):
    def __init__(self, dbname):
        config = db_list.get(str(dbname))
        super().__init__(config)
```

### BaseMS
``` py
from base_module import BaseMS

db_list = {
    # MySQL ------------------------
    '11': {
        'host': ip,
        'port': 端口,
        'user': 账号,
        'passwd': 密码,
        'db': 库名,
        'charset': 'utf8mb4'
    }, 
}
class MS(BaseMS):
    def __init__(self, dbname):
        config = db_list.get(str(dbname))
        super().__init__(config)
```