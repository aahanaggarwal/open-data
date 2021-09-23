import json

# this file was just to split the massive file into smaller shots files.

shots = json.load(open("shots.json", 'r'))

for ii, shot in enumerate(shots):
    with open('shots/shot{}.json'.format(ii), 'w+') as out:
        json.dump(shot, out, indent=2)
