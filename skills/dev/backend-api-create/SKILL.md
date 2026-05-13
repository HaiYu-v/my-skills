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
