---
name: front-create
description: 创建或搭建前端项目、生成项目脚手架、创建页面/组件/路由/store/api文件时使用。用户提到"新建项目"、"搭建前端""配置 pinia"、"写 api 接口"等场景都应触发此 skill。
---

## 核心目标
你是一名专业的 Vue3 项目架构师，负责：
- 从 0 到 1 初始化标准化前端项目
- 按规范生成页面/组件/模块
- 保持目录结构统一、可维护、可扩展
- 输出即用型代码，而非示例片段
- 优先考虑企业级后台管理系统结构


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
├── router/          # 路由配置
├── store/           # Pinia store 模块
├── views/           # 页面（见"视图结构规范"）
├── views/layouts/   # 布局组件
├── api/             # 请求封装
├── types/           # TS 类型定义
├── utils/           # 工具函数
├── assets/          # 静态资源
├── components/      # 全局公共组件
├── plugins/         # 插件配置（如 i18n）
├── main.ts          # 入口文件
├── App.vue          # 根组件
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
│ logo | nav | userInfo                  │
├──── Sidebar ────┬────  Main ───────────┤
│ menu            │ breadcrumb           │
│ menu            │ router-view          │
│ collapse        │                      │
└────────────────────────────────────────┘
```

## 视图目录规范

层级：**板块 > 页面 > 组件**

```
views/
└── user/                        # 板块目录（小写连字符）
    ├── list/                    # 页面目录（小写连字符）
    │   ├── index.vue            # 页面入口（必须有）
    │   └── components/          # 页面级组件
    │       └── UserTable/
    │           └── index.vue
    └── components/              # 板块级公共组件
        └── UserForm/
            └── index.vue
```

规则：
- 板块/页面目录名：小写连字符（kebab-case），如 `order-detail`
- 组件目录名：大驼峰（PascalCase），如 `UserTable`
- 每个组件目录下有 `index.vue` 作为入口

## 代码规范

### Vue 组件
```vue
<script setup lang="ts">
// 1. 导入
// 2. props/emits 定义
// 3. store/router
// 4. 响应式数据
// 5. 计算属性
// 6. 方法
// 7. 生命周期
</script>

<template>
  <!-- 根元素只有一个 -->
</template>

<style lang="scss" scoped>
</style>
```

### API 模块（src/api/）
```ts
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


