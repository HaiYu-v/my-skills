---
name: map-entity
description: 生成实体关系图（ER Diagram）。当用户提到"ER图"、"实体关系图"、"数据库设计"、"表结构"、"画关系图"、"建模"，或者粘贴 SQL 建表语句、描述数据库表之间的关系时，使用此 Skill。支持从自然语言描述、SQL DDL、JSON/YAML 配置、代码模型类等多种输入生成专业的 ER 图。即使用户只是提到"帮我设计一个数据库"或"这几张表之间的关系是怎样的"，也应主动使用此 Skill 生成可视化图。
---

# ER Diagram Skill

从各种输入生成专业的实体关系图，输出为内嵌 SVG 的 HTML 可视化，使用 `show_widget` 工具渲染。

## 输入类型

- **自然语言**：用户描述系统或业务实体，如"一个博客系统，有用户、文章、评论"
- **SQL DDL**：`CREATE TABLE` 语句，自动解析字段和外键
- **JSON/YAML**：数据结构定义
- **代码模型类**：Python ORM (SQLAlchemy/Django)、Java JPA、PHP Eloquent 等

---

## 解析步骤

### 1. 提取实体

从输入中识别：
- **实体名称**（表名 / 类名 / 名词）
- **字段列表**：名称、类型、约束（PK / FK / NOT NULL / UNIQUE）
- **关系**：1:1、1:N、N:M

### 2. 识别关系类型

| 关系      | 标记方式                  |
|-----------|--------------------------|
| 一对一    | `──────`（单线双竖）      |
| 一对多    | `──────<`（crow's foot）  |
| 多对多    | `>──────<`                |
| 可选      | `o──`（圆圈）             |
| 必须      | `\|──`（竖线）            |

### 3. 布局规则

- 每个实体渲染为矩形卡片，标题栏 + 字段列表
- PK 字段用 🔑 标注，FK 字段用 🔗 标注
- 关系用带箭头的连线表示，线上标注关系名称（可选）
- 自动分层布局：主表居中，子表环绕

---

## 渲染规范

使用 `visualize:read_me` 加载 `diagram` 模块，然后调用 `show_widget` 输出 HTML。

### HTML 结构模板

```html
<!-- 使用 SVG + foreignObject 或纯 HTML div 渲染 -->
<div style="font-family: var(--font-sans); background: var(--bg-default);">
  <!-- 实体卡片 + SVG 连线层 -->
</div>
```

### 实体卡片样式

```css
/* 使用 CSS 变量保持主题一致 */
.entity {
  border: 2px solid var(--border-default);
  border-radius: 8px;
  background: var(--bg-card);
  min-width: 180px;
}
.entity-title {
  background: var(--accent);
  color: white;
  padding: 8px 12px;
  font-weight: bold;
  border-radius: 6px 6px 0 0;
}
.entity-field {
  padding: 4px 12px;
  border-bottom: 1px solid var(--border-subtle);
  font-size: 13px;
  display: flex;
  justify-content: space-between;
}
.pk { color: var(--gold); font-weight: bold; }
.fk { color: var(--blue); }
.type { color: var(--text-muted); font-size: 11px; }
```

### 连线绘制

使用 SVG `<path>` 绘制贝塞尔曲线连线：

```javascript
// 计算两个卡片之间的连接点
function getConnectorPath(from, to) {
  // from/to: {x, y, width, height}
  // 选择最近的边中点作为连接点
  // 返回 SVG path d 属性
}
```

Crow's foot 符号用 SVG `<marker>` 定义：
- 多端（Many）：三叉符号
- 一端（One）：竖线
- 可选（Optional）：圆圈

---

## 完整实现示例

当收到输入后，生成类似如下的 HTML widget：

```html
<div id="er-container" style="position:relative; width:100%; overflow:auto; min-height:400px;">
  <!-- SVG 连线层（绝对定位，z-index:0） -->
  <svg id="lines-layer" style="position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;">
    <defs>
      <!-- 定义 crow's foot markers -->
    </defs>
    <!-- 连线路径 -->
  </svg>
  
  <!-- 实体卡片层（相对定位，z-index:1） -->
  <div id="entities-layer" style="position:relative;z-index:1;display:flex;flex-wrap:wrap;gap:40px;padding:40px;">
    <!-- 实体卡片 -->
  </div>
</div>

<script>
  // 渲染完成后，根据卡片实际位置重绘连线
  function redrawLines() { ... }
  window.addEventListener('load', redrawLines);
</script>
```

---

## 常见场景处理

### SQL DDL 输入

```sql
CREATE TABLE users (
  id INT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE
);
CREATE TABLE posts (
  id INT PRIMARY KEY,
  user_id INT REFERENCES users(id),
  title VARCHAR(200)
);
```

→ 解析出 `users` 和 `posts` 两个实体，`posts.user_id → users.id` 为 N:1 关系。

### 自然语言输入

"电商系统：用户可以下多个订单，每个订单包含多个商品，商品属于某个分类"

→ 识别实体：`User`、`Order`、`OrderItem`、`Product`、`Category`
→ 关系：User 1:N Order，Order 1:N OrderItem，OrderItem N:1 Product，Product N:1 Category

### 多对多处理

自动识别并展示中间关联表（如 `order_items`），或用虚线菱形标注逻辑 N:M 关系。

---

## 输出要求

1. 图表可以水平滚动（实体多时）
2. 每个字段显示：图标 + 字段名 + 数据类型
3. 关系线附带标签（如 "contains"、"belongs_to"）
4. 提供图例说明 PK/FK/关系类型符号
5. 颜色区分不同实体类型（主实体 vs 关联表）

---

## 注意事项

- 若字段超过 8 个，折叠非关键字段，显示 "...+N more fields" 可展开
- 输入为代码时，先完整解析再渲染，避免遗漏关系
- 若关系不明确，在图下方列出假设，请用户确认
- 实体数量 > 10 时，建议按模块分组，用颜色区分模块