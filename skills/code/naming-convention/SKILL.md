---
name: naming-convention
description: 在变量,文件,标签等命名时使用
---


## 命名规范

| 类型 | 规则 | 示例 |
|------|------|------|
| 项目/目录/文件 | 小写+中划线 | `my-project/` |
| 目录复数 | 复数命名 | `images/`, `components/` |
| 变量/方法 | 小驼峰 | `getUserInfo()` |
| 常量 | 全大写下划线 | `MAX_COUNT` |
| 类/组件 | 大驼峰 | `UserCard` |

**禁止**：拼音、中文、无意义缩写、下划线起止


## Vue规范

### 组件
- 名称：**多个单词** + **PascalCase**（文件）
- 基础组件：`base-` 前缀
- 紧密耦合：父组件名作前缀

### Router
- 传参用**路由参数**（避免刷新丢失）
- 使用**路由懒加载**
- path：`kebab-case` + 以 `/` 开头
- name：`PascalCase` 且与组件名一致





