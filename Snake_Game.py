# author SryMkr
# date 2021.2.23
# second version of Snake English Game


# import packages
from Snake_food_library import *
from Snake_body_library import *
from Snake_head_library import *
from thread import *
import sys

# tip
words_list,words_list_known = read_words_pool('words_pool/words_pool.txt')
# Chinese tasks
task_words,task_words_known = read_wordTra_pool('words_pool/words_tra_pools.txt')

# snake_speed
snake_moving_speed = 200


# 创建新线程
thread_pro = myThread(1, "Thread-1", words_list)
thread_pro.daemon = True
# load pronunciation
thread_pro.start()

# 创建新线程
thread_pho_1 = myThread_PHO(2, "Thread-2", words_list[:2])
# load pronunciation
thread_pho_1.start()
thread_pho_1.join()

# 创建新线程
thread_pho = myThread_PHO(3, "Thread-3", words_list[2:])
# load pronunciation
thread_pho.daemon = True
thread_pho.start()


# get sequence correct alphabet
continuous_correct_alphabet = built_spelling_dic(words_list, ALPHABET_LIST)


# add correct  alphabet
class Snakebody_alphabet(MySprite_food):
    def __init__(self, frame_nuber):
        MySprite_food.__init__(self)
        self.load_multi_frames("Game_Pictures/NEW_AL1.png", FRAME_WIDTH, FRAME_WIDTH, 13)
        self.draw_current_frame(frame_nuber)


# add wrong alphabet
class wrong_alphabet(MySprite_food):
    def __init__(self, frame_nuber):
        MySprite_food.__init__(self)
        self.load_multi_frames("Game_Pictures/NEW_AL1.png", FRAME_WIDTH, FRAME_WIDTH, 13)
        self.draw_current_frame(frame_nuber)



# initial
def game_init():
    # global variate
    global screen, OTHER_FONT,CHINESE_FONT, \
        timer, snake, alphabet_group, \
        alphabet, random_alphabet, \
        random_alphabet_group, tip_group, tip,PHONETIC_FONT

    # initialize some modules
    pygame.init()
    # set the width and height of window
    # it seems like a drawing board
    screen = pygame.display.set_mode((FRAME_WIDTH * 27, FRAME_WIDTH * 24))
    # set screen caption
    pygame.display.set_caption("Snake English")
    # hide mouse
    pygame.mouse.set_visible(False)
    # show the Chinese on the display
    CHINESE_FONT = pygame.font.SysFont('华文楷体', 36)
    # show other type of font on the display
    OTHER_FONT = pygame.font.SysFont('arial', 36)
    PHONETIC_FONT = pygame.font.Font('Fonts/Lucida-Sans-Unicode.ttf', 36)
    # game clock
    timer = pygame.time.Clock()
    # initialize snake
    snake = Snake_body_Sprite()
    snake.creat_snake()



    # correct alphabet sprite
    alphabet_group = pygame.sprite.Group()
    alphabet = MySprite_food()
    alphabet.load_multi_frames("Game_Pictures/NEW_AL1.png", FRAME_WIDTH, FRAME_WIDTH, 13)
    alphabet_group.add(alphabet)

    # wrong alphabet sprite
    random_alphabet_group = pygame.sprite.Group()
    random_alphabet = MySprite_food()
    random_alphabet.load_multi_frames("Game_Pictures/NEW_AL1.png", FRAME_WIDTH, FRAME_WIDTH, 13)
    random_alphabet_group.add(random_alphabet)

    # create tip sprite
    tip_group = pygame.sprite.Group()
    tip = MySprite_food()
    tip.load_multi_frames("Game_Pictures/health.png", FRAME_WIDTH, FRAME_WIDTH, 1)
    tip_group.add(tip)

    # play the bgm
    game_audio("game_sound/bgm.wav",times=-1)

# other constant
game_init()
# game_over switch
game_over = False
# pause and play switch
pause = False
# conflict switch
food_snake_conflict = False
count = 0
# record score
current_score = 0
# track correct spelling
spell_list = list()

# track eating spelling
eating_spelling = list()
# 提示的计时工具
tip_time = 0
tip_show = False
tip_use = False
write_button = False
# define pause and continue game
def checkquit(events):
    global pause
    for event in events:
        if event.type == pygame.QUIT:
            # save record
            save_record('saved_files/highest_words', highest_words)
            save_record('saved_files/highest_score', highest_score)
            write_words_pool('words_pool/words_pool.txt', words_list, words_list_known)
            write_wordTra_pool('words_pool/words_tra_pools.txt', task_words, task_words_known)
            sys.exit(0)
    keys_two = pygame.key.get_pressed()
    if keys_two[K_ESCAPE]:
        # save record
        save_record('saved_files/highest_words', highest_words)
        save_record('saved_files/highest_score', highest_score)
        write_words_pool('words_pool/words_pool.txt', words_list, words_list_known)
        write_wordTra_pool('words_pool/words_tra_pools.txt', task_words, task_words_known)
        sys.exit(0)

    elif keys_two[K_p]:
        pause = False
    elif keys_two[K_SPACE]:
        pause = True
    elif keys_two[K_q]:
        word_pro = words_list[int(alphabet.current_word_number) - 1]
        pygame.mixer.music.load("Speech_EN/" + word_pro +".mp3")
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play()

try:
  while True:

    # how many frames in 1S
    timer.tick(200)
    # update drawing paper every loop
    # it seems like replace the last picture with new picture
    screen.fill((255, 255, 255))
    # the total time of gameplay
    gameplay_time = pygame.time.get_ticks()

    # load record
    highest_score = load_record('saved_files/highest_score')
    highest_words = load_record('saved_files/highest_words')



    # update records
    if current_score > int(highest_score):
        highest_score = current_score
    if int(alphabet.current_word_number) - 1 > int(highest_words):
        highest_words = int(alphabet.current_word_number) - 1

    # once out of words, then game over
    if int(alphabet.current_word_number) == len(task_words):
        game_over = True
        write_button = True
    # get kinds of events
    events = pygame.event.get()
    checkquit(events)

    if pause:
        # Pause BGM
        pygame.mixer.pause()
        # show the words once game suspended
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
                # get the position of three sprires
                # 产生的坐标不许和蛇头在一个坐标轴上
                snake_head_x_coordinate = snake.snake_head.x_coordinate
                snake_head_y_coordinate = snake.snake_head.y_coordinate
                x_position_list, y_position_list = food_random_position(snake_head_x_coordinate,snake_head_y_coordinate)
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
                if count == 3:
                    food_snake_conflict = True
            # reset
            food_snake_conflict = False
            count = 0

            # snake moving
            snake.snake_moving(gameplay_time, snake_moving_speed)

            # all food update and keep
            tip.tip_update(1, 0, x_position_list, y_position_list)
            alphabet.target_update(continuous_correct_alphabet, 1, 0, x_position_list, y_position_list)
            random_alphabet.random_update(alphabet.current_frame, 1, 0, x_position_list, y_position_list)

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
                random_alphabet.random_update(alphabet.current_frame, gameplay_time + 1, 1, x_position_list,
                                              y_position_list)
                tip.tip_update(gameplay_time + 100, 100, x_position_list, y_position_list)
                # right buzz
                game_audio("game_sound/right.ogg")

                # score plus 10
                current_score += 10
                # spell switch
                spell_switch = True

            #   if eat wrong food
            elif len(pygame.sprite.spritecollide(snake.segments[0], random_alphabet_group, False, False)) > 0:

                # wrong buzz
                game_audio("game_sound/wrong.ogg")
                random_frame = random_alphabet.random_frame

                # add food in eating list
                eating_spelling.append(ALPHABET_LIST[random_frame])
                b = wrong_alphabet(random_frame)
                snake.add_segment(b)
                random_alphabet.random_update(alphabet.current_frame, gameplay_time + 10, 10, x_position_list,
                                              y_position_list)
                tip.tip_update(gameplay_time + 100, 100, x_position_list, y_position_list)
                current_score -= 10
            #   if eat tip
            if len(pygame.sprite.groupcollide(snake.segments, tip_group, False, False)) > 0:
                # print correct spelling of current task
                tip_show = True
                tip_time = gameplay_time
                # once snake tail leave tip
                if pygame.sprite.spritecollideany(snake.segments[-1], tip_group, False):
                    # score -30
                    current_score -= 30
                    # tip update
                    tip.tip_update(gameplay_time + 100, 100, x_position_list, y_position_list)
                    # tip buzz
                    game_audio("game_sound/health.ogg")


            # Snake dead once contact itself
            for n in range(1, len(snake.segments)):
                if pygame.sprite.collide_rect(snake.segments[0], snake.segments[n]):
                    # game over and save records
                    game_over = True
                    write_button =True
                    save_record('saved_files/highest_words', highest_words)
                    save_record('saved_files/highest_score', highest_score)


    # fi game over
    if game_over == True:
        if write_button == True:
            write_words_pool('words_pool/words_pool.txt', words_list, words_list_known)
            write_wordTra_pool('words_pool/words_tra_pools.txt',task_words,task_words_known)
            write_button = False
            # stop backgroud music
            pygame.mixer.stop()
            # game over buzz
            game_audio("game_sound/game_over.ogg")


        backbuffer = pygame.Surface((screen.get_rect().width, screen.get_rect().height))
        backbuffer.fill((255, 0, 0))
        screen.blit(backbuffer, (0, 0))

        # print results after game over
        print_text(CHINESE_FONT, 0 * 0, 0, "学习结束")
        print_text(CHINESE_FONT, FRAME_WIDTH * 7, 0, "本轮完成: " + str(int(alphabet.current_word_number) - 1))
        print_text(CHINESE_FONT, FRAME_WIDTH*15, 0, "本轮得分: " + str(current_score))
        # show how many words player remembered in one round
        print_text(CHINESE_FONT, 0, FRAME_WIDTH*2, "已经学习到的单词如下：")
        print_result(OTHER_FONT, 0, FRAME_WIDTH*4, words_list_known[:])
        print_result(CHINESE_FONT, 0, FRAME_WIDTH * 6, task_words_known[:])
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
        pho_current_words = load_pho('Words_phonetic/'+ words_list[int(alphabet.current_word_number) - 1]+'.txt')
        print_text(PHONETIC_FONT, FRAME_WIDTH * 17, 0, '/'+ pho_current_words+'/')
        print_text(CHINESE_FONT, 0, 0, "当前得分: " + str(current_score))
        print_text(CHINESE_FONT, FRAME_WIDTH * 20, FRAME_WIDTH*4, "剩余任务: " + str(len(task_words)-int(alphabet.current_word_number)))
        print_text(CHINESE_FONT, 0, FRAME_WIDTH * 2, "最高分数: " + str(highest_score))
        print_text(CHINESE_FONT, 0, FRAME_WIDTH * 4, "单词记录: " + str(highest_words))
        if int(alphabet.current_word_number) > 1:
            print_text(CHINESE_FONT, FRAME_WIDTH * 8, FRAME_WIDTH * 4, "刚完成: " + words_list[int(alphabet.current_word_number) - 2])
        else:
            print_text(CHINESE_FONT, FRAME_WIDTH * 8, FRAME_WIDTH * 4, "刚完成: " + '    ')

        # current task spelling
        current_spell = words_list[int(alphabet.current_word_number) - 1]
        # print tip until snake tail
        current_spell_len = len(current_spell)

        # show the process of spelling of current word
        for i in range(len(spell_list)):
            print_text(OTHER_FONT, FRAME_WIDTH * (i + 8), FRAME_WIDTH * 2, spell_list[i], color=(255, 0, 0))
        if ''.join(spell_list) == words_list[int(alphabet.current_word_number) - 2]:
            # delete if do not make mistake and do not use tip
            if ''.join(eating_spelling) == words_list[int(alphabet.current_word_number) - 2] and tip_use == False:

                del snake.segments[-len(spell_list):]
            # record word from words_list if do not make mistake
                words_list_known.append(words_list[int(alphabet.current_word_number) - 2])
                task_words_known.append(task_words[int(alphabet.current_word_number) - 2])
            # clear the two list once task change
            eating_spelling.clear()
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
        tip_group.draw(screen)
        # 画表格
        for i in range(0,27,1):
            vertical_line = pygame.Surface((1, 540), pygame.SRCALPHA)
            vertical_line.fill((0, 0, 0, 20))  # You can change the 100 depending on what transparency it is.
            screen.blit(vertical_line, (FRAME_WIDTH * i, FRAME_WIDTH * 6))

        for i in range(7,24,1):
            horizontal_line = pygame.Surface((810, 1), pygame.SRCALPHA)
            horizontal_line.fill((0, 0, 0, 20))  # You can change the 100 depending on what transparency it is.
            screen.blit(horizontal_line, (0,FRAME_WIDTH * i))

    # draw all sprites
    pygame.display.update()
except:
    save_record('saved_files/highest_words', highest_words)
    save_record('saved_files/highest_score', highest_score)
    write_words_pool('words_pool/words_pool.txt', words_list, words_list_known)
    write_wordTra_pool('words_pool/words_tra_pools.txt', task_words, task_words_known)
    sys.exit(0)