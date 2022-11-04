def map_dict_key(origin_dict, key_mapping):
    """
    Generate a new dict, which replace old key by new key.
    :param origin_dict:
    :param key_mapping: old_key: new_key dict mapping
    :return:
    """
    res = {}
    for old_key, new_key in key_mapping.items():
        res[new_key] = origin_dict.get(old_key)
    return res


def check_dict_update(origin_dict, new_dict):
    """
    Check whether origin dict data has changed, if changed, update the value.
    However, if new_dict doesn't have the key, the origin dict will keep the old value.
    :param origin_dict:
    :param new_dict:
    :return:
    """
    flag = False
    for key in origin_dict.keys():
        new_value = new_dict.get(key)
        origin_value = origin_dict.get(key)
        if new_value and new_value != origin_value:
            origin_dict[key] = new_value
            flag = True
    return flag, origin_dict


__all__ = ['map_dict_key', 'check_dict_update']
