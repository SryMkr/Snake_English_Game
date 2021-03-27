'''
author: SryMkr
date: 2021.3.11
this function is for load record
'''


# import packages
from Other_library import print_text, FRAME_WIDTH
import pygame, sys
from pygame.locals import *
from xlutils.copy import copy
import xlrd


# read game text records
def load_record(filename):
    with open(filename, 'r',encoding='UTF-8') as f:
        record = f.read()
    return record



# define a game introduction
def game_intro(screen, font):
    running = True
    while running:
        # load background picture
        game_intro = pygame.image.load("Game_Pictures/game_intro.jpg").convert_alpha()
        # scale to display
        game_intro = pygame.transform.scale(game_intro, (FRAME_WIDTH * 27, FRAME_WIDTH * 24))
        # draw
        screen.blit(game_intro, (0, 0))
        # load
        text = load_record('words_pool/game_introduction.txt').split('\n')
        y = 0
        for i in range(len(text)):
                text[i].strip()
                print_text(font,0,y,text[i])
                y += 50
        # must be here
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            running = False
        pygame.display.update()


# write record into excel.xls value is a list
def write_excel_game_record(path, value):
    # open a workbook
    workbook = xlrd.open_workbook(path)
    # copy the workbook
    new_workbook = copy(workbook)
    # get the first worksheet
    new_worksheet = new_workbook.get_sheet(0)
    # 第二行第一列是总记忆的单词数
    new_worksheet.write(1, 0, value[0])
    # 第二行第二列是总共玩游戏的时长
    new_worksheet.write(1, 1, value[1])
    # 第二行第一列是总记忆的单词数
    new_worksheet.write(3, 0, value[2])
    # 第二行第二列是总共玩游戏的时长
    new_worksheet.write(3, 1, value[3])
    # 每次写文件都需要创建新文件然后覆盖原文件
    new_workbook.save(path)


# check whether the words in excel.xls
def read_excel_game_record(path):
    # create a empty list
    list = []
    # open workbook
    workbook = xlrd.open_workbook(path)
    # get all sheets by sheet names
    sheets = workbook.sheet_names()
    # get the first sheet
    worksheet = workbook.sheet_by_name(sheets[0])
    # get the correspond content
    total_words = worksheet.cell_value(1, 0)
    total_time = worksheet.cell_value(1, 1)
    highest_score = worksheet.cell_value(3, 0)
    highest_words = worksheet.cell_value(3, 1)
    # add the record into the list
    list.append(total_words)
    list.append(total_time)
    list.append(highest_score)
    list.append(highest_words)
    # return the record list
    return list


# check whether the word in excel.xls
def read_excel_game_review(path):
    # open workbook
    list = []
    workbook = xlrd.open_workbook(path)
    # get all sheets by sheet names
    sheets = workbook.sheet_names()
    # get the first sheet
    worksheet = workbook.sheet_by_name(sheets[0])
    # get the rows of sheet
    old_nrows = worksheet.nrows
    old_cols = worksheet.ncols
    for i in range(old_nrows):
        for j in range(old_cols):
        # get the correspond content
            total_words = worksheet.cell_value(i, j)
            list.append(total_words)
    return list


# show game history
def game_record(screen,font):
    running = True
    while running:
        game_intro = pygame.image.load("Game_Pictures/game_intro.jpg").convert_alpha()
        game_intro = pygame.transform.scale(game_intro, (FRAME_WIDTH * 27, FRAME_WIDTH * 24))
        screen.blit(game_intro, (0, 0))
        list_review=read_excel_game_review('saved_files/game_review.xls')
        list_record = read_excel_game_review('saved_files/game_record.xls')
        print_text(font, 0, 0, str(list_record[0])+':')
        print_text(font, 150, 0, str(int(list_record[2])))
        print_text(font, 0, 50, str(list_record[1])+':')
        print_text(font, 150, 50, str(round(list_record[3],2))+'分钟')
        x = 0
        y = 100
        for i in range(len(list_review)):
            print_text(font, x, y, str(list_review[i]))
            x += 150
            if x >= 600:
                x = 0
                y += 50
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            running = False
        pygame.display.update()


# write record into excel.xls
def write_excel_game_review(path, value):
    # open a workbook
    workbook = xlrd.open_workbook(path)
    # get all sheet names
    sheets = workbook.sheet_names()
    # get the first sheet
    worksheet = workbook.sheet_by_name(sheets[0])
    # get the rows of sheet
    old_nrows = worksheet.nrows
    # copy the workbook
    new_workbook = copy(workbook)
    # get the first worksheet
    new_worksheet = new_workbook.get_sheet(0)
    if old_nrows == 9:
        for i in range(7):
            for j in range(4):
                new_worksheet.write(i+1,j,worksheet.cell_value(i+2, j))
        # 第二行第一列是总记忆的单词数
        new_worksheet.write(old_nrows-1, 0, value[0])
        # 第二行第二列是总共玩游戏的时长
        new_worksheet.write(old_nrows-1, 1, value[1])
        # 第二行第一列是总记忆的单词数
        new_worksheet.write(old_nrows-1, 2, value[2])
        # 第二行第二列是总共玩游戏的时长
        new_worksheet.write(old_nrows-1, 3, value[3])
    else:
        for i in range(4):
            # 第二行第一列是总记忆的单词数
            new_worksheet.write(old_nrows, i, value[i])

    # save file
    new_workbook.save(path)