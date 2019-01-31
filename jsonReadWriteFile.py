import json

def load_json(fileName):    #Load Locally Saved Vehicles
    try:
        f = open(fileName, "r")
    except OSError:
        #print("In load_json, found OSError")
        raise OSError
        return
    try:
        jsonData = json.load(f)
        #print("In load_json, in try, type(jsonCarData): ", type(jsonCarData))
    except ValueError:
        #print("In load_json, found ValueError")
        raise ValueError
        return
    #print("Closing file")
    f.close()
    #print("Returning jsonCarData")
    return jsonData


def write_json(databaseFile, listOfData): #Write locally saved vehicles
    try:
        f = open(databaseFile, "w")
        jsonCarData = json.dumps(listOfData, indent="\t", sort_keys=True)
        f.write(jsonCarData)
        f.close()
        return
    except OSError:
        return
