---
name: vue-refactor
description: 创建和重构页面/界面/组件/路由/store文件时使用。
---

## 相关目录
- 界面依据`@docs/prototype`生成
- 调用接口参考`src/api`
- 实体类参考 `src/type`
- 界面生成在`src/views`目录下


## 我的要求
- 列出任务列表, 一个任务一个任务的去完成

## 处理流程
1. 使用`src/api`和`src/type`来构建界面
2. 对组件进行修改, 尽可的使用UI库提供的组件,如: 图标,表格,菜单等等
3. 对css的设置方式进行修改,尽可能的改成TailwindCSS, 少写`<style>`
4. 新增或修改功能的时候,请列出修改计划, 并询问用户要执行哪些
5. 修改或新增界面后, router.ts文件需要更新
6. 使用skill`vue-front-beautify`对界面进行美化(不需要询问)


> 注意: 只是改动布局的设置方式, 而不是改动布局, 可以稍稍优化一下

## 技术栈
- 框架: Vue3 (Composition API + `<script setup>`)
- 构建: Vite + TypeScript
- 状态管理: Pinia
- 路由: Vue Router
- 样式: SCSS + TailwindCSS
- 请求: Axios
- 图表: ECharts
- UI:  Element Plus / Ant Design Vue (由用户指定)

## 项目目录结构
```
src/
├── api/             # 请求接口（按 controller 拆分）
|   └── request.ts   # 封装 axios 请求(只创文件, 不实现)
├── assets/          # 静态资源
├── components/      # 全局公共组件
├── constants/       # 常量信息（Enum、全局常量等）
├── directives/      # 自定义指令
│   ├── debounce.ts
│   ├── index.ts
│   └── permission.ts
├── lib/             # 第三方库（可选）
├── mock/            # Mock 接口数据
├── plugins/         # 插件配置（如 i18n）
├── router/          # 路由配置（按业务拆分）
├── store/           # Pinia（按业务拆分）
├── themes/          # 主题样式（可选）
├── types/           # TS 类型定义
├── utils/           # 工具函数
├── views/           # 页面目录（按模块划分）
│   ├── layouts/     # 系统布局（Layout）
│   ├── login/       # 登录页
│   ├── employee/    # employee 模块
│   │   ├── components/
│   │   └── employee-list.vue
│   └── role/        # role 模块
│       ├── components/
│       │   └── RoleForm.vue
│       ├── index.scss
│       └── role-update.vue
├── App.vue          # 根组件
├── main.ts          # 入口文件
└── style.scss       # 全局样式
```


### Pinia Store
```ts
// src/store/user.ts
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const info = ref<UserInfo | null>(null)
  // ...
  return { info }
})
```

### 路由配置
```ts
// 懒加载写法
{
  path: '/user/list',
  name: 'UserList',
  component: () => import('@/views/user/list/index.vue'),
  meta: { title: '用户列表', icon: 'user' }
}
```

## 注意事项
- 少使用 `any` 类型，多定义 TS 类型

## 禁止事项
- ❌ 不使用 Options API，统一用 `<script setup>`
- ❌ 组件不直接写在 views 根目录，必须按板块分层
- ❌ 不在组件内直接写 axios，必须通过 `src/api/` 封装
- ❌ 样式不写内联，使用 SCSS + Tailwind


