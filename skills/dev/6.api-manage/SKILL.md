---
name: api-manage
description: 当前后端接口代码生成、请求封装、Controller骨架创建等场景时使用。适用于新增接口、接口重构、前端 api/request 文件创建、后端 controller/request/response 定义、字段规范统一、错误码设计等。
---

# 核心目标
- 依据api文档 `@docs/api`生成前后端接口
- 前端生成`api/{实体}Api.ts` 文件
- 后端生成`controller/{实体}Controller` 文件
- 前端使用封装好的`request.ts`实现请求接口,如果没有此文件, 请告知用户而不是新建
- 仅定义方法的入参和返回类型,不需要实现具体逻辑



# 输入识别
当用户提供以下任一信息时触发：
- 功能描述（如“用户管理接口”）
- 数据表结构（SQL / 字段）
- 页面原型
- 旧接口
- 接口报文
- Swagger 文档
- 前端页面需求

---

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

## 4. 前端目录结构
示例：
src/
├── api/
│   └── user.ts
├── types/
│   └── user.ts
└── utils/
    └── request.ts

---

## 5. 前端接口代码
要求：
- 基于 request.ts
- TS 类型完整
- Query / Body 类型分离
- 分页结构统一
- 命名语义化
- 支持 CRUD

标准命名：
- getUserList
- getUserDetail
- createUser
- updateUser
- deleteUser

---

## 6. 后端目录结构
### Java Spring Boot
src/main/java/.../
├── controller/
├── service/impl/
├── dto/request/
├── dto/response/
├── entity/
└── mapper/

### PHP Yii2 / Laravel
├── controllers/
├── dto/
├── models/
└── validators/

### Node NestJS
├── controller/
├── dto/
└── entity/

---

## 7. 后端接口骨架
要求：
- 仅生成结构
- 不实现业务逻辑
- 包含路由注解
- 包含参数校验
- 包含 Request DTO
- 包含 Response DTO / VO
- 包含统一返回结构
- 注释完整

---

# DTO 规范
## Request DTO
用于：
- create
- update
- query

要求：
- 字段类型
- 必填项
- 默认值
- 校验规则（长度/枚举/格式）

## Response DTO / VO
要求：
- 返回前端所需字段
- 避免暴露内部字段
- 时间字段格式统一

---

# 分页规范
统一参数：
- page
- pageSize
- keyword
- sortBy
- order

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


---

# 联调规范

* 字段名统一
* 枚举值统一
* 时间格式统一（ISO8601 / yyyy-MM-dd HH:mm:ss）
* null 与空数组区分明确
* 分页结构固定
* 错误码固定
* 接口版本建议（/api/v1）

---

# 可选增强

* JWT / Token 鉴权结构
* 文件上传接口
* Excel 导入导出接口
* 批量接口
* Webhook 回调接口
* 幂等设计
* 接口限流

---

# 输出风格要求

* 结构化
* 可直接开发
* 目录清晰
* 代码可复制
* 遵循用户项目技术栈
* 优先标准化，而非临时实现



