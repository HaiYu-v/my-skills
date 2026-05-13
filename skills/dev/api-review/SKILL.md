---
name: api-review
description: 检查 API 文档与前端界面解析的一致性，并自动修复不一致问题。当用户提到"检查接口"、"核对API"、"接口对不上"、"前后端接口一致性"、"校验接口文档"、"API review"时必须使用此 skill。涉及 @docs/api 或 @docs/prototype 目录时也应主动触发。
---

# API Review Skill

## 涉及目录
- API 文档：`@docs/api/`（后端接口定义，含路径、方法、入参、出参）
- 界面解析：`@docs/prototype/`（前端页面需求，含所需接口及字段）

---

## 执行流程

### Step 1：读取文档
1. 扫描 `@docs/prototype/` 下所有文件，提取每个页面/功能**所需的接口列表**，包括：
   - 接口路径（URL）
   - 请求方法（GET/POST 等）
   - 所需入参字段（名称、类型、是否必填）
   - 期望出参字段（名称、类型）

2. 扫描 `@docs/api/` 下所有文件，建立**接口索引**，记录每个接口的：
   - 路径、方法
   - 实际入参定义
   - 实际出参定义

### Step 2：逐项检查
对每个 prototype 中引用的接口，执行以下检查项：

| 检查项 | 说明 |
|--------|------|
| 接口存在性 | API 文档中是否存在该路径+方法的接口 |
| 入参完整性 | prototype 需要的入参字段，API 文档中是否全部存在 |
| 入参类型一致 | 字段类型是否匹配（string/number/boolean/array 等）|
| 出参完整性 | prototype 期望的出参字段，API 文档中是否全部返回 |
| 出参类型一致 | 返回字段类型是否匹配 |
| 必填项一致 | 必填/可选标记是否一致 |

### Step 3：输出检查报告

格式如下：

```
## ✅ 检查通过的接口
- POST /api/user/login
- GET /api/product/list
...

## ❌ 检查不通过的接口

### POST /api/order/create
- ❌ 入参缺失：`coupon_id`（prototype 需要，API 文档未定义）
- ❌ 出参类型不一致：`total_price` prototype 期望 `number`，API 文档定义为 `string`

### GET /api/user/info
- ❌ 接口不存在（API 文档中未找到）
```

### Step 4：修复（需用户确认后执行）

询问用户是否执行修复，确认后按以下顺序处理：

- 使用skill`api-docs`, 修复API文档
- 使用skill`front-api-create`, 修复前端API
- 使用skill`backend-api-create`, 修复后端API
- 修复完成后，**重新执行 Step 1–3** 进行二次验证，确认所有问题已解决

---

## 注意事项
- 字段名大小写视为不同（`userId` ≠ `user_id`）
- 类型兼容但不一致时（如 `int` vs `number`）也标记为警告 ⚠️
- 若文档目录不存在，立即告知用户并停止
- 同一接口被多个页面引用时，只报告一次
