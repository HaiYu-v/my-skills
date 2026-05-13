---
name: prototype-analysis
description: 当用户希望分析界面原型, 拆组件、梳理页面结构、生成开发设计文档时使用。适用于 Vue3 / React 项目前期的页面结构分析、组件设计、实体抽象、状态管理与 API 规划。
---

# 核心目标
- 依据`@docs/html`提供的原型html, 将原型转化为可开发的前端工程方案
- 输出结构化开发文档到`docs/prototype`目录下
- 一个界面一个md文件

## 拆解框架

### 第一步：组件树分析

从HTML结构自顶向下拆，每个组件记录：

| 字段 | 说明 |
|---|---|
| 组件名 | 用功能命名，如 `KolSearchBar`、`LiveStreamTable` |
| 作用 | 这个组件解决什么问题 |
| 布局/样式 | flex/grid、尺寸、响应式断点、关键 class |
| 父子关系 | 谁包含它，它包含谁 |
| 兄弟关系 | 同层组件间是否共享状态 |
| 涉及事件 | 列出所有用户交互点 |

---

### 第二步：事件清单

每个事件记录：

```
事件名：点击搜索按钮
触发组件：KolSearchBar
行为类型：调用API
具体行为：
  - 收集 keyword/dateRange/platform 参数
  - 调用 GET /api/kol/list
  - 结果写入 KolTable 的数据源
  - loading 状态控制
副作用：重置分页到第1页
```

行为类型分类：
- **改数**：修改本地 state/store
- **调用API**：发请求，处理 loading/error
- **路由跳转**：`router.push()`
- **联动其他组件**：emit 事件或共享 store

---

### 第三步：实体识别

从表单字段、表格列、筛选条件里提取实体，每个实体记录：

**实体属性表**
```
实体：KOL（达人）
属性：
  - id: string
  - name: string（昵称）
  - platform: enum（tiktok/douyin）
  - follower_count: number
  - ...
```

**接口设计**（每个实体的 CRUD）：

```
GET /api/kol/list
描述：分页查询KOL列表
req: {
  keyword?: string,
  platform?: string,
  page: number,
  page_size: number
}
resp: {
  total: number,
  list: KOL[]
}

GET /api/kol/{id}
描述：KOL详情
resp: KOL & { live_records: LiveStream[] }
```

---

### 输出文档结构建议

```
PRD拆解文档
├── 1. 页面列表（路由表）
├── 2. 组件树（每页一棵树）
├── 3. 事件清单
├── 4. 实体 & 接口文档
└── 5. 状态管理设计（哪些数据放 store）
```

