
def merge_dict_list(dict_list):
    def recur(hd, rest):
        if rest:
            return recur(merge_dicts(hd, rest[0]), rest[1:])
        else:
            return hd
    return recur(dict_list[0], dict_list[1:]) if dict_list else {}


def merge_dicts(parent_dict, child_dict):
    def merge(k, v):
        if isinstance(v, dict):
            if parent_dict.get(k) is None or (v == {} and not isinstance(parent_dict.get(k), dict)):
                parent_dict[k] = {}
            return merge_dicts(parent_dict[k], v)
        else:
            parent_dict[k] = v
    if child_dict:
        [merge(k, v) for k, v in child_dict.items()]
    return parent_dict