---
name: prototype-analysis
description: 当用户提供界面原型（HTML / 截图 / 线框图 / 图片转HTML）并希望分析前端实现方案、拆组件、梳理页面结构、生成开发设计文档时使用。适用于 Vue3 / React 项目前期的页面结构分析、组件设计、实体抽象、状态管理与 API 规划。
---

# 核心目标
将原型转化为可开发的前端工程方案，按：
页面定位 → 布局结构 → 组件树 → 数据实体 → 状态管理 → API设计 → 交互流程
- 输出结构化开发文档到`docs/prototype`目录下
- 一个界面一个md文件

---

# 输出原则
- 组件化优先（高复用、低耦合）
- 忽略全局公共框架（导航栏、侧边栏等非核心部分）
- 明确容器组件 / 展示组件
- 明确父子关系 / 同级关系 / 通信方式
- 明确布局方式（Flex / Grid / 响应式）
- 明确交互事件、状态变化、接口调用
- 明确业务实体（Entity）
- 明确前后端 API 需求
- 输出结果必须可直接指导开发
---

# 分析流程

## 一、页面定位（Page Purpose）
说明：
- 页面名称
- 核心目标
- 用户角色
- 核心功能
- 使用场景

---

## 二、布局结构（Layout Structure）
分析页面区域：
- Header
- Sidebar
- Main Content
- Footer
- Filter Bar
- Toolbar
- Modal / Drawer

输出：
- 布局模式（Flex / Grid / Absolute）
- 固定 / 自适应
- 滚动区域
- 响应式策略

---

## 三、组件拆解（Component Breakdown）
按组件树逐层拆解。

### 每个组件必须包含：
### 1. 名称
如：
- PageContainer
- SearchBar
- DataTable
- FormModal
- Pagination

### 2. 职责
- 展示
- 输入
- 筛选
- 数据承载
- 操作

### 3. 样式
- 尺寸
- 布局
- 间距
- 状态样式（hover / active / disabled）
- Tailwind / SCSS建议

---

## 四、组件关系（Component Relationships）

### 父子关系
说明：
- 谁管理数据
- 谁请求 API
- 谁负责展示
- 谁派发事件

示例：
UserPage
├── FilterBar
├── UserTable
└── Pagination

### 同级关系
说明：
- 是否共享状态
- 是否父组件中转
- 是否 Pinia / Redux

---

## 五、交互逻辑（Interaction Logic）

### 用户行为
- 点击
- 输入
- 搜索
- 切换
- 上传
- 分页
- 排序
- 拖拽

### 系统行为
- API调用
- Loading
- Toast
- 表单校验
- 弹窗
- 状态更新
- 乐观更新 / 回滚

### 输出格式
1. 用户动作
2. 触发组件
3. 调用 API
4. 更新状态
5. UI反馈

---

## 六、状态管理（State Management）

### 页面状态
- loading
- queryParams
- pagination
- modalVisible

### 全局状态
- userInfo
- token
- permissions

### 推荐方案
- 简单页：ref / reactive
- 中型页：composition hooks
- 跨页：Pinia / Redux

---

## 七、实体设计（Entity Design）

### 每个实体必须包含：
- 实体名
- 字段
- 类型
- 枚举值
- 前端用途

### 示例：
```ts
interface User {
  id: number
  name: string
  email: string
  status: 'enabled' | 'disabled'
  createdAt: string
}
````

---

## 八、API设计（Backend API Requirements）

### 按业务动作拆解：

* List
* Detail
* Create
* Update
* Delete
* Batch
* Toggle Status
* Upload
* Export
* Auth
* Permission
* Dictionary

---

### 每个 API 必须说明：

### 1. 接口

GET /api/users

### 2. 调用组件

UserTable / FilterBar

### 3. 调用时机

页面加载 / 搜索 / 分页

### 4. 请求参数

* page
* pageSize
* keyword
* status

### 5. 返回结构

```json
{
  "list": [],
  "total": 0
}
```

### 6. 前端处理

* 更新 tableData
* 更新 pagination
* loading=false

---

# 输出模板（必须遵循）

## 页面定位

...

## 布局结构

...

## 组件树

...

## 核心组件分析

### SearchBar

...

### DataTable

...

## 状态管理

...

## 实体设计

...

## API设计

...

## 用户交互流程

...

## 开发建议

* 组件复用建议
* 状态拆分建议
* 性能优化建议
* 可维护性建议

---

# 质量要求

* 不只描述“页面长什么样”，必须描述“前端怎么实现”
* 不只拆 UI，必须拆数据、状态、交互、接口
* 优先工程化，而非视觉化
* 输出结果应接近高级前端设计文档



