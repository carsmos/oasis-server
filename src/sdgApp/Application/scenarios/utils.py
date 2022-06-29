
### 场景树生成
def scenarios_to_tree(parent_id, parent_name, scenarios, level):
    childs = []
    for scenario in scenarios:
        if scenario.parent_id == parent_id:
            childs.append(scenario)
    total = 0
    children = []
    if childs:
        for child in childs:
            child_tree = scenarios_to_tree(child.id, child.name, scenarios, level + 1)
            total += child_tree["total"]
            children.append(child_tree)
        return {"name": parent_name, "level": level, "total": total, "children": children}
    else:
        return {"name": parent_name, "level": level, "total": 1}


### 查找parent_id下的全部子场景，并组合成id列表
def file_child_ids_in_scenarios(parent_id, scenarios):
    childs = []
    for scenario in scenarios:
        if scenario.parent_id == parent_id:
            childs.append(scenario)
    file_child_ids = []
    if childs:
        for child in childs:
            if child.types == "dir":
                child_ids = file_child_ids_in_scenarios(child.id, scenarios)
                file_child_ids.extend(child_ids)
            else:
                file_child_ids.append(child.id)
        return file_child_ids
    else:
        return []



