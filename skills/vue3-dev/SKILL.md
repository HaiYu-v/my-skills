---
name: vue3-dev
description: vue3开发,当前端使用vue3开发时使用
---

## 项目结构
- src/view: 项目界面
  - 一个板块一个目录
    - 有components目录,板块封装组件
    - 有index.types.ts文件, 板块公用数据类型
  - 板块下一个界面也一个目录
    - 每个界面以index.vue为入口文件
    - 有components目录,界面封装组件
    - 有index.types.ts文件, 界面公用数据类型
  - 一个组件一个目录
    - 组件名的vue文件
    - 有index.types.ts文件, 组件的数据类型
- src/api: 项目请求api
 - 一个板块一个目录
 - 一个实体一个ts文件,仅写api方法 
- src/store: 项目store,使用pinia
参考
``` 
src/view
│
├─auth(权限板块)
│
└─tiktok-kol(tk达人板块)
    │  index.types.ts
    ├─brand-info
    │  │  index.types.ts
    │  │  index.vue
    │  └─components
    │
    └─components
           │
           └─RingPieChart
                   index.types.ts
                   index.vue
```

