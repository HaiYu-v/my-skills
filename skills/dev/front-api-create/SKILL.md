---
name: front-api-create
description: 生成前端接口代码时必须使用此 skill。触发场景包括：新增 API 接口、接口重构、前端 api/request 文件创建。
---

## 我的要求
- 依据API文档`@docs/api`
- 生成前端api接口和对应的req类
 - 不需要resp类, 直接在对应的实体里加字段就行
 - 字段使用`?`表示可选

> 如果找不到 `@docs/api`，询问用户提供接口说明，不要自行假设字段。

---

## 前端生成规范（TypeScript）

### 目录结构

```
src/
├── api/
│   ├── request.ts        ← 已有封装，不新建
│   └── {entity}Api.ts    ← 本 skill 生成
└── types/
    └── {entity}.ts       ← 本 skill 生成
```

> ⚠️ `request.ts` 必须已存在才能生成 api 文件。若不存在，告知用户并停止，不自行创建。

### types/{entity}.ts 模板

```typescript
// src/api/user.ts
import request from '@/utils/request'

export function searchUserApi(data: {
    search: string
    platform_id: number
    region_id: number
}) {
    return request({
        url: '/backend/creator-analysis/search-user',
        method: 'post',
        data
    })
}
```

### 字段规范

- 时间字段：统一 `yyyy-MM-dd HH:mm:ss` ，前后端保持一致
- 命名风格：前端 camelCase，后端按语言惯例（Java/PHP: camelCase，Python: snake_case）
- null vs 空数组：列表字段无数据返回 `[]`，单对象不存在返回 `null`
- 接口版本：路径统一前缀 `/api/v1/`


## 输出要求
- 必须输出完整目录结构
- 代码可直接复制使用
- 仅生成骨架，不实现业务逻辑
- 注释完整，说明每个方法用途
- 严格遵循用户项目已有的命名风格
