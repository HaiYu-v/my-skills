---
name: api-doc-create
description: 生成API文档, OpenAPI/Swagger 文档生成,接口文档生成时使用。
---

# 我的要求
- 生成OpenAPI 3.0 YAML文档
- 不需要生成数据模型schemas
- 生成的yaml文件能导入apifox或postman
- 每个字段都要有中文解释
- 字段使用`lowerCamelCase`进行命名

# 输出原则

## 1. 接口分析
包含：
- 接口用途
- 核心实体字段
- 请求方式选择原因
- 权限建议（可选）


## 2. RESTful API 设计
- 只用GET,POST和DELETE

---

## 3. OpenAPI 3.0 YAML
必须包含：
- openapi
- info
- servers
- tags
- paths
- parameters
- requestBody
- responses
- security（如涉及鉴权）

要求：
- 可直接用于 Swagger / Apifox / Postman 导入
- 示例值清晰

---


# 分页规范
统一参数：
- total 总数
- page 当前页
- pageSize 每页大小
- keyword 模糊搜索
- orderBy（ASC/DESC）
- sortBy 排序字段

统一返回：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "list": [],
    "total": 0,
    "page": 1,
    "pageSize": 10
  }
}
````

---

# 返回结构规范

## 成功

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

## 失败

```json
{
  "code": 1000,
  "message": "参数错误",
  "data": null
}
```

---

# 状态码规范

* 200 成功
* 1000 失败

---

# 命名规范

## URL

* 使用复数资源名词
* 使用 kebab-case
  示例：
* /users
* /user-orders


## 方法名
```
add / update / delete / detail / get 
get 获取/set 设置, 
add 增加/remove 删除, 
create 创建/destory 销毁, 
start 启动/stop 停止, 
open 打开/close 关闭, 
read 读取/write 写入, 
load 载入/save 保存,
begin 开始/end 结束, 
backup 备份/restore 恢复,
import 导入/export 导出, 
split 分割/merge 合并,
inject 注入/extract 提取,
attach 附着/detach 脱离, 
bind 绑定/separate 分离, 
view 查看/browse 浏览, 
edit 编辑/modify 修改,
select 选取/mark 标记, 
copy 复制/paste 粘贴,
undo 撤销/redo 重做, 
insert 插入/delete 移除,
add 加入/append 添加, 
clean 清理/clear 清除,
index 索引/sort 排序,
find 查找/search 搜索, 
increase 增加/decrease 减少, 
play 播放/pause 暂停, 
launch 启动/run 运行, 
compile 编译/execute 执行, 
debug 调试/trace 跟踪, 
observe 观察/listen 监听,
build 构建/publish 发布,
input 输入/output 输出,
encode 编码/decode 解码, 
encrypt 加密/decrypt 解密, 
compress 压缩/decompress 解压缩, 
pack 打包/unpack 解包,
parse 解析/emit 生成,
connect 连接/disconnect 断开,
send 发送/receive 接收, 
download 下载/upload 上传, 
refresh 刷新/synchronize 同步,
update 更新/revert 复原, 
lock 锁定/unlock 解锁, 
check out 签出/check in 签入, 
submit 提交/commit 交付, 
push 推/pull 拉,
expand 展开/collapse 折叠, 
enter 进入/exit 退出,
abort 放弃/quit 离开, 
obsolete 废弃/depreciate 废旧, 
collect 收集/aggregate 聚集
```
---