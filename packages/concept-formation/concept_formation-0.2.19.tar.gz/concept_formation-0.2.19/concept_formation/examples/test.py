from concept_formation.trestle import TrestleTree
from concept_formation.datasets import load_rb_s_07
from concept_formation.datasets import load_rb_s_07_human_predictions

towers = {t['_guid']: t for t in load_rb_s_07()} 
human_predictions = load_rb_s_07_human_predictions()

human_data = {}
key = None
for line in human_predictions:
    line = line.rstrip().split(",")
    if key is None:
        key = {v:i for i,v in enumerate(line)}
        continue
    user = int(line[key['user_id']])
    order = int(line[key['order']])-1
    prediction = int(line[key['prediction']])
    guid = line[key['instance_guid']]
    
    if user not in human_data:
        human_data[user] = []

    human_data[user].append((order, guid, prediction))
    
for user in human_data:
    human_data[user].sort()

for user in human_data:
    tree = TrestleTree()

    for order, guid, prediction in human_data[user]:
        concept = tree.categorize(towers[guid])
        if order > 0:
            print("%i,%s,%s" % (order, prediction, int(concept.predict('success'))))
        tree.ifit(towers[guid])
 

