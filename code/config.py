import json

from custom.action_space import DefaultActionSpace, \
    GridActionSpace, ActionSpaceType, make_action
from custom.reward import PathReward, RewardType, make_reward
from custom.constants import RootConfigKeys, ActionConfigKeys, \
        RewardConfigKeys, RewardConstants, ActionConstants


def make_default_root_config():
    root_config = dict()
    root_config[RootConfigKeys.TRAIN_AFTER] = 1000
    root_config[RootConfigKeys.SLEEP_TIME] = 0.1
    root_config[RootConfigKeys.INIT_X] = -0.55265
    root_config[RootConfigKeys.INIT_Y] = -31.9786
    root_config[RootConfigKeys.INIT_Z] = -19.0225
    root_config[RootConfigKeys.MOVE_DURATION] = 4
    root_config[RootConfigKeys.USE_FLAG_POS] = True
    root_config[RootConfigKeys.EPOCH_COUNT] = 100
    root_config[RootConfigKeys.MAX_STEPS_MUL] = 10000
    root_config[RootConfigKeys.MEMORY_SIZE] = 5000
    root_config[RootConfigKeys.TARGET_UPDATE_INTERVAL] = 50000
    root_config[RootConfigKeys.TRAIN_INTERVAL] = 4
    root_config[RootConfigKeys.ACTION_CONFIG] = {}
    root_config[RootConfigKeys.REWARD_CONFIG] = {}
    return root_config


def make_default_action_config(action_type):
    action_config = dict()
    action_config[ActionConfigKeys.ACTION_SPACE_TYPE] = action_type
    action_config[ActionConfigKeys.SCALING_FACTOR] = 0.25
    if action_type  == ActionSpaceType.GRID_SPACE:
        pass
    elif action_type == ActionSpaceType.DEFAULT_SPACE:
        action_config[ActionConfigKeys.GRID_SIZE] = 4
    else:
        raise ValueError("unknown action type")
    return action_config


def make_default_reward_config(reward_type):
    reward_config = dict()
    reward_config[RewardConfigKeys.COLLISION_PENALTY] = -1000
    reward_config[RewardConfigKeys.THRESH_DIST] = 7
    reward_config[RewardConfigKeys.REWARD_TYPE] = reward_type
    if reward_type == RewardType.EXPLORATION_REWARD:
        reward_config[RewardConfigKeys.EXPLORE_USED_CAMS_LIST] = [3]
        reward_config[RewardConfigKeys.EXPLORE_VEHICLE_RAD] = 7
        reward_config[RewardConfigKeys.EXPLORE_GOAL_ID] = 0
        reward_config[RewardConfigKeys.EXPLORE_MAX_HEIGHT] = 100
        reward_config[RewardConfigKeys.EXPLORE_HEIGHT_PENALTY] = -200
    elif reward_type == RewardType.PATH_REWARD:
        reward_config[RewardConfigKeys.PATH_BETA] = 1.0
        reward_config[RewardConfigKeys.PATH_POINTS_LIST] = None
        reward_config[RewardConfigKeys.PATH_LARGE_DIST_PENALTY] = -10
    else:
        raise ValueError("unknown reward type")
    return reward_config

def init_and_dump_configs():
    config_grid_path = make_default_root_config()
    config_grid_explore = make_default_root_config()

    config_default_path = make_default_root_config()
    config_default_explore = make_default_root_config()

    reward_explore = make_default_reward_config(
            RewardType.EXPLORATION_REWARD)
    reward_path = make_default_reward_config(
            RewardType.PATH_REWARD)

    action_grid = make_default_action_config(
            ActionSpaceType.GRID_SPACE)
    action_default = make_default_action_config(
            ActionSpaceType.DEFAULT_SPACE)

    for item in [config_grid_path, config_default_path]:
        item[RootConfigKeys.REWARD_CONFIG] = reward_path
    for item in [config_grid_explore, config_default_explore]:
        item[RootConfigKeys.REWARD_CONFIG] = reward_explore
    for item in [config_grid_path, config_grid_explore]:
        item[RootConfigKeys.ACTION_CONFIG] = action_grid
    for item in [config_default_path, config_default_explore]:
        item[RootConfigKeys.ACTION_CONFIG] = action_default

    names = ["grid_path", "default_path", \
            "grid_explore", "default_explore"]
    items = [config_grid_path, config_default_path, \
            config_grid_explore, config_default_explore]

    if not os.path.exists("config-example"):
        os.makedirs("config-example")
    for config, name in zip(items, names):
        with open("config-example/" + name + ".json", "w") as f:
            json.dump(config, f, indent=4)


