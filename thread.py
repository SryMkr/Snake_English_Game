import threading
from MyGame.word_pronounciation_library import *
import requests
import re



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

class myThread_PHO(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name, words_list):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.words_list = words_list
        self.pho_list = []

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        # load pronunciation
        for i in range(len(self.words_list)):
            word = self.words_list[i]
            word = word.replace(" ", "_")
            phoneticSpelling = ""

            # url的格式有规律
            request = requests.get("https://en.oxforddictionaries.com/definition/" + word)
            html = request.text
            # 查看网页发现音标所处的行HTML格式有规律 使用正则表达式描述
            regularExpression = r'<span\s+class="phoneticspelling">/([^\/]*)/</span>'

            matchObject = re.search(regularExpression, html, re.I)

            if matchObject:
                if matchObject.group(1):
                    phoneticSpelling = matchObject.group(1)
                else:
                    print("\nword \"" + word + "\" has no phonetic spelling in the dictionary")
            else:
                print("\nword \"" + word + "\" has no phonetic spelling in the dictionary")
            self.pho_list.append(phoneticSpelling)
    def get_result(self):
        return self.pho_list






