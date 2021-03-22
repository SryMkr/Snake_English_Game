'''
 author SryMkr
 date 2021.3.5
 the function of this library is to download pronunciation
    and phonetics before execute game

'''
import threading
from word_pronounciation_library import youdao
from words_phonetic_library import OxfordDictionary
from words_handling_library import read_taskwords_xls
import time


# 读取对应年级的单词
words_list, _ = read_taskwords_xls('words_pool/nine_grade/nine_grade_unknown.xls',108)


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




# download the phonetic alphabet
# extend threading.Thread
class myThread_PHO(threading.Thread):

    def __init__(self, threadID, words_list):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.words_list = words_list

    # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
    def run(self):
        # load pronunciation
        for i in range(len(self.words_list)):
            wp = OxfordDictionary(self.words_list[i],'phonetic_alphabet.xls')
            wp._getPho()
            time.sleep(0.1)


# 创建下载发音的线程，这个发音会存到发音文件夹，需要自己换一下位置
thread_pro = myThread(1, "Thread-1", words_list)
# load pronunciation
thread_pro.start()


# 创建下载音节线程
thread_pho = myThread_PHO(2, words_list)
# load pronunciation
thread_pho.start()




