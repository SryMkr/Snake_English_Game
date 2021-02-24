# author： SryMkr
# date 2021.2.24

# The library consists of some basic functions to support Snake Game


# import packages
import pygame
import random
import numpy as np

# 26 alphabet
ALPHABET_LIST = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']

# the width of one frame
FRAME_WIDTH = 30


# show general texts of screen
def print_text(font_size, x_coordinate, y_coordinate, text, color=(0, 0, 0)):
    # return a surface
    text_img = font_size.render(text, True, color)
    # get window/screen/display surface  return surface
    screen = pygame.display.get_surface()
    # built surface onto screen
    screen.blit(text_img, (x_coordinate, y_coordinate))


# show game results of screen，这块随着词库的增加将来可能需要改
def print_result(font_size, x_start, y_start, list, color=(0,0,0)):
    # get window/screen/display surface  return surface
    screen = pygame.display.get_surface()
    # show the completed English words
    for text in list:
        # return a surface
        text_img = font_size.render(text, True, color)
        # draw result one by one
        screen.blit(text_img, (x_start, y_start))
        # change the x coordinate
        x_start += 240
        # change the y coordinate
        if x_start > 30 * 16:
            x_start = 0
            y_start += 120


# get index of words task 现在是直接把所有的单词保留进去，以后就是用一个加一个
# get the counterpart index of alphabet
def built_spelling_dic(task_list, alphabet_list):
    # create empty dictionary
    spelling_dic = {}
    # spelling index
    spelling_index = 1
    # task index
    task_index = 1
    # reture an alphabet dictionary for show correct alphabet
    for word in task_list:
        for correct_spelling in word:
            # find out every alphabet index
            alphabet_index = alphabet_list.index(correct_spelling)
            # built dictionary
            spelling_dic["{}-{}".format(task_index, spelling_index)] = alphabet_index
            # alphabet number plus 1 只是为了保证字典键值唯一，其他作用有待开发
            spelling_index += 1
        # word number plus 1
        # word_index is to track current word task
        task_index += 1
    # return dictionary
    return spelling_dic


# set audio of game
def game_audio(filename,volumn=0.1,times = 0):
    #initialize the mixer
    pygame.mixer.init()
    # get the sound file
    sound = pygame.mixer.Sound(filename)
    # force to find a channel
    channel = pygame.mixer.find_channel(True)
    # set music volume
    channel.set_volume(volumn)
    # directly play once call
    channel.play(sound,times)


# read words pool
def read_words_pool(filename):
    with open(filename,'r+') as f:
        # str-dic
        dic = eval(f.read())  # 读取的str转换为字典
        a = list(dic.values())
        return a[0],a[1]


# write words pool
def write_words_pool(filename,original_words_pool, known_words):
    dic = {}
    for word in known_words:
        if word not in original_words_pool:
            pass
        else:
            original_words_pool.remove(word)
    dic['0'] = original_words_pool
    dic['1'] = known_words
    with open(filename, 'w+') as f:
        # dic to str
        f.write(str(dic))



# read chinese meaning
def read_wordTra_pool(filename):
    with open(filename,'r',encoding='utf-8') as f:
        dic = eval(f.read())
        a = list(dic.values())
        return a[0], a[1]


# write chinese meaning
def write_wordTra_pool(filename,original_words_pool, known_words):
    dic = {}
    with open(filename, 'w+',encoding='utf-8') as f:
        for word in known_words:
            if word not in original_words_pool:
                pass
            else:
                original_words_pool.remove(word)
        dic['0'] = original_words_pool
        dic['1'] = known_words
        f.write(str(dic))


# save game records
def save_record(filename, highest_record):
    with open(filename, 'w',encoding='UTF-8') as f:
        f.write(str(highest_record))


# load game records
def load_record(filename):
    with open(filename, 'r',encoding='UTF-8') as f:
        record = f.read()
    return record


# save words phonetic
def save_pho(filename, highest_record):
    with open(filename, 'w',encoding='UTF-8') as f:
        f.write(str(highest_record))


# load words phonetic
def load_pho(filename):
    with open(filename, 'r',encoding='UTF-8') as f:
       record= f.read()
    return record


# for three different position of three different food
# in case they overlap
# the food cannot have the same axe coordinate with snake head
def food_random_position(snake_head_x_coordinate,snake_head_y_coordinate):
    # create x coordinate list
    x_coordinate_list = list(np.arange(0, 27)*FRAME_WIDTH)
    # avoid occasional snake head contact
    x_coordinate_list.remove(snake_head_x_coordinate)
    # create y coordinate list
    y_coordinate_list = list(np.arange(6, 24)*FRAME_WIDTH)
    # avoid occasional snake head contact
    y_coordinate_list.remove(snake_head_y_coordinate)
    # randomly choose three x coordinate
    x_coordinate = random.sample(x_coordinate_list, 3)
    # randomly choose three y coordinate
    y_coordinate = random.sample(y_coordinate_list, 3)
    # return the x, y coordinate
    return x_coordinate, y_coordinate


# define the snake head direction
def snake_head_direction(snake, snake_direction):
    # up
    if snake_direction.second_variate < 0:
        snake.snake_head.first_frame = 1 * snake.snake_head.multi_frames_columns
        snake.snake_head.last_frame = snake.snake_head.first_frame + 1
    #down
    elif snake_direction.second_variate > 0:
        snake.snake_head.first_frame = 3 * snake.snake_head.multi_frames_columns
        snake.snake_head.last_frame = snake.snake_head.first_frame + 1
    #lift
    elif snake_direction.first_variate < 0:
        snake.snake_head.first_frame = 0 * snake.snake_head.multi_frames_columns
        snake.snake_head.last_frame = snake.snake_head.first_frame + 1
    # right
    elif snake_direction.first_variate > 0:
        snake.snake_head.first_frame = 2 * snake.snake_head.multi_frames_columns
        snake.snake_head.last_frame = snake.snake_head.first_frame + 1
    # change to correct direction
    if snake.snake_head.current_frame < snake.snake_head.first_frame:
        snake.snake_head.current_frame = snake.snake_head.first_frame


# define two variate with two method respectively
class two_Variate(object):
    # define two private variates
    def __init__(self, variate_one, variate_two):
        self.__x = variate_one
        self.__y = variate_two

    # get first variate
    def get_variate_one(self): return self.__x
    # set first variate
    def set_variate_one(self, x): self.__x = x
    # the function of property is to allow variate_one have the two method
    # automatically trigger when calling
    # (property has claimed  the class property
    # therefore, there is not self before first_variate)
    first_variate = property(get_variate_one, set_variate_one)

    # get second variate
    def get_variate_two(self): return self.__y
    # set second variate
    def set_variate_two(self, y): self.__y = y
    # the function of property is to allow variate_one have the two method
    # automatically trigger when calling
    second_variate = property(get_variate_two, set_variate_two)




