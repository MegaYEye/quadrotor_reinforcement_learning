class ExplorationReward(object):
    def __init__(self, client, collision_penalty = -200,
            height_penalty=-100,
            used_cams=[3], vehicle_rad=0.5, thresh_dist=3,
            goal_id=0, max_height = 40):
        self.collision_penalty = collision_penalty
        self.client = client
        self.used_cams = used_cams
        self.vehicle_rad = vehicle_rad
        self.tau_d = thresh_dist
        self.goal_id = goal_id
        self.max_height = max_height
        self.height_penalty = height_penalty

    def compute_reward(self, quad_state, quad_vel, collision_info):
        if collision_info.has_collided:
            reward = self.collision_penalty
        elif quad_state.z_val > self.max_height:
            reward = self.height_penalty
        else:
            client = self.client
            INF = 1e100
            max_depth_perspective = -INF
            max_depth_vis = -INF
            max_depth_planner = -INF
            for camera_id in used_cams:
               requests = [
                    ImageRequest(camera_id, query, True, False)
                    for query in [
                        AirSimImageType.DepthPerspective,
                        AirSimImageType.DepthVis,
                        AirSimImageType.DepthPlanner,
                    ]]
                responses = client.simGetImages(requests)
                max_depth_planner = max(max_depth_planner,
                    np.max(np.array(responses[0].image_data_float)))
                max_depth_vis = max(max_depth_vis,
                    np.max(np.array(responses[1].image_data_float)))
                max_depth_planner = max(max_depth_planner,
                    np.max(np.array(responses[2].image_data_float)))
            goals = [max_depth_perspective, max_depth_vis,
                        max_depth_planner]
            print("ExplorationReward: these are the goals = ", goals)
            dist = goals[self.goal_id]
            reward = (dist - self.vehicle_rad) / (self.tau_d - self.vehicle_rad)
            print("ExplorationReward: before truncating we have = ", reward)
            reward = min(reward, 1)
            print("ExplorationReward: after truncation we obtained: ", reward)

        return reward

class PathReward(object):

    def __init__(self, points=None,
            thresh_dist=7, beta=1,
            collision_penalty=-100,
            large_dist_penalty=-10,
            client=None):
        if points is None:
            points = [
               [-0.55265, -31.9786, -19.0225],
               [48.59735, -63.3286, -60.07256],
               [193.5974, -55.0786, -46.32256],
               [369.2474, 35.32137, -62.5725],
               [541.3474, 143.6714, -32.07256]
            ]
        self.points = list()
        for item in points:
            self.points.append(np.array(item))
        self.thresh_dist = thresh_dist
        sefl.beta = beta
        self.collision_penalty = collision_penalty
        self.large_dist_penalty = large_dist_penalty
        self.client = client

    def compute_reward(self, quad_state, quad_vel, collision_info):
        thresh_dist = self.thresh_dist
        beta = self.beta

        pts = self.points

        quad_pt = np.array(list((quad_state.x_val, quad_state.y_val, quad_state.z_val)))

        if collision_info.has_collided:
            reward = self.collision_penalty
        else:
            dist = 10000000
            for i in range(0, len(pts)-1):
                dist = min(dist, np.linalg.norm(np.cross((quad_pt - pts[i]), (quad_pt - pts[i+1])))/np.linalg.norm(pts[i]-pts[i+1]))

            #print(dist)
            if dist > thresh_dist:
                reward = self.large_dist_penalty
            else:
                reward_dist = (math.exp(-beta*dist) - 0.5)
                reward_speed = (np.linalg.norm([quad_vel.x_val, quad_vel.y_val, quad_vel.z_val]) - 0.5)
                reward = reward_dist + reward_speed

        return reward


