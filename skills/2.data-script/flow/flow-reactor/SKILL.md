---
name: flow-reactor
description: |
  流水线数据处理模式的代码生成 skill。当用户需要将数据处理流程拆分为串联节点（pipeline/流水线）、
  或提到"处理节点"、"数据流水线"、"批量处理"、"固化数据"、等场景时触发。
---

## 流水线处理
把数据的处理流程拆成一个个处理节点, 节点串联形成一个流水线, 生成数据的原料, 进入流水线后一步步处理, 最终生成所需数据


## 流水线处理数据流程
- 定义产品的实体, 在model目录下
- 流水线入参和生成公共参数(节点共用参数)
- 生成数据原料(处理节点)
- 处理节点2
- 处理节点3
- ......
- 流水线收尾的处理(非节点)

## 我的要求
- 流水线是一个函数
- 处理节点也是一个函数
- 流水线和处理节点都要加上`@trace('描述信息')`

## 核心概念
```
原料 (unique_ids / 输入集合)
  └─→ 流水线主函数 @trace
        ├─→ 生成公共参数 (rank_map, recent_map, ...)
        ├─→ 处理节点1 @trace  ← 补充实体字段
        ├─→ 处理节点2 @trace
        ├─→ 处理节点3 @trace
        │   ...
        └─→ 收尾逻辑 (写库、分区替换，非节点)
```

---


## 流水线主函数参考代码
```python
@trace("流水线：处理XXX数据")
def solidify_xxx(unique_ids: list, cache: IdCache, market_id: int, date_s: str, date_e: str):

        # ── 2. 生成公共参数（各节点只读，不修改）──────────────
        ck = CK('ck_xx')
        rank_map: dict = {}
        _build_rank_map(rank_map, market_id, ck)
        recent_map: dict = {}
        _build_recent_map(recent_map, market_id, ck)

        # ── 3. 分批处理原料 ────────────────────────────────────
            # ── 处理节点（按依赖顺序调用）─────────────────────
            _node_restore_old_data(entity_map, tmp_21, market_id, ck_21)
            _node_fill_basic_info(entity_map, tmp_56, market_id, ck_56)
            _node_fill_content_tags(entity_map, tmp_56, market_id, ck_56)
            _node_fill_commerce_data(entity_map, tmp_56, market_id, ck_56)
            _node_fill_rank_and_recent(entity_map, rank_map, recent_map)

        # ── 4. 收尾：分区替换（流水线末尾，非节点）────────────
          # ── 写入替换表 ─────────────────────────────────────
              CkUtil.insert_dict(ck_21, replace_table, [e.model_dump() for e in entities])
              insert_total += len(entities)
              Log.log(f">>>>>> 已插入 {insert_total}")

              del entities, entity_map
              gc.collect()
```

---

## 处理节点函数
- 每个节点函数遵循统一签名：`(entity_map, 公共参数) -> None`
- entity_map (原料map, unqieu_id=原料)
```python
@trace("节点1")
def _node_restore_old_data(entity_map: dict, 公共参数):
    ...


@trace("节点2")
def _node_fill_basic_info(entity_map: dict, 公共参数):
    ...


@trace("节点3")
def _node_fill_rank_and_recent(entity_map: dict, 公共参数):
    ...
```

---

## 公共参数构建函数
公共参数构建函数也加 `@trace`，但**不是处理节点**（不操作实体 map）：
```python
@trace("构建排名 map")
def _build_rank_map(rank_map: dict, market_id: int, ck: CK):
    sql = f"""
        SELECT entity_id,
               ROW_NUMBER() OVER (ORDER BY gmv_count DESC) AS gmv_count_rank
        FROM {SysVar.TABLE_XXX}
        WHERE market_id = {market_id}
    """
    for row in ck.queryAll_dict(sql):
        rank_map[row['entity_id']] = row


@trace("构建环比 map")
def _build_recent_map(recent_map: dict, market_id: int, ck: CK):
    date_e = SysVar.RECENT_28_DATE_E
    date_s = TimeUtil.get_previous_day_str(date_e, 27)
    # ... 查询当期 & 上期，计算 mom = round(100*(cur/pre - 1), 2)
    # 结果写入 recent_map[entity_id][f"{field}_recent_28day_mom"]
```

---

## 命名规范

| 类型 | 前缀 | 示例 |
|------|------|------|
| 流水线主函数 | `solidify_` / `process_` | `solidify_creator` |
| 处理节点 | `_node_` | `_node_fill_basic_info` |
| 公共参数构建 | `_build_` | `_build_rank_map` |
| @trace 描述 | 动词+名词 | `"节点：填充基础信息"` |

---

## 检查清单（生成代码后自查）

- [ ] 所有函数（流水线 + 节点 + 公共参数构建）都有 `@trace('...')`
- [ ] 公共参数（rank_map 等）在流水线入口生成，只读传入节点
- [ ] 节点函数只修改 `entity_map` 中的实体字段，不写库
- [ ] 分区替换、写库等收尾操作在流水线末尾，不放进节点
- [ ] 分批处理后 `del + gc.collect()` 释放内存







