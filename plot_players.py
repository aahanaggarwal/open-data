
#%%

import matplotlib.pyplot as plt

plt.style.use("seaborn-whitegrid")

import numpy as np

x = np.linspace(0, 10, 30)
y = np.sin(x)

plt.plot(x, y, 'o', color = 'black')
# %%

# this file won't work now since i've split the shots file.
import json

shots_file = open("shots.json", "r")
shots_data = json.load(shots_file)
print(shots_data[0]["shot"]["freeze_frame"])
# %%
import random

shots = [random.randint(0, len(shots_data)) for _ in range(20)]

shots = filter(lambda x: "freeze_frame" in shots_data[x]["shot"].keys(), shots)

for shot_num in shots:

    print(shots_data[shot_num]["id"])
    points, names = [], []
    for player in shots_data[shot_num]["shot"]["freeze_frame"]:
        points.append(player["location"])
        names.append(player["player"]["name"].split(" ")[0])

    ball_loc = shots_data[shot_num]["location"]
    end_loc = shots_data[shot_num]["shot"]["end_location"]

    points = np.array(points)
    x, y = points.T
    plt.scatter(x,y)

    plt.scatter(ball_loc[0], ball_loc[1], marker='x')
    plt.scatter(end_loc[0], end_loc[1], marker='+')

    for i, txt in enumerate(names):
        plt.annotate(txt, (x[i], y[i]))

    plt.annotate("ball end", (end_loc[0], end_loc[1]))
    plt.show()
# %%
