import numpy as np
import matplotlib.pyplot as plt
import os
from colorama import Style, Fore
from copy import deepcopy
import bfs
import astar
import dfs
import pygame.constants

from source import ucs

TIME_OUT = 1800

path_board = os.getcwd() + '\\..\\Testcases'
path_checkpoint = os.getcwd() + '\\..\\Checkpoints'
print(1)


def get_boards():
    os.chdir(path_board)
    list_boards = []
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f'{path_board}\\{file}'
            board = get_board(file_path)
            list_boards.append(board)
    return list_boards


def get_check_points():
    os.chdir(path_checkpoint)
    list_checkpoints = []
    list_checkpoints_data = []
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f'{path_checkpoint}\\{file}'
            check_point = get_pair(file_path)
            list_checkpoints.append(check_point)
    return list_checkpoints


def get_board(file_path):
    result = np.loadtxt(f'{file_path}', dtype=str, delimiter=',')
    for row in result:
        format_row(row)
    return result


def get_pair(file_path):
    result = np.loadtxt(f'{file_path}', dtype=int, delimiter=',')
    return result


def format_check_point(checkpoints):
    result = []
    for check_point in checkpoints:
        result.append((check_point[0], check_point[1]))
    return result


def format_row(row):
    for i in range(len(row)):
        if row[i] == '1':
            row[i] = '#'
        elif row[i] == 'p':
            row[i] = '@'
        elif row[i] == 'b':
            row[i] = '$'
        elif row[i] == 'c':
            row[i] = '%'


# for board in get_boards():
#     print(board)
# for check_point in get_check_points():
#     print(check_point)

maps = get_boards()
checkpoints = get_check_points()
# print('Debug')
# checkpoints_map = checkpoints[0]
# print(checkpoints_map)
# print('End debug')
pygame.init()
pygame.font.init()
WINDOW_HEIGHT = 640
WINDOW_WIDTH = 640
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Sokobannnn')
pygame.display.set_icon(pygame.image.load('../Assets/12.png'))
clock = pygame.time.Clock()

BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)
assets_path = os.getcwd() + '\\..\\Assets'
os.chdir(assets_path)
player = pygame.image.load(os.getcwd() + '\\player.png')
wall = pygame.image.load(os.getcwd() + '\\wall.png')
box = pygame.image.load(os.getcwd() + '\\box.png')
space = pygame.image.load(os.getcwd() + '\\space.png')
point = pygame.image.load(os.getcwd() + '\\point.png')
arrow_left = pygame.image.load(os.getcwd() + '\\arrow_left.png')
arrow_right = pygame.image.load(os.getcwd() + '\\arrow_right.png')
init_background = pygame.image.load(os.getcwd() + '\\init_background.png')
loading_background = pygame.image.load(os.getcwd() + '\\loading_background.png')
notfound_background = pygame.image.load(os.getcwd() + '\\notfound_background.png')
found_background = pygame.image.load(os.getcwd() + '\\found_background.png')


def renderMap(board):
    width = len(board[0])
    height = len(board)
    indent = (640 - width * 32) / 2.0
    for i in range(height):
        for j in range(width):
            screen.blit(space, (j * 32 + indent, i * 32 + 200))
            if board[i][j] == '#':
                screen.blit(wall, (j * 32 + indent, i * 32 + 200))
            elif board[i][j] == '@':
                screen.blit(player, (j * 32 + indent, i * 32 + 200))
            elif board[i][j] == '$':
                screen.blit(box, (j * 32 + indent, i * 32 + 200))
            elif board[i][j] == '%':
                screen.blit(point, (j * 32 + indent, 32 * i + 200))


mapNumber = 0
algorithm = "Breadth First Search"
scene_state = 'init'
loading = False


def sokoban():
    running = True
    global scene_state
    global loading
    global algorithm
    global list_board
    global mapNumber
    stateLength = 0
    currentState = 0
    found = True
    while running:
        screen.blit(init_background, (0, 0))
        if scene_state == 'init':
            initGame(maps[mapNumber])

        if scene_state == 'executing':
            list_check_points = checkpoints[mapNumber]
            if algorithm == "Breadth First Search":
                print("BFS")
                list_board= bfs.BFS_Search(maps[mapNumber], list_check_points)
            elif algorithm == 'A Star Search':
                print("AStar")
                list_board= astar.AStar_Search(maps[mapNumber], list_check_points)
            elif algorithm == "Depth First Search":
                print('DFS')
                list_board= dfs.DFS_search(maps[mapNumber], list_check_points)
            elif algorithm == "Uniform Cost Search":
                print('UCS')
                list_board= ucs.UCS_Search(maps[mapNumber], list_check_points)
            if len(list_board) > 0:
                scene_state = "playing"
                stateLength = len(list_board[0])
                currentState = 0
            else:
                scene_state = "end"
                found = False
        if scene_state == "loading":
            loadingGame()
            scene_state = "executing"
        if scene_state == "end":
            if found:
                foundGame(list_board[0][stateLength - 1], stateLength)
            else:
                notfoundGame()
        if scene_state == "playing":
            clock.tick(2)
            renderMap(list_board[0][currentState])
            currentState = currentState + 1
            if currentState == stateLength:
                scene_state = "end"
                found = True
        # Check event when you press key board
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:

                # Press arrow key board to change level map
                if event.key == pygame.K_RIGHT and scene_state == "init":
                    if mapNumber < len(maps) - 1:
                        mapNumber = mapNumber + 1
                if event.key == pygame.K_LEFT and scene_state == "init":
                    if mapNumber > 0:
                        mapNumber = mapNumber - 1
                # Press ENTER key board to select level map and algorithm
                if event.key == pygame.K_RETURN:
                    if scene_state == "init":
                        scene_state = "loading"
                    if scene_state == "end":
                        scene_state = "init"
                # Press SPACE key board to switch algorithm
                if event.key == pygame.K_SPACE and scene_state == "init":
                    if algorithm == "Breadth First Search":
                        algorithm = "A Star Search"
                    elif algorithm == "A Star Search":
                        algorithm = "Depth First Search"
                    elif algorithm == "Depth First Search":
                        algorithm = "Uniform Cost Search"
                    else:
                        algorithm = "Breadth First Search"
        pygame.display.flip()
    pygame.quit()


def initGame(map):
    titleSize = pygame.font.Font('gameFont.ttf', 64)
    titleText = titleSize.render('SokobanGame', True, WHITE)
    titleRect = titleText.get_rect(center=(320, 80))
    screen.blit(titleText, titleRect)

    desSize = pygame.font.Font('gameFont.ttf', 24)
    desText = desSize.render('Select your map!', True, WHITE)
    desRect = desText.get_rect(center=(320, 144))
    screen.blit(desText, desRect)

    mapSize = pygame.font.Font('gameFont.ttf', 30)
    mapText = mapSize.render("Level. " + str(mapNumber + 1), True, WHITE)
    mapRect = mapText.get_rect(center=(320, 180))
    screen.blit(mapText, mapRect)

    screen.blit(arrow_left, (240, 260))
    screen.blit(arrow_right, (380, 260))

    algorithmSize = pygame.font.Font('gameFont.ttf', 30)
    algorithmText = algorithmSize.render(str(algorithm), True, WHITE)
    algorithmRect = algorithmText.get_rect(center=(320, 600))
    screen.blit(algorithmText, algorithmRect)
    renderMap(map)


def loadingGame():
    screen.blit(loading_background, (0, 0))

    fontLoading_1 = pygame.font.Font('gameFont.ttf', 40)
    text_1 = fontLoading_1.render('SHHHHHHH!', True, WHITE)
    text_rect_1 = text_1.get_rect(center=(320, 60))
    screen.blit(text_1, text_rect_1)

    fontLoading_2 = pygame.font.Font('gameFont.ttf', 20)
    text_2 = fontLoading_2.render('The problem is being solved, stay right there!', True, WHITE)
    text_rect_2 = text_2.get_rect(center=(320, 100))
    screen.blit(text_2, text_rect_2)


def foundGame(map, stateLength):
    screen.blit(found_background, (0, 0))

    font_1 = pygame.font.Font('gameFont.ttf', 30)
    text_1 = font_1.render('Yeah! The problem is solved!!!', True, WHITE)
    text_rect_1 = text_1.get_rect(center=(320, 100))
    screen.blit(text_1, text_rect_1)

    font_2 = pygame.font.Font('gameFont.ttf', 20)
    text_2 = font_2.render('Press Enter to continue.', True, WHITE)
    text_rect_2 = text_2.get_rect(center=(320, 600))
    screen.blit(text_2, text_rect_2)

    font_3 = pygame.font.Font('gameFont.ttf', 30)
    text_3 = font_3.render(f'{stateLength} moves', True, WHITE)
    text_rect_3 = text_3.get_rect(center=(320, 150))
    screen.blit(text_3, text_rect_3)

    renderMap(map)


def notfoundGame():
    screen.blit(notfound_background, (0, 0))

    font_1 = pygame.font.Font('gameFont.ttf', 40)
    text_1 = font_1.render('Oh no, I tried my best :(', True, WHITE)
    text_rect_1 = text_1.get_rect(center=(320, 100))
    screen.blit(text_1, text_rect_1)

    font_2 = pygame.font.Font('gameFont.ttf', 20)
    text_2 = font_2.render('Press Enter to continue.', True, WHITE)
    text_rect_2 = text_2.get_rect(center=(320, 600))
    screen.blit(text_2, text_rect_2)



def main():
    sokoban()


if __name__ == "__main__":
    main()