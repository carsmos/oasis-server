
### 场景树生成
def scenarios_to_tree(parent_id, parent_name, types, tags, scenarios, level):
    childs = []
    for scenario in scenarios:
        if scenario["parent_id"] == parent_id:
            childs.append(scenario)
    if childs:
        total = 0
        children = []
        for child in childs:
            child_tree = scenarios_to_tree(child["id"], child["name"], child["types"], child["tags"], scenarios, level + 1)
            total += child_tree["total"]
            children.append(child_tree)
        return {"id": parent_id, "name": parent_name, "tags": tags, "level": level, "total": total, "children": children}
    else:
        if types == "dir":
            return {"id": parent_id, "name": parent_name, "types": types, "tags": tags, "level": level, "total": 0}
        else:
            return {"id": parent_id, "name": parent_name, "types": types, "tags": tags, "level": level, "total": 1}


### 查找parent_id下的全部子场景，并组合成id列表
def file_child_ids_in_scenarios(parent_id, scenarios):
    childs = []
    for scenario in scenarios:
        if scenario["parent_id"] == parent_id:
            childs.append(scenario)
    if childs:
        file_child_ids = []
        for child in childs:
            if child["types"] == "dir":
                child_ids = file_child_ids_in_scenarios(child["id"], scenarios)
                file_child_ids.extend(child_ids)
            else:
                file_child_ids.append(child["id"])
        return file_child_ids
    else:
        return []


### 递归删除parent_id及其全部子场景
async def delete_scenario_group(scenario_id, scenarios, repo):
    childs = []
    for scenario in scenarios:
        if scenario["parent_id"] == scenario_id:
            childs.append(scenario)
    if childs:
        for child in childs:
            await delete_scenario_group(child["id"], scenarios, repo)

    await repo.delete_scenario_by_id(scenario_id)


