---
name: vue-front-create
description: 创建或搭建Vue前端项目、生成项目脚手架、创建页面/界面/组件/路由/store文件时使用。
---

## 参考
- 界面依据`@docs/prototype`生成
- 调用接口参考`src/api`
- 实体类参考 `src/type`
- 界面生成在`src/views`目录下


## 我的要求
- 列出任务列表, 一个任务一个任务的去完成
- 请尽可能的使用UI组件库提供的布局组件
- 请尽可的使用UI 组件库提供的组件,图标等
- css样式使用TailwindCSS, 尽可能的不写`<style>`
- 尽可能的使用已有的公共组件
- 修改或新增界面后, router.ts文件需要更新

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


## 布局结构

整体采用三段式布局，封装为 `layouts/DefaultLayout.vue`：
- **顶部导航栏** (NavBar)
- **左侧侧边栏** (Sidebar)
  - 支持折叠/展开（宽度切换，图标模式）
  - 菜单高亮跟随当前路由
  - 权限过滤（可扩展）
- **右侧内容区** (Main)，使用 `<router-view />` 渲染
```
┌──────────────── Header ────────────────┐
│ logo | nav |                  userInfo │
├──── Sidebar ────┬────  Main ───────────┤
│ menu            │ breadcrumb           │
│ menu            │ router-view          │
│ collapse        │                      │
└────────────────────────────────────────┘
```

## 代码规范

### Vue 组件
```vue
<template>
  <!-- 根元素只有一个 -->
</template>

<script setup lang="ts">
// 1. 导入
// 2. props/emits 定义
// 3. store/router
// 4. 响应式数据
// 5. 计算属性
// 6. 方法
// 7. 生命周期
</script>

<style lang="scss" scoped>
</style>
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


