---
name: api-docs
description: 当前后端 API 接口设计、OpenAPI/Swagger 文档生成时使用。
---

# 核心目标
- OpenAPI 3.0 YAML文档生成 生成到 `@docs/api`
- 参考相关实体的信息 `@docs/entity`
- 参考相关的实体的建表sql语句 `@docs/sql`


# 输出原则
## 必须输出内容（按顺序）
---

## 1. 接口分析
包含：
- 接口用途
- 资源模型（Resource）
- 核心实体字段
- 请求方式选择原因
- 权限建议（可选）

---

## 2. RESTful API 设计
规范：
### 查询列表
GET /resources

### 查询详情
GET /resources/{id}

### 新增
POST /resources

### 更新
PUT /resources/{id}

### 局部更新（可选）
PATCH /resources/{id}

### 删除
DELETE /resources/{id}

### 批量操作（如需要）
POST /resources/batch-delete

---

## 3. OpenAPI 3.0 YAML
必须包含：
- openapi
- info
- servers
- tags
- paths
- parameters
- requestBody
- responses
- schemas
- security（如涉及鉴权）

要求：
- 可直接用于 Swagger / Apifox / Postman 导入
- schema 字段完整
- 示例值清晰

---


# 分页规范
统一参数：
- page
- page_size
- keyword
- order_by

统一返回：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "list": [],
    "total": 0,
    "page": 1,
    "pageSize": 10
  }
}
````

---

# 返回结构规范

## 成功

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

## 失败

```json
{
  "code": 40001,
  "message": "参数错误",
  "data": null
}
```

---

# 状态码规范

* 0 成功
* 40000 通用业务失败
* 40001 参数错误
* 40100 未授权
* 40300 无权限
* 40400 资源不存在
* 50000 服务端错误

---

# 命名规范

## URL

* 使用复数资源名词
* 使用 kebab-case
  示例：
* /users
* /user-orders


## 方法名

* get
* list
* create
* update
* patch
* delete

---

# 接口设计原则

* 查询用 GET
* 新增用 POST
* 删除用 DELETE
---







