import json


def watch(path1, path2):
    with open(path1, 'r', encoding='utf8')as fp:
        json_data = json.load(fp)

    data = list()
    for i in json_data:
        del i['tag']
        del i['sentence']
        data.append(i)
    with open(path2, 'w', encoding='utf8')as fp:
        json.dump(data, fp, ensure_ascii=False)
