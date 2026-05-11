---
name: interface-create
description: 创建或搭建前端创建页面/组件/路由/store/api文件时使用。用户提到"新建界面"、"搭建界面"、"创建页面"、"加一个路由"、"写一个组件"等场景都应触发此 skill。
---

## 视图目录规范
层级：**板块 > 页面 > 组件**

```
views/
└── user/                        # 板块目录（小写连字符）
    ├── relation/                # 页面目录（小写连字符）
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