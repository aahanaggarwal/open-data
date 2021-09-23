import os
import json

files = [os.path.join("data/events", f) for f in os.listdir("data/events") if os.path.isfile(os.path.join("data/events", f))]

shots_file = open("shots.json", "a+")


for f_str in files:
    game_file = open(f_str, "r")
    game_data = json.load(game_file)
    shot_data = [event for event in game_data if event["type"]["id"] == 16]
    json.dump(shot_data, shots_file, indent=2)

