---
name: vue-component-create
description: 只有指定使用的时候才使用此skill. 创建 Vue3 前端组件时使用。适用场景：新建页面组件、功能模块、表单、列表、弹窗等任何 Vue3 组件开发任务。
---

# Vue3 组件开发规范

## 核心三原则

### 1. 假数据用 dict，不定义类型

Mock 数据直接写对象字面量，禁止声明 interface / type / class。

```ts
// ✅ 正确
const userInfo = { id: 1, name: '张三', role: 'admin', status: 1 }
const tableData = [
  { id: 1, title: '标题A', amount: 9800, createdAt: '2024-01-10' },
  { id: 2, title: '标题B', amount: 3200, createdAt: '2024-01-11' },
]

// ❌ 禁止
interface User { id: number; name: string }
const user: User = { id: 1, name: '张三' }
```

---

### 2. 虚拟 API 写在文件最开头

组件文件顶部（import 之后，组件定义之前）统一放虚拟 API 函数，返回 Promise 包裹的 mock 数据，模拟真实异步调用。

```ts
// ========== Mock API ==========
const fetchList = () => Promise.resolve({
  code: 0,
  data: {
    list: [
      { id: 1, name: 'KOL-001', fans: 128000, platform: 'tiktok' },
      { id: 2, name: 'KOL-002', fans: 56000, platform: 'instagram' },
    ],
    total: 2,
  },
})

const submitForm = (params) => Promise.resolve({ code: 0, msg: '提交成功' })
// ========== /Mock API ==========
```

> 后续对接真实接口时，只需替换此区块，组件逻辑无需改动。

---

### 3. 复用组件/函数：只读不改，需改则复制

- **可以**调用项目中已有的组件和函数
- **禁止**直接修改
- 如需定制行为，复制源码到当前文件，改副本，不动原件

```ts
// ✅ 复用已有工具函数
import { formatDate } from '@/utils/date'

// ✅ 需要定制时，复制一份在本文件修改
const formatDateCustom = (date, fmt = 'MM-DD HH:mm') => {
  // 基于 formatDate 逻辑复制后修改
  return dayjs(date).format(fmt)
}

// ❌ 禁止
// 直接去 @/utils/date.ts 里改 formatDate 的实现
```

> 注意: 请严格遵守这个规则, 不要去修改其它地方的代码

---

## 文件结构模板

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'
// 其他 import...

// ========== Mock API ==========
const fetchXxx = () => Promise.resolve({ code: 0, data: [] })
// ========== /Mock API ==========

// 状态
const loading = ref(false)
const list = ref([])

// 方法
const loadData = async () => {
  loading.value = true
  const res = await fetchXxx()
  list.value = res.data
  loading.value = false
}

onMounted(loadData)
</script>

<template>
  <!-- 模板内容 -->
</template>
```

---

## 快速检查清单

开始写组件前确认：

- [ ] Mock 数据是否用字面量对象，没有 interface/type？
- [ ] 虚拟 API 是否写在文件顶部 Mock API 区块内？
- [ ] 要复用的组件/函数是否只调用、不修改源文件？