import threading
from word_pronounciation_library import *
from words_phonetic_library import *
import time


#为了下载音频所以需要创建线程来单独下载单词的发音


class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name, words_list):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.words_list = words_list


    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        # load pronunciation
        for i in range(len(self.words_list)-1):
            sp = youdao(self.words_list[i])
            sp.down()
        time.sleep(0.1)




class myThread_PHO(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name, words_list):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.words_list = words_list

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        # load pronunciation
        for i in range(len(self.words_list)):
            wp = oxford(self.words_list[i])
            wp._getPho()
            time.sleep(0.1)





