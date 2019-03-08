
class CellType(object):
    EMPTY = " "
    PLAYER = "@"
    APPLE = "$"
    WALL = "#"
    OPPONENT = "O"
    AGENT_FRONT = "x"
    BEAM = "*"

class Colors:
    SCREEN_BACKGROUND = (10, 10, 10)  # BLACK
    CELL_TYPE = {
        CellType.WALL: (125, 125, 125),  # GRAY
        CellType.AGENT_FRONT: (50, 50, 50),  # DARK GRAY
        CellType.PLAYER: (0, 0, 255),  # BLUE
        CellType.OPPONENT: (255, 0, 0),  # RED
        CellType.APPLE: (0, 255, 0),  # GREEN
        CellType.BEAM: (255, 204, 51),  # Yellow
    }

'''def grid_reset(food_list, agent_list):
    grid = np.full([40, 20], ' ', dtype=object)
    for i in food_list:
        grid[i[0]][i[1]] = CellType.APPLE
    for agent in agent_list:
        grid[agent.x][agent.y] = CellType.PLAYER
        grid[agent.get_front_player()[0]][agent.get_front_player()[1]] = CellType.AGENT_FRONT
        #for beam in beam_set_list:
        #   grid[beam[0]][beam[1]] = CellType.BEAM
    return grid'''