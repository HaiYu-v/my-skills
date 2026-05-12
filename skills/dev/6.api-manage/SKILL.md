---
name: api-manage
description: 当前后端接口代码生成、请求封装、Controller骨架创建等场景时使用。适用于新增接口、接口重构、前端 api/request 文件创建、后端 controller/request/response 定义、字段规范统一、错误码设计等。
---

# 核心目标
- 依据api文档 `@docs/api`生成前后端接口
- 前端生成`api/{实体}Api.ts` 文件和`types/{实体}.ts` 文件
- 后端生成`controller/{实体}Controller` 文件和`model/{实体}/{实体}Dto`文件
- 前端使用封装好的`request.ts`实现请求接口,如果没有此文件, 请告知用户而不是新建
- 仅定义方法的入参和返回类型,不需要实现具体逻辑



## 4. 前端目录结构
示例：
```
src/
├── api/
|   ├── request.ts
│   └── user.ts
└── types/
    └── user.ts
```

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
├── model/dto/{实体}/
└── model/entity/

---
## 7. 后端接口骨架
要求：
- 仅生成结构
- 不实现业务逻辑
- 包含路由注解
- 包含参数校验
- 包含 Request DTO
- 包含 Response DTO
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

## Response DTO 
要求：
- 返回前端所需字段
- 避免暴露内部字段
- 时间字段格式统一


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
  "code": 1000,
  "message": "参数错误",
  "data": null
}
```



# 联调规范

* 字段名统一
* 枚举值统一
* 时间格式统一（ISO8601 / yyyy-MM-dd HH:mm:ss）
* null 与空数组区分明确
* 分页结构固定
* 错误码固定
* 接口版本建议（/api/v1）


# 输出风格要求

* 结构化
* 可直接开发
* 目录清晰
* 代码可复制
* 遵循用户项目技术栈
* 优先标准化，而非临时实现



