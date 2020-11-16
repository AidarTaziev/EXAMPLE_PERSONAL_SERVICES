def remove_keys_from_dict(keys_list, dict):
    for key in keys_list:
        if key in dict: del dict[key]


def replace_keys_from_dict(keys_dict, dict):
    for key in dict.keys():
        if key in keys_dict.keys():
            dict[keys_dict[key]] = dict.pop(key)

