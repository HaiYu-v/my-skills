---
name: backend-api-create
description: 生成后端接口代码时必须使用此 skill。触发场景包括：新增 API 接口、接口重构、后端 Controller/DTO 骨架生成.
---

## 我的要求
- 依据API文档`@docs/api`
- 生成后端controller接口和对应的resp,req类 

> 如果找不到 `@docs/api`，询问用户提供接口说明，不要自行假设字段。

---


## 后端生成规范
### Java Spring Boot

**目录结构：**
```
src/main/java/.../
├── controller/
│   └── {Entity}Controller.java
└── model/dto/
    └── {entity}/
        ├── Req.java
        └── Resp.java
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


### 字段规范

- 时间字段：统一 `yyyy-MM-dd HH:mm:ss` ，前后端保持一致
- 命名风格：前端 camelCase，后端按语言惯例（Java/PHP: camelCase，Python: snake_case）
- null vs 空数组：列表字段无数据返回 `[]`，单对象不存在返回 `null`
- 接口版本：路径统一前缀 `/api/v1/`


## 输出要求
- 必须输出完整目录结构
- 代码可直接复制使用
- 仅生成骨架，不实现业务逻辑
- 注释完整，说明每个方法用途
- 严格遵循用户项目已有的命名风格
