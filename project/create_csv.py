from numpy.lib.function_base import angle
import pandas as pd
import json
from math import atan2

data = json.load(open('shots.json', 'r'))

num_shots = len(data)
CENTRE_OF_GOAL = (120, 40)
LEFT_OF_GOAL = (120, 36)
RIGHT_OF_GOAL = (120, 44)

def sign(p1, p2, p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

def player_between_goal(shot_location, player_location):
    pt = player_location
    v1, v2, v3 = shot_location, RIGHT_OF_GOAL, LEFT_OF_GOAL
    d1 = sign(pt, v1, v2)
    d2 = sign(pt, v2, v3)
    d3 = sign(pt, v3, v1)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    if has_neg and has_pos:
        return 0
    else:
        return 1

team = []
play_pattern = []
duration = []
distance_to_goal = []
angle_to_goal = []
players_between_goal = []
within_1 = []
within_5 = []
within_10 = []

goal = []


for shot in data:
    if 'freeze_frame' not in shot['shot'].keys():
        continue
    team.append(shot['possession_team']['name'])

    shot_location = shot['location']
    curr_dist = ((shot_location[0] - CENTRE_OF_GOAL[0])**2 + (shot_location[1] - CENTRE_OF_GOAL[1])**2)**0.5
    distance_to_goal.append(curr_dist)

    angle1 = atan2(LEFT_OF_GOAL[1] - shot_location[1], LEFT_OF_GOAL[0] - shot_location[0])
    angle2 = atan2(RIGHT_OF_GOAL[1] - shot_location[1], RIGHT_OF_GOAL[0] - shot_location[0])
    angle_to_goal.append(abs(min(angle1, angle2)))

    between_goal_count = 0

    within_1_count = 0
    within_5_count = 0
    within_10_count = 0

    for player in shot['shot']['freeze_frame']:
        curr_loc = player['location']
        between_goal_count += player_between_goal(shot_location, curr_loc) 
        dist_to_shot = ((curr_loc[0] - shot_location[0])**2 + (curr_loc[1] - shot_location[1])**2)**0.5
        if dist_to_shot < 1:
            within_1_count += 1
        if dist_to_shot < 5:
            within_5_count += 1
        if dist_to_shot < 10:
            within_10_count += 1

    within_1.append(within_1_count)
    within_5.append(within_5_count)
    within_10.append(within_10_count)

    players_between_goal.append(between_goal_count)
    play_pattern.append(shot['play_pattern']['name'])
    duration.append(shot['duration'])

    if shot['shot']['outcome']['name'] == "Goal":
        goal.append(1)
    else:
        goal.append(0)

df = pd.DataFrame({
    'team': team,
    'distant_to_goal': distance_to_goal,
    'play_pattern': play_pattern,
    'duration': duration,
    'angle_to_goal': angle_to_goal,
    'players_between_goal': players_between_goal,
    'within_1': within_1,
    'within_5': within_5,
    'within_10': within_10,
    'goal': goal,
})

df.to_csv('shots.csv', index=True, header=True, index_label='shot_num')
print(df.describe())