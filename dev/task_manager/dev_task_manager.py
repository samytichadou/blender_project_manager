##### JSON #####

import json

def create_json_file(datas, path) :
    with open(path, "w") as write_file :
        json.dump(datas, write_file, indent=4, sort_keys=False)

def read_json(filepath):
    with open(filepath, "r") as read_file:
        dataset = json.load(read_file)
    return dataset

def isSerializable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False

def initializeJsonDatas(data_list) :
    datas = {}
    for d in data_list:
        datas[d] = []
    return datas


### TASKS MANAGEMENT ###

import os

def create_task_dataset(remove_list, add_list):
    dataset = initializeJsonDatas({'0_rem', '1_add'})
    for key in remove_list:
        dataset['0_rem'].append(key)
    for key in add_list:
        dataset['1_add'].append(key)
    return dataset

def find_task_filepath(json_filepath):
    if not os.path.isfile(json_filepath):
        return None
    parent_dir = os.path.dirname(json_filepath)
    json_filename = os.path.basename(json_filepath)
    if ".json" in json_filename:
        json_filename = json_filename.split(".json")[0]
    n = 0
    for file in os.listdir(parent_dir):
        if json_filename in file:
            if ".task" in file:
                n += 1
    task_filename = json_filename + ".task%i" % n
    #TODO check if task files are all there, no missing numbers
    return os.path.join(parent_dir, task_filename)

def create_task_file():
    return

### EXEC ###
def test_function(json_name):
    
    parentdir = os.path.dirname(__file__)
    fp = os.path.join(parentdir, json_name)

    origin_dataset = initializeJsonDatas({'entry1', 'entry2', 'entry3'})

    origin_dataset['entry1'].append("test")

    create_json_file(origin_dataset, fp)
    print(origin_dataset)

    print(os.path.basename(fp))

    target_dataset = initializeJsonDatas({'entry0', 'entry2', 'entry3'})


fp = r"C:\Users\tonton\Desktop\test_taskmanager\json_test.json"

#test_function("json_test.json")
print(find_task_filepath(fp))