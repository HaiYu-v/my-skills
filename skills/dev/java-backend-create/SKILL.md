---
name: java-backend-create
description: 创建或搭建 Java Spring Boot 项目。当用户需要从零初始化一个 Spring Boot 后端项目、生成标准化目录结构、创建 Controller/Service/Mapper 等分层代码、配置 MyBatis-Plus、集成 Knife4j 文档、添加统一响应/异常处理、配置多数据源（MySQL + ClickHouse）时，必须使用此 skill。即使用户只说"帮我建一个 Spring Boot 项目"或"写一个接口"，也应触发。
---

## 相关目录
- 实体关系 `@docs/entity`
- 建表语句 `@docs/sql`
- api文档 `@docs/api`


## 我的要求
- 尽可能的使用`mybatis-plus`的`IService`进行数据库操作
- service 不需要定义接口 
- 不要使用`@Autowired`, 使用Lombok的`@RequiredArgsConstructor`

## 处理流程
- 实现controller接口


## 技术栈
| 类别 | 技术 |
|------|------|
| 框架 | Spring Boot 3.x、Spring MVC、Spring AOP |
| ORM | MyBatis-Plus 3.x |
| 数据库 | MySQL 8、ClickHouse |
| 工具库 | Lombok、Hutool |
| 文档 | Knife4j (OpenAPI 3) |
| 构建 | Maven |
| 其他 | Validation(jakarta)|

---

## 项目目录结构

```
src/main/java/{groupId}/{artifactId}/
├── config/                  # 配置类
├── common/                  # 公共模块
│   ├── result/
│   │   ├── R.java           # 统一响应体
│   │   └── ResultCode.java  # 响应码枚举
│   ├── exception/
│   │   ├── BizException.java          # 业务异常
│   │   └── GlobalExceptionHandler.java
│   └── aop/
│       └── LogAspect.java   # 日志切面
├── controller/              # 控制层（按业务模块）
├── service/                 # 服务层
├── mapper/                  # MyBatis-Plus Mapper
├── model/                  # 数据库实体（对应表）
│   ├── entity/                  # 数据库实体（对应表）
│   ├──dto/                     # 请求参数对象
│   └──vo/                      # 响应视图对象
├── utils/                   # 工具类
└── {ArtifactId}Application.java

src/main/resources/
├── mapper/                  # MyBatis XML（如需复杂 SQL）
├── application.yml          # 主配置
├── application-dev.yml      # 开发环境
└── application-prod.yml     # 生产环境
```

