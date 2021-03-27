'''
author SryMkr
date 2021.3.26
final version of Snake English Game
'''

# 每个单词需要记录的数据基于大数据分析,然后给出合适的难度
# 因为每次位置都更新，所以只能保证这次更新位置不重复，但是不能保证，连续好几次更新位置不重复

# import packages
from Snake_body_library import *
from game_introducation import *
import time,datetime
from words_handling_library import *
from words_phonetic_library import get_word_pho
import pygame_menu


# get today's date
TODAY = datetime.date.today()
# game start time
t0 = time.perf_counter()
# played time
current_spent_words=0
# score got
current_score = 0
# words got
current_remembered_words=0
# review record list
review_list = [0,0,0,0]
# load history record
total_remembered_words,total_spent_words, highest_score, highest_words= \
    read_excel_game_record('saved_files/game_record.xls')
record_list = [total_remembered_words,total_spent_words,highest_score,highest_words]
# create two empty list for known words
words_list_known = []
task_words_known = []
# track correct spelling
spell_list = list()
# how may words to practice
train_words_number = 9
# how many words practiced?
words_number = 0
# 卡住的时候的一个时钟
fix_clock = 10
# 游戏运行了几次
exe_times = 0
# initialize some modules
pygame.init()
# set the width and height of window
screen = pygame.display.set_mode((FRAME_WIDTH * 27, FRAME_WIDTH * 24))
# set screen caption
pygame.display.set_caption("English Words Practice")
# show the Chinese fonts on the display
CHINESE_FONT = pygame.font.Font('Fonts/STKAITI.TTF', 36)
INTRO_FONT = pygame.font.Font('Fonts/STKAITI.TTF', 25)
# show other type of font on the display
OTHER_FONT = pygame.font.Font('Fonts/arial.ttf', 36)
PHONETIC_FONT = pygame.font.Font('Fonts/Lucida-Sans-Unicode.ttf', 36)

# save game record
def save_game_record():
    global total_spent_words,current_spent_words
    review_list = [str(TODAY), round(current_spent_words, 2), current_score, current_remembered_words]
    current_spent_words = (time.perf_counter() - t0) / 60
    total_spent_words += current_spent_words
    record_list[0] = total_remembered_words + current_remembered_words
    record_list[1] = total_spent_words
    write_excel_game_review('saved_files/game_review.xls', review_list)
    write_excel_game_record('saved_files/game_record.xls', record_list)
    delete_taskwords_xls(word_file_path, words_list_known)
    write_knownwords_xls(word_review_file_path, words_list_known, task_words_known)
    pygame.quit()
    sys.exit(0)


# initial
def game_init():
    # global variate
    global snake, alphabet,alphabet_group, snake_speed,background_music_setting,\
        tip_group,track_spelling_setting,words_list, task_words,\
        main_game_running, tip, wrong_words_num_setting,continuous_correct_alphabet,\
        words_phonetic_setting,tip_show_setting,train_words_num_setting,word_file_path,\
        phonetic_file_path,pronunciation_file_path,train_words_number,word_review_file_path

    # initialize snake
    snake = Snake_body_Sprite()
    snake.creat_snake()

    # correct alphabet sprite
    alphabet_group = pygame.sprite.Group()
    alphabet = MySprite_food()
    alphabet.load_multi_frames("Game_Pictures/NEW_AL1.png", FRAME_WIDTH, FRAME_WIDTH, 13)
    alphabet_group.add(alphabet)

    # 专门设置单词的菜单
    mytheme_fix = pygame_menu.themes.Theme(background_color=(0, 0, 0, 0), title_background_color=(0, 0, 0, 0))
    game_fix_menu = pygame_menu.Menu(400, 400, '', theme=mytheme_fix, menu_position=(80, 60))
    # 第一页的菜单，标题和内容都透明
    mytheme1 = pygame_menu.themes.Theme(background_color=(0, 0, 0, 0), title_background_color=(0, 0, 0, 0))
    game_first_mune = pygame_menu.Menu(400, 200, '', theme=mytheme1, menu_position=(65, 60))
    # 选择年级，这个在所有的都结束之后需要弄一下
    # 设置本次训练的单词个数
    train_words_num_setting = game_fix_menu.add_text_input('单词数(5-15): ', default='9', font_name='Fonts/STKAITI.TTF',
                                                           selection_color=(255, 0, 0), background_color=(0, 255, 0))

    grade_setting = game_fix_menu.add_selector('选择词库',[('三年级', screen), ('四年级', screen), ('五年级', screen), ('六年级', screen),
                                                    ('初一', screen), ('初二', screen), ('初三', screen)], font_name='Fonts/STKAITI.TTF',
                                                   selection_color=(255, 0, 0),background_color=(0, 255, 0))
    # 进入游戏
    game_fix_menu.add_button('进入游戏', game_first_mune, font_name='Fonts/STKAITI.TTF', background_color=(0, 255, 0),
                               selection_color=(255, 0, 0))

    # 第二页游戏设置里的菜单
    myimage = pygame_menu.baseimage.BaseImage('Game_Pictures/game_intro.jpg')
    mytheme = pygame_menu.themes.Theme(background_color=myimage, title_background_color=(0, 0, 0,0),
                                       title_font_color=(255, 0, 0))
    game_setting_mune = pygame_menu.Menu(FRAME_WIDTH * 24, FRAME_WIDTH * 27, '', theme=mytheme,menu_id='game_setting')

    # 设置干扰选项
    wrong_words_num_setting = game_setting_mune.add_text_input('干扰选项(1-3): ', default='1',
                                                               font_name='Fonts/STKAITI.TTF',
                                                               selection_color=(255, 0, 0))

    # 蛇的移动速度设置
    snake_speed = game_setting_mune.add_text_input('蛇的移动速度(100-500): ', default='200', font_name='Fonts/STKAITI.TTF',
                                                   textinput_id='snake_speed', selection_color=(255, 0, 0))
    # 有无字母追踪
    track_spelling_setting = game_setting_mune.add_selector('拼写追踪', [('YES', screen), ('NO', screen)],
                                                            font_name='Fonts/STKAITI.TTF', selection_color=(255, 0, 0))
    # 有无背景音乐
    background_music_setting = game_setting_mune.add_selector('背景音乐', [('YES', screen), ('NO', screen)],
                                                              font_name='Fonts/STKAITI.TTF',
                                                              selection_color=(255, 0, 0))
    # 有无提示
    tip_show_setting = game_setting_mune.add_selector('单词提示', [('YES', screen), ('NO', screen)],
                                                      font_name='Fonts/STKAITI.TTF', selection_color=(255, 0, 0))
    # 有无音节
    words_phonetic_setting = game_setting_mune.add_selector('单词音节', [('YES', screen), ('NO', screen)],
                                                      font_name='Fonts/STKAITI.TTF', selection_color=(255, 0, 0))
    # 保存设置，并返回上一级菜单
    game_setting_mune.add_button('保存并返回', pygame_menu.events.BACK,
                                                            font_name='Fonts/STKAITI.TTF', selection_color=(255, 0, 0))
    # 第一页菜单所展示的内容
    learn_mode=game_first_mune.add_button('开始游戏', main_game, font_name='Fonts/STKAITI.TTF', background_color=(0, 255, 0),
                               selection_color=(255, 0, 0))
    review_mode = game_first_mune.add_button('复习模式', main_game, True, font_name='Fonts/STKAITI.TTF',
                                             background_color=(0, 255, 0), selection_color=(255, 0, 0))
    game_first_mune.add_button('游戏设置',  game_setting_mune, font_name='Fonts/STKAITI.TTF',
                               background_color=(0, 255, 0), selection_color=(255, 0, 0))
    game_first_mune.add_button('游戏记录', game_record, screen, INTRO_FONT, font_name='Fonts/STKAITI.TTF',
                               background_color=(0, 255, 0), selection_color=(255, 0, 0))
    game_first_mune.add_button('游戏帮助', game_intro,screen,INTRO_FONT, font_name='Fonts/STKAITI.TTF', background_color=(0,255,0),selection_color=(255, 0, 0))
    game_first_mune.add_button('结束游戏', save_game_record, font_name='Fonts/STKAITI.TTF', background_color=(0,255,0),selection_color=(255, 0, 0))

    # play the background music
    game_audio("game_sound/bgm.wav", volumn=0.3, times=-1)
    game_bgp = pygame.image.load("Game_Pictures/Snake_Begin_UI.png").convert_alpha()
    game_bgp = pygame.transform.scale(game_bgp, (FRAME_WIDTH * 27, FRAME_WIDTH * 24))

    while True:
        screen.blit(game_bgp, (0, 0))
        if train_words_num_setting.get_selected_time():
            train_words_number = game_play_setting(train_words_num_setting)
        # 选择词库
            if grade_setting.get_value()[0][0] == '三年级':
                word_file_path = 'words_pool/three_grade/three_grade_unknown.xls'
                phonetic_file_path = 'Words_phonetic/three_grade/three_grade_phonetic.xls'
                pronunciation_file_path = 'Speech_EN/three_grade/'
                word_review_file_path = 'words_pool/three_grade/three_grade_known.xls'
            elif grade_setting.get_value()[0][0] == '四年级':
                word_file_path = 'words_pool/four_grade/four_grade_unknown.xls'
                phonetic_file_path = 'Words_phonetic/four_grade/four_grade_phonetic.xls'
                pronunciation_file_path = 'Speech_EN/four_grade/'
                word_review_file_path = 'words_pool/four_grade/four_grade_known.xls'
            elif grade_setting.get_value()[0][0] == '五年级':
                word_file_path = 'words_pool/five_grade/five_grade_unknown.xls'
                phonetic_file_path = 'Words_phonetic/five_grade/five_grade_phonetic.xls'
                pronunciation_file_path = 'Speech_EN/five_grade/'
                word_review_file_path = 'words_pool/five_grade/five_grade_known.xls'
            elif grade_setting.get_value()[0][0] == '六年级':
                word_file_path = 'words_pool/six_grade/six_grade_unknown.xls'
                phonetic_file_path = 'Words_phonetic/six_grade/six_grade_phonetic.xls'
                pronunciation_file_path = 'Speech_EN/six_grade/'
                word_review_file_path = 'words_pool/six_grade/six_grade_known.xls'
            elif grade_setting.get_value()[0][0] == '初一':
                word_file_path = 'words_pool/seven_grade/seven_grade_unknown.xls'
                phonetic_file_path = 'Words_phonetic/seven_grade/seven_grade_phonetic.xls'
                pronunciation_file_path = 'Speech_EN/seven_grade/'
                word_review_file_path = 'words_pool/seven_grade/seven_grade_known.xls'
            elif grade_setting.get_value()[0][0] == '初二':
                word_file_path = 'words_pool/eight_grade/eight_grade_unknown.xls'
                phonetic_file_path = 'Words_phonetic/eight_grade/eight_grade_phonetic.xls'
                pronunciation_file_path = 'Speech_EN/eight_grade/'
                word_review_file_path = 'words_pool/eight_grade/eight_grade_known.xls'
            elif grade_setting.get_value()[0][0] == '初三':
                word_file_path = 'words_pool/nine_grade/nine_grade_unknown.xls'
                phonetic_file_path = 'Words_phonetic/nine_grade/nine_grade_phonetic.xls'
                pronunciation_file_path = 'Speech_EN/nine_grade/'
                word_review_file_path = 'words_pool/nine_grade/nine_grade_known.xls'

            words_list, task_words = read_taskwords_xls(word_file_path,
                                                                train_words_number)
            continuous_correct_alphabet = built_spelling_dic(words_list, ALPHABET_LIST)

        events = pygame.event.get()
        if game_fix_menu.is_enabled():
            game_fix_menu.update(events)
            game_fix_menu.draw(screen)
        pygame.display.update()


# define pause and continue game
def checkquit(events):
    global pause,main_game_running
    for event in events:
        if event.type == pygame.QUIT :
            if game_over == False:
                save_game_record()
    keys_two = pygame.key.get_pressed()
    if keys_two[K_ESCAPE]:
        main_game_running=False
    elif keys_two[K_p]:
        pause = False
    elif keys_two[K_SPACE]:
        pause = True
    # the pronunciation of words
    elif keys_two[K_q]:
        word_pro = words_list[int(alphabet.current_word_number) - 1]
        pygame.mixer.music.load(pronunciation_file_path + word_pro +".mp3")
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play()


def main_game(review_mode =False):
    global highest_words,highest_score,task_words,exe_times,\
        pause,record_list,words_number,game_over,fix_clock,\
        current_score,current_spent_words,words_lock,continuous_correct_alphabet,\
        current_remembered_words,main_game_running,words_list,\
        phonetic_file_path,pronunciation_file_path,word_review_file_path

    # 蛇的移动速度
    snake_moving_speed = game_play_setting(snake_speed)
    # 背景音乐
    bgm = game_play_setting(background_music_setting)
    if bgm[0][0] == 'YES':
        pygame.mixer.stop()
        game_audio("game_sound/bgm.wav", volumn=0.3, times=-1)
    # mute the bgm
    elif bgm[0][0] == 'NO':
        pygame.mixer.stop()
    # 单词提示
    prompt_show = game_play_setting(tip_show_setting)
    # 拼写追踪
    track_spelling = game_play_setting(track_spelling_setting)

    # 有无音节
    word_phone=game_play_setting(words_phonetic_setting)
    wrong_letters_num = int(game_play_setting(wrong_words_num_setting))

    # 给以后复习模式用
    if review_mode==True and exe_times == 0:
        words_list, task_words = read_taskwords_xls(word_review_file_path, int(train_words_number))
        continuous_correct_alphabet = built_spelling_dic(words_list, ALPHABET_LIST)
    exe_times += 1
    if prompt_show[0][0] == 'YES':
        # create tip sprite
        tip_group = pygame.sprite.Group()
        tip = MySprite_food()
        tip.load_multi_frames("Game_Pictures/health.png", FRAME_WIDTH, FRAME_WIDTH, 1)
        tip_group.add(tip)

    # wrong alphabet sprite
    random_alphabet_group = pygame.sprite.Group()
    for i in range(wrong_letters_num):
        random_alphabet = MySprite_food()
        random_alphabet.load_multi_frames("Game_Pictures/NEW_AL1.png", FRAME_WIDTH, FRAME_WIDTH, 13)
        random_alphabet_group.add(random_alphabet)

    # game_over switch
    game_over = False
    # pause and play switch
    pause = False
    # 每次游戏重新开始计数的话，分数也要重新归零
    current_score = 0
    # 每次游戏重开，记住的单词数也要清0
    current_remembered_words = 0
    # conflict switch
    food_snake_conflict = False
    count = 0
    # track eating spelling
    eating_spelling = list()
    # 提示的计时工具
    tip_time = 0
    tip_show = False
    # have ued tip or not?
    tip_use = False
    write_button = False
    # 防止重复写
    game_over_buzz = True
    main_game_running = True
    while main_game_running:
        # game clock
        timer = pygame.time.Clock()
        # how many frames in 1S
        timer.tick(60)
        # get kinds of events
        events = pygame.event.get()
        checkquit(events)
        # update drawing paper every loop
        # it seems like replace the last picture with new picture
        screen.fill((255, 255, 255))
        # the total time of gameplay
        gameplay_time = pygame.time.get_ticks()
        record_list[2] = highest_score
        record_list[3] = highest_words

        # update records
        if current_score > int(highest_score):
            highest_score = current_score
        if current_remembered_words > int(highest_words):
            highest_words = current_remembered_words

        # once out of words, then game over
        if words_number == len(task_words) and game_over_buzz == True:
            words_number = 0
            game_over = True
            write_button = True

        # game pause
        if pause:
            # Pause BGM
            pygame.mixer.pause()
            print_text(CHINESE_FONT, 250, 300, '游戏暂停', color=(255, 0, 0))
            print_text(CHINESE_FONT, 185, 400, '请按[P]键开始游戏', color=(255, 0, 0))

        else:
            # Unpause BGM
            pygame.mixer.unpause()
            # get held keys
            keys = pygame.key.get_pressed()
            # Snake dead once contact walls
            x = snake.segments[0].x_coordinate // 30
            y = snake.segments[0].y_coordinate // 30
            # appear from other side when contact wall
            if x < 0:
                snake.segments[0].x_coordinate = 26 * 30
            elif x >= 27:
                snake.segments[0].x_coordinate = 0
            elif y < 6:
                snake.segments[0].y_coordinate = 23 * 30
            elif y >= 24:
                snake.segments[0].y_coordinate = 30 * 6
            # control the direction of snake
            # snake cannot move to opposite direction
            if x>=0 and x <= 27 and y >=6 and y <=24:
                if (keys[K_UP] or keys[K_w]) and snake.velocity.second_variate!=1:
                    snake.velocity = two_Variate(0, -1)
                elif (keys[K_DOWN] or keys[K_d]) and snake.velocity.second_variate!=-1:
                    snake.velocity = two_Variate(0, 1)
                elif (keys[K_LEFT] or keys[K_a]) and snake.velocity.first_variate!=1:
                    snake.velocity = two_Variate(-1, 0)
                elif (keys[K_RIGHT] or keys[K_d]) and snake.velocity.first_variate!=-1:
                    snake.velocity = two_Variate(1, 0)

            # control head
            snake_head_direction(snake, snake.velocity)
            snake.snake_head.head_update(gameplay_time, 100)

            # if not game over
            if not game_over:
                # whether food positions conflict with snake
                while not food_snake_conflict:
                    # 得到蛇头的坐标
                    snake_head_x_coordinate = snake.snake_head.x_coordinate
                    snake_head_y_coordinate = snake.snake_head.y_coordinate
                    # 在这里修改要添加字母的个数
                    x_position_list, y_position_list = food_random_position(snake_head_x_coordinate,snake_head_y_coordinate,wrong_letters_num+2)
                    food_position, snake_position = snake.snake_position(x_position_list, y_position_list)

                    for i in food_position:
                        # if not go on
                        if i not in snake_position:
                            count += 1
                        # if so, get new position
                        else:
                            count = 0
                            break
                    # all are not conflict the pass
                    if count == wrong_letters_num + 2:
                        food_snake_conflict = True
                # reset
                food_snake_conflict = False
                count = 0

                # snake moving
                snake.snake_moving(gameplay_time, snake_moving_speed)
                # all food update and keep
                if prompt_show[0][0] == 'YES':
                    tip.tip_update(1, 0, x_position_list, y_position_list)
                alphabet.target_update(continuous_correct_alphabet, 1, 0, x_position_list, y_position_list)

                # 保证出现字母不相同
                wrong_letters_image = [1, 1]
                while len(wrong_letters_image) !=len(set(wrong_letters_image)):
                    wrong_letters_postion = 2
                    wrong_letters_image.clear()
                    for sprite in random_alphabet_group.sprites():
                        sprite.random_update(alphabet.current_frame, 1+fix_clock, 0, x_position_list[wrong_letters_postion], y_position_list[wrong_letters_postion])
                        wrong_letters_postion += 1
                        wrong_letters_image.append(sprite.random_frame)
                    gameplay_time_one = pygame.time.get_ticks()
                    if gameplay_time_one > gameplay_time+1000:
                        fix_clock += 10
                #   if eat correct food
                if len(pygame.sprite.spritecollide(snake.segments[0], alphabet_group, False)) > 0:
                    # create a new sprite
                    current_frame = alphabet.current_frame
                    a = Snakebody_alphabet(current_frame)
                    # add food in spelling_list
                    spell_list.append(ALPHABET_LIST[current_frame])
                    # add food in eating list
                    eating_spelling.append(ALPHABET_LIST[current_frame])
                    # add to snake tail
                    snake.add_segment(a)
                    # food update
                    alphabet.target_update(continuous_correct_alphabet, gameplay_time + 1, 1, x_position_list,
                                           y_position_list)
                    # 保证出现位置不会重复
                    wrong_letters_image = [1, 1]
                    while len(wrong_letters_image) != len(set(wrong_letters_image)):
                        wrong_letters_postion = 2
                        wrong_letters_image.clear()
                        for sprite in random_alphabet_group.sprites():
                            sprite.random_update(alphabet.current_frame, gameplay_time + fix_clock, 10, x_position_list[wrong_letters_postion],
                                                 y_position_list[wrong_letters_postion])
                            wrong_letters_postion += 1
                            wrong_letters_image.append(sprite.random_frame)
                        fix_clock += 10
                    if prompt_show[0][0] == 'YES':
                        tip.tip_update(gameplay_time + 100, 100, x_position_list, y_position_list)
                    # right buzz
                    game_audio("game_sound/right.wav")
                    # score plus 10
                    current_score += 10

                #   if eat wrong food
                elif len(pygame.sprite.spritecollide(snake.segments[0], random_alphabet_group, False, False)) > 0:
                    collide_sprite=pygame.sprite.spritecollide(snake.segments[0], random_alphabet_group, False, False)
                    # wrong buzz
                    game_audio("game_sound/wrong.wav")
                    random_frame = collide_sprite[0].random_frame
                    # add food in eating list
                    eating_spelling.append(ALPHABET_LIST[random_frame])
                    b = wrong_alphabet(random_frame)
                    snake.add_segment(b)
                    # 保证出现位置不会重复
                    wrong_letters_image = [1, 1]
                    while len(wrong_letters_image) != len(set(wrong_letters_image)):
                        wrong_letters_postion = 2
                        wrong_letters_image.clear()
                        print(wrong_letters_image)
                        for sprite in random_alphabet_group.sprites():
                            sprite.random_update(alphabet.current_frame, gameplay_time + fix_clock, 10, x_position_list[wrong_letters_postion],
                                                 y_position_list[wrong_letters_postion])
                            wrong_letters_postion += 1
                            wrong_letters_image.append(sprite.random_frame)
                        fix_clock += 10
                    if prompt_show[0][0] == 'YES':
                        tip.tip_update(gameplay_time + 100, 100, x_position_list, y_position_list)
                    current_score -= 10

                #   if eat tip
                if prompt_show[0][0] == 'YES':
                    if len(pygame.sprite.groupcollide(snake.segments, tip_group, False, False)) > 0:
                        # print correct spelling of current task
                        tip_show = True
                        tip_time = gameplay_time
                        # 到蛇的第二个就开始消失计时
                        if  len(pygame.sprite.spritecollide(snake.segments[1], tip_group, False, False)) > 0:
                            # score -30
                            current_score -= 30
                            # tip update
                            tip.tip_update(gameplay_time + 100, 100, x_position_list, y_position_list)
                            # tip buzz
                            game_audio("game_sound/health.wav")

                # Snake dead once contact itself
                for n in range(1, len(snake.segments)):
                    if pygame.sprite.collide_rect(snake.segments[0], snake.segments[n]):
                        # game over and save records
                        game_over = True
                        write_button =True

        # if game over
        if game_over == True:
            if write_button == True:
                pygame.mixer.stop()
                # game over buzz
                game_audio("game_sound/game_over.wav")
                game_over_buzz = False
                # 每次游戏结束之后，要清除蛇后面的东西
                del snake.segments[2:]
                write_button = False

            game_over_image = pygame.image.load("Game_Pictures/game_intro.jpg").convert_alpha()
            game_over_image = pygame.transform.scale(game_over_image, (FRAME_WIDTH * 27, FRAME_WIDTH * 24))
            screen.blit(game_over_image, (0, 0))

            # print results after game over
            print_text(CHINESE_FONT, 0 * 0, 0, "学习结束")
            print_text(CHINESE_FONT, FRAME_WIDTH * 7, 0, "本轮完成: " + str(len(words_list_known)))
            print_text(CHINESE_FONT, FRAME_WIDTH*15, 0, "本轮得分: " + str(current_score))
            # show how many words player remembered in one round
            print_text(CHINESE_FONT, 0, FRAME_WIDTH*2, "已经学习到的单词如下：")
            print_result(OTHER_FONT, 0, FRAME_WIDTH*4, set(words_list_known[:]))

        else:
            # show tip
            if tip_show ==True:
                print_text(CHINESE_FONT, FRAME_WIDTH * 17, 60, "提示: " + words_list[int(alphabet.current_word_number) - 1],
                         color=(255, 0, 0))
                # flay us if you use tip
                tip_use = True
                # disappear after 1.5 second
                if gameplay_time > tip_time + 1500:
                    tip_show = False

            # print current state
            print_text(CHINESE_FONT, FRAME_WIDTH * 8, 0, "当前任务: " + task_words[int(alphabet.current_word_number) - 1])

            # set up whether there are phonetics or not
            if word_phone[0][0] == 'YES':
                pho_current_words = get_word_pho(phonetic_file_path, words_list[int(alphabet.current_word_number) - 1])
                print_text(PHONETIC_FONT, FRAME_WIDTH
                           * 17, 0, '/'+ pho_current_words+'/')
            print_text(CHINESE_FONT, 0, 0, "当前得分: " + str(current_score))
            print_text(CHINESE_FONT, FRAME_WIDTH * 20, FRAME_WIDTH*4, "剩余任务: " + str(len(task_words)-int(alphabet.current_word_number)+1))
            print_text(CHINESE_FONT, 0, FRAME_WIDTH * 2, "最高分数: " + str(int(highest_score)))
            print_text(CHINESE_FONT, 0, FRAME_WIDTH * 4, "单词记录: " + str(int(highest_words)))

            # 刚刚拼写完成的单词
            if int(alphabet.current_word_number) > 1:
                print_text(CHINESE_FONT, FRAME_WIDTH * 8, FRAME_WIDTH * 4, "刚完成: " + words_list[int(alphabet.current_word_number) - 2])
            else:
                print_text(CHINESE_FONT, FRAME_WIDTH * 8, FRAME_WIDTH * 4, "刚完成: " + '    ')

            # show the process of spelling of current word
            if track_spelling[0][0] == 'YES':
                for i in range(len(spell_list)):
                    print_text(OTHER_FONT, FRAME_WIDTH * (i + 8), FRAME_WIDTH * 2, spell_list[i], color=(255, 0, 0))
            if ''.join(spell_list) == words_list[int(alphabet.current_word_number) - 2]:
                # delete if do not make mistake and do not use tip
                if ''.join(eating_spelling) == words_list[int(alphabet.current_word_number) - 2] and tip_use == False:
                    del snake.segments[-len(spell_list):]
                # record word from words_list if do not make mistake
                    if words_list[int(alphabet.current_word_number) - 2] not in words_list_known:
                        words_list_known.append(words_list[int(alphabet.current_word_number) - 2])
                        task_words_known.append(task_words[int(alphabet.current_word_number) - 2])
                    current_remembered_words += 1
                # clear the two list once task change
                eating_spelling.clear()
                words_number += 1
                spell_list.clear()
                tip_use = False
            # draw lines
            pygame.draw.line(screen, (0, 0, 0), (0, FRAME_WIDTH * 6), (FRAME_WIDTH * 27, FRAME_WIDTH * 6), 1)
            pygame.draw.line(screen, (0, 0, 0), (0, FRAME_WIDTH * 4), (FRAME_WIDTH * 27, FRAME_WIDTH * 4), 1)
            pygame.draw.line(screen, (0, 0, 0), (0, FRAME_WIDTH * 2), (FRAME_WIDTH * 27, FRAME_WIDTH * 2), 1)
            pygame.draw.line(screen, (0, 0, 0), (FRAME_WIDTH*8-10, 0), (FRAME_WIDTH*8-10, FRAME_WIDTH * 6), 1)

            # draw all sprites
            snake.draw(screen)
            random_alphabet_group.draw(screen)
            alphabet_group.draw(screen)

            # set up whether there are prompts or not
            if prompt_show[0][0] == 'YES':
                tip_group.draw(screen)
            # draw grid
            for i in range(0,27,1):
                vertical_line = pygame.Surface((1, 540), pygame.SRCALPHA)
                vertical_line.fill((0, 0, 0, 20))
                screen.blit(vertical_line, (FRAME_WIDTH * i, FRAME_WIDTH * 6))
            for i in range(7,24,1):
                horizontal_line = pygame.Surface((810, 1), pygame.SRCALPHA)
                horizontal_line.fill((0, 0, 0, 20))
                screen.blit(horizontal_line, (0,FRAME_WIDTH * i))

        # draw all sprites
        pygame.display.update()


game_init()
