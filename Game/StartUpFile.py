import importlib

os = importlib.import_module("os")
pd = importlib.import_module("pandas")

SoLevel = 1

def LoadFile(path):
    Lst = []
    FileList = os.listdir(path)
    FileList.sort(key = lambda b : int(b.split(".")[0]))

    for File in FileList:
        Lst1 = []
        f = open(os.path.join(path, File))
        Data = f.read().split("\n")

        if '' in Data: 
            Lst.append([])
            continue

        for D in Data:
            D = list(map(int, D.split(" ")))

            if len(D) == 3:
                Position = (D[0], D[1], D[2])

            else:
                Position = (D[0], D[1])

            Lst1.append(Position)
        
        Lst.append(Lst1)
    
    return Lst

# import pandas as pd

def LoadMapData(path):
    Lst = []
    FileList = os.listdir(path)
    FileList.sort(key = lambda b : int(b.split(".")[0]))
    for File in FileList:
        df = pd.read_excel(os.path.join(path, File), header=None)
        mapdata = df.values
        Lst.append(mapdata)
    
    return Lst

PosCorrectGateFilePath = "StoreData\\Map\\Data\\PosCorrectGate"
PosGateClockFilePath = "StoreData\\Map\\Data\\PosGateClock"
MapDataPath = "StoreData\\Map\\Data\\Map"

CorrectGateList = LoadFile(PosCorrectGateFilePath)
GateClockList = LoadFile(PosGateClockFilePath)
MapData = LoadMapData(MapDataPath)