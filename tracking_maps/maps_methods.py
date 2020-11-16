import json

json_files_path = './tracking_maps/json/'
maps_data = f'{json_files_path}/result.json'
nomenclature_index = f'{json_files_path}/nomenclature_index.json'


def get_data_from_file(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)


maps_data_file = get_data_from_file(json_file=maps_data)
nomenclature_indexes_file = get_data_from_file(json_file=nomenclature_index)


def get_nomenclature_by_index(index):
    for item in nomenclature_indexes_file:
        if index == item.get('id'):
            return item.get('nomenclature')

    return None


def filter_data(nomenclature_indexes_list, field):
    nomenclature_indexes = set(nomenclature_indexes_list or set())
    if not nomenclature_indexes:
        return []

    result = []

    for item in maps_data_file:
        for index in nomenclature_indexes:
            if item.get(field) == get_nomenclature_by_index(index):
                result.append(item)

    return result
