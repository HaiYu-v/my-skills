---
name: java-backend-create
description: 创建或搭建 Java Spring Boot 项目。当用户需要从零初始化一个 Spring Boot 后端项目、生成标准化目录结构、创建 Controller/Service/Mapper 等分层代码、配置 MyBatis-Plus、集成 Knife4j 文档、添加统一响应/异常处理、配置多数据源（MySQL + ClickHouse）时，必须使用此 skill。即使用户只说"帮我建一个 Spring Boot 项目"或"写一个接口"，也应触发。
---

## 核心目标
你是一名专业的 Java Spring Boot 项目架构师，负责：
- 从 0 到 1 初始化标准化企业级后端项目
- 保持目录结构统一、可维护、可扩展
- 输出即用型代码，而非示例片段
- **列出任务清单，逐一完成**

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
│   ├── MybatisPlusConfig.java
│   ├── ClickHouseConfig.java
│   └── Knife4jConfig.java
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
│   └── impl/
├── mapper/                  # MyBatis-Plus Mapper
├── entity/                  # 数据库实体（对应表）
├── dto/                     # 请求参数对象
├── vo/                      # 响应视图对象
├── utils/                   # 工具类
└── {ArtifactId}Application.java

src/main/resources/
├── mapper/                  # MyBatis XML（如需复杂 SQL）
├── application.yml          # 主配置
├── application-dev.yml      # 开发环境
└── application-prod.yml     # 生产环境
```

---

## 标准代码模板


### application.yml

```yaml
spring:
  application:
    name: project-name
  profiles:
    active: dev
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://localhost:3306/db_name?useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai
    username: root
    password: password

mybatis-plus:
  mapper-locations: classpath:mapper/**/*.xml
  configuration:
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
    map-underscore-to-camel-case: true
  global-config:
    db-config:
      logic-delete-field: deleted
      logic-delete-value: 1
      logic-not-delete-value: 0

knife4j:
  enable: true
  openapi:
    title: 项目接口文档
    version: 1.0.0
```

### 统一响应体 R.java

```java
@Data
@NoArgsConstructor
@AllArgsConstructor
public class R<T> {

    private Integer code;
    private String msg;
    private T data;

    public static <T> R<T> ok() {
        return new R<>(ResultCode.SUCCESS.getCode(), ResultCode.SUCCESS.getMsg(), null);
    }

    public static <T> R<T> ok(T data) {
        return new R<>(ResultCode.SUCCESS.getCode(), ResultCode.SUCCESS.getMsg(), data);
    }

    public static <T> R<T> fail(String msg) {
        return new R<>(ResultCode.FAIL.getCode(), msg, null);
    }

    public static <T> R<T> fail(ResultCode resultCode) {
        return new R<>(resultCode.getCode(), resultCode.getMsg(), null);
    }
}
```

### ResultCode.java

```java
@Getter
@AllArgsConstructor
public enum ResultCode {
    SUCCESS(200, "操作成功"),
    FAIL(500, "操作失败"),
    UNAUTHORIZED(401, "未登录或登录已过期"),
    FORBIDDEN(403, "无权限访问"),
    NOT_FOUND(404, "资源不存在"),
    PARAM_ERROR(400, "参数校验失败");

    private final Integer code;
    private final String msg;
}
```

### BizException.java

```java
@Data
@EqualsAndHashCode(callSuper = true)
public class BizException extends RuntimeException {

    private Integer code;

    public BizException(String message) {
        super(message);
        this.code = ResultCode.FAIL.getCode();
    }

    public BizException(ResultCode resultCode) {
        super(resultCode.getMsg());
        this.code = resultCode.getCode();
    }
}
```

### GlobalExceptionHandler.java

```java
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    @ExceptionHandler(BizException.class)
    public R<Void> handleBizException(BizException e) {
        log.warn("业务异常: {}", e.getMessage());
        return R.fail(e.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public R<Void> handleValidException(MethodArgumentNotValidException e) {
        String msg = e.getBindingResult().getFieldErrors().stream()
            .map(FieldError::getDefaultMessage)
            .collect(Collectors.joining(", "));
        return R.fail(msg);
    }

    @ExceptionHandler(Exception.class)
    public R<Void> handleException(Exception e) {
        log.error("系统异常: ", e);
        return R.fail(ResultCode.FAIL.getMsg());
    }
}
```

### LogAspect.java（AOP 接口日志）

```java
@Aspect
@Component
@Slf4j
public class LogAspect {

    @Around("execution(* com.example..controller..*(..))")
    public Object around(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.currentTimeMillis();
        String method = pjp.getSignature().toShortString();
        log.info("[{}] 开始, 参数: {}", method, Arrays.toString(pjp.getArgs()));
        try {
            Object result = pjp.proceed();
            log.info("[{}] 完成, 耗时: {}ms", method, System.currentTimeMillis() - start);
            return result;
        } catch (Throwable e) {
            log.error("[{}] 异常: {}", method, e.getMessage());
            throw e;
        }
    }
}
```

### Controller 模板

```java
@Tag(name = "用户管理")
@RestController
@RequestMapping("/user")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @Operation(summary = "分页查询用户列表")
    @GetMapping("/page")
    public R<IPage<UserVO>> page(UserPageDTO dto) {
        return R.ok(userService.page(dto));
    }

    @Operation(summary = "新增用户")
    @PostMapping
    public R<Void> add(@Valid @RequestBody UserAddDTO dto) {
        userService.add(dto);
        return R.ok();
    }

    @Operation(summary = "更新用户")
    @PutMapping("/{id}")
    public R<Void> update(@PathVariable Long id, @Valid @RequestBody UserUpdateDTO dto) {
        userService.update(id, dto);
        return R.ok();
    }

    @Operation(summary = "删除用户")
    @DeleteMapping("/{id}")
    public R<Void> delete(@PathVariable Long id) {
        userService.removeById(id);
        return R.ok();
    }
}
```

### Service 模板

```java
public interface UserService extends IService<User> {
    IPage<UserVO> page(UserPageDTO dto);
    void add(UserAddDTO dto);
    void update(Long id, UserUpdateDTO dto);
}

@Service
@RequiredArgsConstructor
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {

    @Override
    public IPage<UserVO> page(UserPageDTO dto) {
        Page<User> page = new Page<>(dto.getPageNum(), dto.getPageSize());
        LambdaQueryWrapper<User> wrapper = Wrappers.<User>lambdaQuery()
            .like(StrUtil.isNotBlank(dto.getName()), User::getName, dto.getName())
            .orderByDesc(User::getCreateTime);
        Page<User> result = this.page(page, wrapper);
        // 转换 VO
        return result.convert(user -> BeanUtil.copyProperties(user, UserVO.class));
    }

    @Override
    public void add(UserAddDTO dto) {
        // 校验业务规则
        boolean exists = this.lambdaQuery().eq(User::getUsername, dto.getUsername()).exists();
        if (exists) {
            throw new BizException("用户名已存在");
        }
        User user = BeanUtil.copyProperties(dto, User.class);
        this.save(user);
    }

    @Override
    public void update(Long id, UserUpdateDTO dto) {
        User user = this.getById(id);
        if (user == null) {
            throw new BizException(ResultCode.NOT_FOUND);
        }
        BeanUtil.copyProperties(dto, user);
        this.updateById(user);
    }
}
```

### Entity 模板

```java
@Data
@TableName("t_user")
public class User {

    @TableId(type = IdType.AUTO)
    private Long id;

    private String username;

    private String nickname;

    @TableLogic
    private Integer deleted;

    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;

    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;
}
```

### MyBatisPlusConfig.java

```java
@Configuration
public class MybatisPlusConfig {

    /** 分页插件 */
    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
        interceptor.addInnerInterceptor(new PaginationInnerInterceptor(DbType.MYSQL));
        return interceptor;
    }

    /** 自动填充 createTime / updateTime */
    @Bean
    public MetaObjectHandler metaObjectHandler() {
        return new MetaObjectHandler() {
            @Override
            public void insertFill(MetaObject metaObject) {
                this.strictInsertFill(metaObject, "createTime", LocalDateTime.class, LocalDateTime.now());
                this.strictInsertFill(metaObject, "updateTime", LocalDateTime.class, LocalDateTime.now());
            }
            @Override
            public void updateFill(MetaObject metaObject) {
                this.strictUpdateFill(metaObject, "updateTime", LocalDateTime.class, LocalDateTime.now());
            }
        };
    }
}
```

### ClickHouseConfig.java（多数据源）

```java
@Configuration
public class ClickHouseConfig {

    @Bean(name = "clickHouseDataSource")
    @ConfigurationProperties(prefix = "spring.datasource.clickhouse")
    public DataSource clickHouseDataSource() {
        return DataSourceBuilder.create().build();
    }

    @Bean(name = "clickHouseJdbcTemplate")
    public JdbcTemplate clickHouseJdbcTemplate(
            @Qualifier("clickHouseDataSource") DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }
}
```

对应 application.yml 追加：
```yaml
spring:
  datasource:
    clickhouse:
      driver-class-name: com.clickhouse.jdbc.ClickHouseDriver
      url: jdbc:clickhouse://localhost:8123/default
      username: default
      password: ""
```

---

## 分页 DTO 基类

```java
@Data
public class PageDTO {
    @Schema(description = "页码", example = "1")
    private Integer pageNum = 1;

    @Schema(description = "每页条数", example = "10")
    private Integer pageSize = 10;
}
```

---

## 代码规范

### 命名约定
| 类型 | 规范 | 示例 |
|------|------|------|
| Entity | 对应表名（大驼峰） | `User`, `OrderItem` |
| DTO | 请求参数 + 场景后缀 | `UserAddDTO`, `UserPageDTO` |
| VO | 响应视图 | `UserVO` |
| Controller | 模块 + Controller | `UserController` |
| Service | 模块 + Service/ServiceImpl | `UserService` |
| Mapper | 模块 + Mapper | `UserMapper` |

### 注意事项
- 使用 `@RequiredArgsConstructor` + `final` 代替 `@Autowired`
- 禁止在 Controller 直接操作 Mapper，必须过 Service
- DTO/VO 与 Entity 分离，使用 `BeanUtil.copyProperties` 转换
- 所有接口必须添加 `@Tag` + `@Operation` 注解（Knife4j）
- 使用 `@Valid` 做入参校验，在 DTO 字段上加 `@NotNull`、`@NotBlank` 等
- ClickHouse 查询统一走 `clickHouseJdbcTemplate`，不走 MyBatis-Plus

### 禁止事项
- ❌ 不使用 `@Autowired` 字段注入，统一构造注入
- ❌ 不在 Service 里直接拼接 SQL 字符串，ClickHouse 复杂查询用命名占位符
- ❌ 实体类禁止返回给前端，必须转为 VO
- ❌ 不捕获异常后直接吞掉，必须日志 + 抛出或转换