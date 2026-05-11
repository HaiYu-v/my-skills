---
name: prototype-analysis
description: >
  当用户提供界面原型（HTML、截图、线框图、页面结构描述）并希望拆解前端实现方案时使用。
  触发词包括：分析这个页面、拆组件、梳理页面结构、生成开发方案、输出设计说明、前端怎么做。
  适用于 Vue3 项目开发前的原型拆解、组件设计、接口规划、实体建模。
---

# 核心目标
将界面原型转化为**可直接指导 Vue3 开发**的结构化方案，输出内容工程化、可落地。

# 输出原则
- 以组件化为第一原则
- 分析顺序：页面定位 → 布局结构 → 组件树 → 实体模型 → API 设计 → 状态管理
- 忽略全局公共组件（导航栏、侧边菜单）
- 区分容器组件（持有数据/状态）和展示组件（纯渲染）
- 明确父子通信方式（props/emits/pinia）
- 输出必须包含 TypeScript 类型定义和接口规范

---

# 分析流程

## 一、页面定位
- 页面名称与路由
- 核心目标（一句话）
- 用户角色
- 主要功能列表

## 二、布局结构
描述整体布局区域划分：
- 各区域：Header / Sidebar / Main / Footer / Modal / Drawer
- 每个区域说明：布局方式（Flex/Grid）、固定/自适应、是否滚动

## 三、组件树
以缩进树形式输出，标注组件类型：

```
PageName (容器)
├── FilterBar (容器) — 管理查询参数
│   ├── SearchInput (展示)
│   └── StatusSelect (展示)
├── DataTable (容器) — 管理列表数据
│   └── TableRowActions (展示)
└── Pagination (展示)
```

**每个组件说明：**
- 类型：容器 / 展示
- Props：列出关键入参及类型
- Emits：列出关键事件
- 内部状态（容器组件才需要）
- 关键样式说明（布局/尺寸/状态样式）

## 四、实体模型
提取页面涉及的业务实体，输出 TypeScript 接口：

```ts
interface User {
  id: number
  name: string
  status: 'enabled' | 'disabled'
  createdAt: string
}
```

## 五、API 设计
按业务动作推导接口（非机械按页面分类）：

| 动作 | Method | Path | 调用方 | 参数 | 返回 |
|------|--------|------|--------|------|------|
| 查询列表 | GET | /api/users | UserPage | page, pageSize, keyword, status | { list: User[], total: number } |
| 新增用户 | POST | /api/users | UserFormModal | UserCreateDTO | User |
| 删除用户 | DELETE | /api/users/:id | TableRowActions | id | void |

## 六、状态管理
- **组件内状态**（ref/reactive）：loading、modalVisible、formData
- **页面级状态**（组合式函数 useXxx）：queryParams、pagination、tableData
- **全局状态**（Pinia）：仅跨页面共享的数据，如 userInfo、permissions

---

# 输出格式
使用 Markdown，层级清晰，代码块标注语言。优先产出可复制使用的 TypeScript 类型和接口表格。
