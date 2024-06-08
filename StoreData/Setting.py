import json

def GetDataOnFileJson(NameFile):
    FilePath = f"StoreData/{NameFile}.json"
    file = open(FilePath, mode = "r")
    data = json.load(file)
    file.close()
    return data

def SaveDataSetting(NameFile, data):
    FilePath = f"StoreData/{NameFile}.json"
    savefile = open(FilePath,"w")
    json.dump(data, savefile, indent = 6)

class DataStore:
    SettingData = GetDataOnFileJson("Setting")
    StudyData = GetDataOnFileJson("Study")