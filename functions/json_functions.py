import json


# create json file
def create_json_file(datas, path) :
    with open(path, "w") as write_file :
        json.dump(datas, write_file, indent=4, sort_keys=False)

# read json
def read_json(filepath):
    with open(filepath, "r") as read_file:
        dataset = json.load(read_file)
    return dataset

# check if serializable
def isSerializable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False

# create json dataset
def createJsonDatasetFromProperties(datasetin, avoid_list):
    json_dataset = {}
    for p in datasetin.bl_rna.properties:
        if not p.is_readonly and p.identifier not in avoid_list:
            if isSerializable(getattr(datasetin, p.identifier)):
                json_dataset[p.identifier] = getattr(datasetin, p.identifier)
    return json_dataset

# initialize json asset datas
def initializeAssetJsonDatas(data_list) :
    datas = {}
    for d in data_list:
        datas[d] = []
    return datas
