import json
from pprint import pprint

key = {}
key[1] = "x-axis"
key[2] = "y-axis"
key[3] = "month"
key[4] = "day"
key[5] = "FFMC"
key[6] = "DMC"
key[7] = "DC"
key[8] = "ISI"
key[9] = "temp"
key[10] = "RH"
key[11] = "wind"
key[12] = "rain"
key[13] = "area"

with open('/Users/cmaclell/Downloads/forestfires.csv', 'r') as fin:
    instances = []
    for line in fin:
        instance = {}

        for i,v in enumerate(line.strip().split(",")):
            if v == '?':
                continue

            try:
                v = float(v)
            except:
                pass

            instance[key[i+1]] = v

        instances.append(instance)

    pprint(json.dumps(instances))
        
        

        

