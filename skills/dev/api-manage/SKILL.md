---
name: api-manage
description: 生成前后端接口代码时必须使用此 skill。触发场景包括：新增 API 接口、接口重构、前端 api/request 文件创建、后端 Controller/DTO 骨架生成、字段规范统一、错误码设计、前后端联调规范对齐。只要用户提到"写接口"、"生成 API"、"创建 Controller"、"封装请求"、"定义 DTO"、"前后端接口对接"等，立即触发此 skill，即使用户没有明确说"生成代码"也要触发。
---

# API 接口代码生成 Skill

## 执行流程（每次必须按序执行）
- **读取 API 文档** —— 查找 `@docs/api` 或用户提供的接口描述
- **按规范生成代码**，输出目录结构 + 完整代码

> 如果找不到 `@docs/api`，询问用户提供接口说明，不要自行假设字段。

---

## 前端生成规范（Vue3 + TypeScript）

### 目录结构

```
src/
├── api/
│   ├── request.ts        ← 已有封装，不新建
│   └── {entity}Api.ts    ← 本 skill 生成
└── types/
    └── {entity}.ts       ← 本 skill 生成
```

> ⚠️ `request.ts` 必须已存在才能生成 api 文件。若不存在，告知用户并停止，不自行创建。

### types/{entity}.ts 模板

```typescript
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

---

## 后端生成规范

根据用户技术栈选择对应模板：

- **Java Spring Boot** → 见下方 Java 规范
- **PHP Yii2** → 见下方 PHP 规范  
- **Python FastAPI / Flask** → 见下方 Python 规范

---

### Java Spring Boot

**目录结构：**
```
src/main/java/.../
├── controller/
│   └── {Entity}Controller.java
└── model/
    ├── {entity}/
    │   ├── {Entity}QueryReq.java
    │   ├── {Entity}CreateReq.java
    │   ├── {Entity}UpdateReq.java
    │   └── {Entity}Resp.java
```

**Controller 骨架：**
```java
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import tiktok_shop.common.result.Result;
import tiktok_shop.service.AffiliateSellerService;

@Slf4j
@Tag(name = "联盟卖家相关接口")
@RestController
@RequestMapping("/affiliate-seller")
public class AffiliateSellerController {

    @Autowired
    AffiliateSellerService affiliateSellerService;

    @Operation(summary = "搜索达人")
    @PostMapping("/search-creator")
    public Result<DTO> searchCreator(){
      return Result.success();
    }

    @Operation(summary = "与达人展开对话")
    @PostMapping("/create-conversation")
    public Result<DTO> createConversation(){
      return Result.success();
    }

    @Operation(summary = "发送即时消息")
    @PostMapping("/send-message")
    public Result<DTO> sendMessage(){
      return Result.success();
    }
```

---

### PHP Yii2

**目录结构：**
```
controllers/
└── {Entity}Controller.php
models/
└── dto/
    ├── {Entity}QueryForm.php
    ├── {Entity}CreateForm.php
    └── {Entity}UpdateForm.php
```

**Controller 骨架：**
```php
<?php
namespace app\controllers;

use yii\rest\ActiveController;
use yii\filters\VerbFilter;

class {Entity}Controller extends ActiveController
{
    public $modelClass = '{Entity}';

    public function behaviors(): array
    {
        return array_merge(parent::behaviors(), [
            'verbs' => [
                'class' => VerbFilter::class,
                'actions' => [
                    'index'  => ['GET'],
                    'view'   => ['GET'],
                    'create' => ['POST'],
                    'update' => ['PUT', 'PATCH'],
                    'delete' => ['DELETE'],
                ],
            ],
        ]);
    }

    /** GET /v1/{entity-path} 分页列表 */
    public function actionIndex(): array { return []; }

    /** GET /v1/{entity-path}/{id} 详情 */
    public function actionView(int $id): array { return []; }

    /** POST /v1/{entity-path} 创建 */
    public function actionCreate(): array { return []; }

    /** PUT /v1/{entity-path}/{id} 更新 */
    public function actionUpdate(int $id): array { return []; }

    /** DELETE /v1/{entity-path}/{id} 删除 */
    public function actionDelete(int $id): void {}
}
```

---

### Python FastAPI

**目录结构：**
```
app/
├── routers/
│   └── {entity}.py
└── schemas/
    └── {entity}.py
```

**Router 骨架：**
```python
from fastapi import APIRouter, Query
from app.schemas.{entity} import (
    {Entity}ListQuery, Create{Entity}Req, Update{Entity}Req, {Entity}Resp, PageResp
)

router = APIRouter(prefix="/api/v1/{entity-path}", tags=["{Entity}"])

@router.get("", response_model=PageResp[{Entity}Resp])
async def list_{entity}(params: {Entity}ListQuery = Query()):
    pass

@router.get("/{id}", response_model={Entity}Resp)
async def get_{entity}(id: int):
    pass

@router.post("", response_model={Entity}Resp)
async def create_{entity}(body: Create{Entity}Req):
    pass

@router.put("/{id}", response_model={Entity}Resp)
async def update_{entity}(id: int, body: Update{Entity}Req):
    pass

@router.delete("/{id}", status_code=204)
async def delete_{entity}(id: int):
    pass
```

---

### 字段规范

- 时间字段：统一 `yyyy-MM-dd HH:mm:ss` ，前后端保持一致
- 命名风格：前端 camelCase，后端按语言惯例（Java/PHP: camelCase，Python: snake_case）
- null vs 空数组：列表字段无数据返回 `[]`，单对象不存在返回 `null`
- 接口版本：路径统一前缀 `/api/v1/`

---

## 输出要求
- 必须输出完整目录结构
- 代码可直接复制使用
- 仅生成骨架，不实现业务逻辑
- 注释完整，说明每个方法用途
- 严格遵循用户项目已有的命名风格
```
