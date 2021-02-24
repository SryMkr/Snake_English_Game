# author SryMkr
# date 2021.1.14
# This library is for Snake Body


# import package
from Other_library import *
from Snake_head_library import *


# create the body of snake
class Snake_body_Sprite(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            # set the snake moving direction is  left
            self.velocity = two_Variate(-1, 0)
            # record the time of last moving
            self.old_time = 0
            # snake is made of segments
            self.segments = list()

        # create the beginning snake
        def creat_snake(self):
            # create snake head sprite
            self.snake_head = MySprite_head()
            # load main picture
            self.snake_head.load_head_frames("Game_Pictures/Snake_head1.png", 30, 30, 2)
            # set position
            self.snake_head.x_coordinate = FRAME_WIDTH * 9
            self.snake_head.y_coordinate = FRAME_WIDTH * 15
            # get image surface
            self.snake_head.head_update(40)
            # add the image surface in to segments list
            self.segments.append(self.snake_head)

            #  sprite for separate head from alphabet
            snake_head1 = MySprite_head()
            snake_head1.load_head_frames("Game_Pictures/Snake_head.png", 30, 30, 2)
            snake_head1.x_coordinate = FRAME_WIDTH * 8
            snake_head1.y_coordinate = FRAME_WIDTH * 14
            # 将这个surface一个个放入到一个列表中，本质上还是自己创建的snake
            snake_head1.head_update(40)
            self.segments.append(snake_head1)

        # eating food
        def add_segment(self, alphabet_collision):
            # the index of last image surface
            last = len(self.segments) - 1
            # the direction of snake
            start_velocity = two_Variate(0, 0)
            # adding food according to snake moving direction
            if self.velocity.first_variate < 0:  # left
                start_velocity.variate_one = 30
            elif self.velocity.first_variate > 0:  # right
                start_velocity.variate_one = -30
            if self.velocity.second_variate < 0:   # up
                start_velocity.variate_two = 30
            elif self.velocity.second_variate > 0:  # down
                start_velocity.variate_two = -30
            # set x&y coordinate of food
            alphabet_collision.x_coordinate = self.segments[last].x_coordinate + start_velocity.first_variate
            alphabet_collision.y_coordinate = self.segments[last].y_coordinate + start_velocity.second_variate
            # adding to snake tail
            self.segments.append(alphabet_collision)

        # draw all image surfaces
        def draw(self, surface):
            # one by one
            for segment in self.segments:
                # pass surface coordinate
                surface.blit(segment.image, (segment.x_coordinate, segment.y_coordinate))

        # food and snake cannot overlap
        def snake_position(self, x_coordinates, y_coordinates):
            # get the positions of three food
            random_topleft_postions = []
            for i in range(len(x_coordinates)):
                random_topleft_postion = []
                random_topleft_postion.append(x_coordinates[i])
                random_topleft_postion.append(y_coordinates[i])
                random_topleft_postions.append(random_topleft_postion)
            # get the positions of snake segments
            snake_topleft_postions = []
            for segment in self.segments:
                snake_topleft_postion = []
                snake_topleft_postion.append(segment.x_coordinate)
                snake_topleft_postion.append(segment.y_coordinate)
                snake_topleft_postions.append(snake_topleft_postion)
            # return two lists
            return random_topleft_postions, snake_topleft_postions

        # snake moving
        def snake_moving(self, ticks, speed):
            # control moving by time
            # 200 the speed, change if you like
            if ticks > self.old_time + speed:
                # replace old time with current time
                self.old_time = ticks
                # pass x&y coordinate one by one except head
                for n in range(len(self.segments) - 1, 0, -1):
                    self.segments[n].x_coordinate = self.segments[n - 1].x_coordinate
                    self.segments[n].y_coordinate = self.segments[n - 1].y_coordinate
                # set snake head x&y coordinate
                self.segments[0].x_coordinate += self.velocity.first_variate * FRAME_WIDTH
                self.segments[0].y_coordinate += self.velocity.second_variate * FRAME_WIDTH

print('运行成功，请等待加载游戏')


