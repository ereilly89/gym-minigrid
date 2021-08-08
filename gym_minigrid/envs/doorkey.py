from gym_minigrid.minigrid import *
from gym_minigrid.register import register

class DoorKeyEnv(MiniGridEnv):
    """
    Environment with a door and key, sparse reward
    """ 

    def __init__(self, size=8):
        super().__init__(
            grid_size=size,
            max_steps=10*size*size
        )

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place a goal in the bottom-right corner
        self.put_obj(Goal(), width - 2, height - 2)

        # Create a vertical splitting wall
        splitIdx = self._rand_int(2, width-2) # Ex) 2
        self.splitIdx = splitIdx
        self.grid.vert_wall(splitIdx, 0)

        # Place the agent at a random position and orientation
        # on the left side of the splitting wall
        self.agent_pos = self.place_agent(size=(splitIdx, height))

        # Place a door in the wall
        doorIdx = self._rand_int(1, width-2) # Ex) 2
        self.doorIdx = doorIdx
        self.door_pos = (splitIdx, doorIdx)
        self.put_obj(Door('yellow', is_locked=True), splitIdx, doorIdx)

        # Place a yellow key on the left side
        self.key_pos = self.place_obj(
            obj=Key('yellow'),
            top=(0, 0),
            size=(splitIdx, height)
        )

        self.mission = "use the key to open the door and then get to the goal"


    def _gen_state(self, width, height, stateInfo):
         # Create an empty grid
        self.grid = stateInfo["grid"]

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place a goal in the bottom-right corner
        self.put_obj(Goal(), width - 2, height - 2)

        # Create a vertical splitting wall
        self.grid.vert_wall(stateInfo["splitIdx"], 0)

        # Place the agent at a random position and orientation
        # on the left side of the splitting wall
        # self.place_agent(size=(stateInfo["splitIdx"], height))
        
        # Place agent as pre-determined position
        self.agent_pos = stateInfo["agent_pos"]
        self.put_obj(None, self.agent_pos[0], self.agent_pos[1])
        self.agent_dir = stateInfo["agent_dir"]


        # Place a door in the wall
        self.door_pos = (stateInfo["splitIdx"], stateInfo["doorIdx"])
        self.put_obj(Door('yellow', is_locked=True), stateInfo["splitIdx"], stateInfo["doorIdx"])

        # Place a yellow key on the left side
        self.key_pos = stateInfo["key_pos"]

        # Place key at pre-determined position
        self.put_obj(Key('yellow'), self.key_pos[0], self.key_pos[1])
        self.carrying = stateInfo["carrying"]
        self.step_count = stateInfo["step_count"]

        self.mission = "use the key to open the door and then get to the goal"


    """
    def _set_state(self, stateInfo):
        # Current position and direction of the agent
        self.agent_pos = None
        self.agent_dir = None

        # Generate a new random grid at the start of each episode
        # To keep the same grid for each episode, call env.seed() with
        # the same seed before calling env.reset()
        self._gen_state(self.width, self.height, stateInfo)
        

        # These fields should be defined by _gen_grid
        assert self.agent_pos is not None
        assert self.agent_dir is not None

        # Check that the agent doesn't overlap with an object
        start_cell = self.grid.get(*self.agent_pos)
        assert start_cell is None or start_cell.can_overlap()

        # Item picked up, being carried, initially nothing
        self.carrying = stateInfo["carrying"]

        # Step count since episode start
        self.step_count = stateInfo["step_count"]

        # Return first observation
        obs = self.gen_obs()
        return obs
    """
class DoorKeyEnv5x5(DoorKeyEnv):
    def __init__(self):
        super().__init__(size=5)

class DoorKeyEnv6x6(DoorKeyEnv):
    def __init__(self):
        super().__init__(size=6)

class DoorKeyEnv16x16(DoorKeyEnv):
    def __init__(self):
        super().__init__(size=16)

register(
    id='MiniGrid-DoorKey-5x5-v0',
    entry_point='gym_minigrid.envs:DoorKeyEnv5x5'
)

register(
    id='MiniGrid-DoorKey-6x6-v0',
    entry_point='gym_minigrid.envs:DoorKeyEnv6x6'
)

register(
    id='MiniGrid-DoorKey-8x8-v0',
    entry_point='gym_minigrid.envs:DoorKeyEnv'
)

register(
    id='MiniGrid-DoorKey-16x16-v0',
    entry_point='gym_minigrid.envs:DoorKeyEnv16x16'
)
