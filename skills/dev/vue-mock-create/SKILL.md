---
name: vue-mock-create
description: 在 Vue3 + Vite 项目中使用 vite-plugin-mock 和 mockjs 搭建 Mock 数据服务。当用户提到"mock数据"、"接口mock"、"vite mock"、"假数据"、"本地接口模拟"、"前端联调"、"接口还没好"等场景时触发本技能。覆盖从安装配置到编写 mock 文件、使用 mockjs 生成随机数据、按环境控制 mock 开关、以及常见问题排查的完整流程。
---

## 我的要求
- 使用`vite-plugin-mock` + `mockjs`
- 接口依据`src/api`
- 实体关系依据 `docs/entity`
- 实体表结构依据 `docs/sql`






## 一、安装

```bash
npm install vite-plugin-mock mockjs -D
npm install @types/mockjs -D  # TypeScript 项目
```

---

## 二、vite.config.ts 配置

### 基础配置

```ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { viteMockServe } from 'vite-plugin-mock'

export default defineConfig({
  plugins: [
    vue(),
    viteMockServe({
      mockPath: 'mock',       // mock 文件所在目录，相对项目根目录
      enable: true,           // 是否启用
    }),
  ],
})
```

### 按环境控制（推荐）

```ts
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { viteMockServe } from 'vite-plugin-mock'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd())
  return {
    plugins: [
      vue(),
      viteMockServe({
        mockPath: 'mock',
        enable: env.VITE_USE_MOCK === 'true',
      }),
    ],
  }
})
```

`.env.development`：
```
VITE_USE_MOCK=true
```

`.env.production`：
```
VITE_USE_MOCK=false
```

### 常用配置项说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `mockPath` | string | `'mock'` | mock 文件目录 |
| `enable` | boolean | `true` | 是否启用 |
| `watchFiles` | boolean | `true` | 是否监听文件变化热更新 |
| `logger` | boolean | `true` | 控制台打印请求日志 |

---

## 三、编写 Mock 文件

Mock 文件放在 `mock/` 目录下，每个文件导出一个 `MockMethod[]` 数组。

### 基础结构

```ts
// mock/user.ts
import type { MockMethod } from 'vite-plugin-mock'

export default [
  {
    url: '/api/user/info',      // 拦截的请求路径
    method: 'get',              // 请求方法：get | post | put | delete | patch
    timeout: 200,               // 模拟延迟（ms），不写则无延迟
    response: ({ query, body, headers }) => {
      return {
        code: 200,
        message: 'ok',
        data: { id: 1, name: '张三', role: 'admin' },
      }
    },
  },
] as MockMethod[]
```

### response 函数参数

| 参数 | 说明 |
|------|------|
| `query` | URL query 参数（GET 参数） |
| `body` | 请求体（POST/PUT 的 JSON body） |
| `headers` | 请求头 |
| `params` | 路由参数（如 `/api/user/:id`） |

### 根据参数动态响应

```ts
// mock/user.ts
import type { MockMethod } from 'vite-plugin-mock'

export default [
  // POST 登录：根据 body 参数判断
  {
    url: '/api/auth/login',
    method: 'post',
    response: ({ body }) => {
      const { username, password } = body
      if (username === 'admin' && password === '123456') {
        return {
          code: 200,
          data: { token: 'mock-token-admin-xxx', name: '管理员' },
        }
      }
      return { code: 401, message: '账号或密码错误' }
    },
  },

  // GET 列表：支持分页参数
  {
    url: '/api/user/list',
    method: 'get',
    response: ({ query }) => {
      const page = Number(query.page) || 1
      const pageSize = Number(query.pageSize) || 10
      return {
        code: 200,
        data: {
          list: Array.from({ length: pageSize }, (_, i) => ({
            id: (page - 1) * pageSize + i + 1,
            name: `用户${(page - 1) * pageSize + i + 1}`,
          })),
          total: 100,
          page,
          pageSize,
        },
      }
    },
  },
] as MockMethod[]
```

---

## 四、结合 mockjs 生成随机数据

详见 → [mockjs 数据模板参考](./references/mockjs-templates.md)

### 快速示例

```ts
// mock/product.ts
import Mock from 'mockjs'
import type { MockMethod } from 'vite-plugin-mock'

export default [
  {
    url: '/api/product/list',
    method: 'get',
    response: () => {
      return Mock.mock({
        code: 200,
        'data|20': [{
          'id|+1': 1,                          // 自增 ID
          name: '@ctitle(4, 10)',               // 随机中文标题
          'price|10-9999.2': 1,                // 随机价格，保留2位小数
          'stock|0-500': 1,                    // 随机库存
          'status|1': ['上架', '下架', '预售'], // 随机从数组取一个
          createTime: '@datetime',             // 随机日期时间
          image: '@image("200x200", "#4A7BF7", "#fff", "@ctitle(2)")',
        }],
        total: 100,
      })
    },
  },
] as MockMethod[]
```

---

## 五、目录组织建议

```
mock/
├── index.ts         # 可选：统一导出或做一些全局配置
├── user.ts          # 用户相关接口
├── product.ts       # 商品相关接口
├── order.ts         # 订单相关接口
└── common.ts        # 公共接口（字典、枚举等）
```

每个文件按业务模块分组，导出 `MockMethod[]`，插件会自动扫描目录下所有文件。

---

## 六、在业务代码中使用

Mock 对业务代码完全透明，使用 axios：

```ts
// 正常调用，无需任何特殊处理
const { data } = await axios.get('/api/product/list', {
  params: { page: 1, pageSize: 20 }
})
```

如果项目有 axios 封装（baseURL），注意 mock 路径要和 baseURL 配合：

```ts
// axios 实例配置了 baseURL: '/api'
// 则 mock url 应为 /api/product/list（完整路径）
```

