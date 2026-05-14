---
name: feature-update
description: 当用户指定使用这个skill的时候才使用
---

## 相关目录
- 相关实体 `@docs/entity`
- api文档 `@docs/api`
- 建表sql `@docs/sql`
- 前端接口 `**/src/api`
- 前端实体 `**/src/type`
- 后端接口 `**/controller`
- 后端实体 `**/model`

## 处理流程
1. 根据用户的要求进行处理, 处理完成后执行后面的步骤
2. 判断是否需要修改api文档, 使用skill `api-doc`
3. 判断是否需要修改前端接口, 使用skill `front-api-create`
4. 判断是否需要修改后端接口, 使用skill `backend-api-create`
5. 判断是否需要修改实体, 使用skill `entity-create`
6. 判断是否需要修改建表语句, 请告知用户, 让用户重新建表

