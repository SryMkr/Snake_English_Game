'''
author： SryMkr
date: 2021.3.10
The library consists of some basic functions to
support Snake Game
'''

# import packages
import pygame
import random
import numpy as np
from Snake_food_library import MySprite_food

# 26 alphabet
ALPHABET_LIST = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']

# the width of one frame
FRAME_WIDTH = 30


# add correct  alphabet,正确单词图片在这修改
class Snakebody_alphabet(MySprite_food):
    def __init__(self, frame_nuber):
        MySprite_food.__init__(self)
        self.load_multi_frames("Game_Pictures/NEW_AL1.png", FRAME_WIDTH, FRAME_WIDTH, 13)
        self.draw_current_frame(frame_nuber)

# add wrong alphabet,错误单词图片在这修改
class wrong_alphabet(MySprite_food):
    def __init__(self, frame_nuber):
        MySprite_food.__init__(self)
        self.load_multi_frames("Game_Pictures/NEW_AL1.png", FRAME_WIDTH, FRAME_WIDTH, 13)
        self.draw_current_frame(frame_nuber)

# show general texts on the screen
def print_text(font_size, x_coordinate, y_coordinate, text, color=(0, 0, 0)):
    # return a surface
    text_img = font_size.render(text, True, color)
    # get window/screen/display surface  return surface
    screen = pygame.display.get_surface()
    # built surface onto screen
    screen.blit(text_img, (x_coordinate, y_coordinate))


# show game results of screen
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
        word = word.lower()
        word = word.strip()
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

# 获得输入的值
def game_play_setting(variables):
    return variables.get_value()

# 最多有三个干扰选项，加一个提示的位置，加一个正确选项，一共就是6个位置
# for three different position of three different food
# in case they overlap
# the food cannot have the same axe coordinate with snake head
def food_random_position(snake_head_x_coordinate,snake_head_y_coordinate,wrong_letters_num):
    # create x coordinate list
    x_coordinate_list = list(np.arange(0, 27)*FRAME_WIDTH)
    # avoid occasional snake head contact
    x_coordinate_list.remove(snake_head_x_coordinate)
    # create y coordinate list
    y_coordinate_list = list(np.arange(6, 24)*FRAME_WIDTH)
    # avoid occasional snake head contact
    y_coordinate_list.remove(snake_head_y_coordinate)
    # randomly choose three x coordinate
    x_coordinate = random.sample(x_coordinate_list, wrong_letters_num)
    # randomly choose three y coordinate
    y_coordinate = random.sample(y_coordinate_list, wrong_letters_num)
    # return the x, y coordinate
    return x_coordinate, y_coordinate



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




