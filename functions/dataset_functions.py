import bpy


from ..global_variables import setting_prop_statement, setting_prop_error_statement


# return props of a dataset as a list [prop, value]
def returnDatasetProperties(dataset):
    properties_list = []

    for p in dataset.bl_rna.properties:
        if not p.is_readonly:
            value = getattr(dataset, p.identifier)
            properties_list.append([p, value])
    if len(properties_list) != 0:
        return properties_list

# set attributes from json
def setPropertiesFromJsonDataset(datasetin, datasetout, winman):
    for prop in datasetin:
        try:
            if winman.bpm_debug: print(setting_prop_statement + prop) ###debug
            setattr(datasetout, '%s' % prop, datasetin[prop])
        except (KeyError, AttributeError):
            if winman.bpm_debug: print(setting_prop_error_statement + prop) ###debug
            pass

# set attributes between 2 dataset
def setPropertiesFromDataset(datasetin, datasetout, winman):
    for prop in datasetin.bl_rna.properties:
        if not prop.is_readonly:
            try:
                if winman.bpm_debug: print(setting_prop_statement + prop.identifier) ###debug
                setattr(datasetout, '%s' % prop.identifier, getattr(datasetin, prop.identifier))
            except (KeyError, AttributeError):
                if winman.bpm_debug: print(setting_prop_error_statement + prop.identifier) ###debug
                pass