"""
迷宫问题
"""
from copy import deepcopy
from my_struct import MyStack, MyQueue

# 当前位置的下一步位置坐标
directions = [
    lambda x, y: (x - 1, y),
    lambda x, y: (x + 1, y),
    lambda x, y: (x, y - 1),
    lambda x, y: (x, y + 1),
]


def maze_stack(maze, start_xy, end_xy):
    """
    用栈方法解决迷宫问题
    深度优先：把走过的路线坐标存入栈，一条路失败后，通过坐标出栈，逐个退回，再重新试探新的路线坐标
    :param maze: 迷宫矩阵
    :param start_xy: 起点坐标
    :param end_xy: 终点坐标
    :return:
    """
    path = MyStack()
    path.push(start_xy)
    while not path.is_empty():
        curr_xy = path.get_pop()  # 当前坐标
        if curr_xy == end_xy:  # 到达终点
            print(path)
            return True
        for direction in directions:  # 试探下一步
            next_xy = direction(curr_xy[0], curr_xy[1])
            if maze[next_xy[0]][next_xy[1]] == 0:  # 有路，把下一步的坐标push入栈
                path.push(next_xy)
                maze[next_xy[0]][next_xy[1]] = 1  # 走过的路标记为墙
                break
        else:  # 无路，把上一步的坐标pop出栈
            path.pop()
    else:
        print('无解')
        return False


def real_path(path):
    """
    回溯路径
    :param path:
    :return:
    """
    r_path = []
    i = len(path) - 1
    while i >= 0:
        r_path.append(path[i].get('position'))
        i = path[i].get('flag')
    r_path.reverse()
    return r_path


def maze_queue(maze, start_xy, end_xy):
    """
    用队列方法解决迷宫问题
    广度优先：把每一个坐标的任意一个可以前进的下一步坐标，存入队列，并将当前坐标出队列存入历史路线，重复这种操作，直到达到终点坐标，路线也将是最短的路线
        为了能回溯路线到起点，需要在坐标进出队列操作时，同时也将该坐标与父坐标的指向关系传入
    :param maze: 迷宫矩阵
    :param start_xy: 起点坐标
    :param end_xy: 终点坐标
    :return:
    """
    q = MyQueue()
    path_flag = []
    start_gps = {  # GPS：坐标 + 与父坐标的指向关系
        'position': start_xy,
        'flag': -1,
    }
    q.append(start_gps)
    while not q.is_empty():
        curr_gps = q.popleft()
        path_flag.append(curr_gps)  # 路径追加GPS
        curr_xy = curr_gps.get('position')  # 当前坐标
        if curr_xy == end_xy:  # 到达终点
            print(real_path(path_flag))
            return True
        for direction in directions:  # 试探下一步
            next_xy = direction(curr_xy[0], curr_xy[1])
            if maze[next_xy[0]][next_xy[1]] == 0:  # 把所有能走的下一步GPS都存入队列
                next_gps = {
                    'position': next_xy,
                    'flag': len(path_flag) - 1,
                }
                q.append(next_gps)
                maze[next_xy[0]][next_xy[1]] = 1  # 走过的路标记为墙
    else:
        print('无解')
        return False


if __name__ == '__main__':
    the_maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
    maze1 = deepcopy(the_maze)
    maze2 = deepcopy(the_maze)
    start = (1, 1)
    end = (8, 8)
    # 栈方法：深度优先
    maze_stack(maze1, start, end)
    # 队列方法：广度优先
    maze_queue(maze2, start, end)
