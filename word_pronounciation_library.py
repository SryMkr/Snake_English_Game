'''
 author SryMkr
 Date 2021.3.5
 the function of this library is for pronunciation
'''


# import package
import os
import urllib.request


# define youdao dictionary class
class youdao():
    # type = 0：US  type = 1：UK
    def __init__(self, word, type=1):
        # get the lowercase of the word
        word = word.lower()
        # get the UN or US accent
        self._type = type
        # get the word
        self._word = word

        # get file root path
        self._dirRoot = os.path.dirname(os.path.abspath(__file__))
        #if 0 == self._type:
        #    self._dirSpeech = os.path.join(self._dirRoot, 'Speech_US')  # 美音库
        #else:
        # get the path of pronunciation
        self._dirSpeech = os.path.join(self._dirRoot, 'Speech_EN')

        # 判断是否存在美音库
        #if not os.path.exists('Speech_US'):
            # 不存在，就创建
        #    os.makedirs('Speech_US')
        # EN_SOUND exist?
        if not os.path.exists('Speech_EN'):
            # if not, then create
            os.makedirs('Speech_EN')

        # get the pronouciation path
        #if 0 == self._type:
        #    self._dirSpeech = os.path.join(self._dirRoot, 'Speech_US')  # 美音库
        #else:
        # get the path of pronunciation
        self._dirSpeech = os.path.join(self._dirRoot, 'Speech_EN')  # 英音库

    # get the local path of pronunciation
    def _getWordMp3FilePath(self, word):
        # get the lowercase of word
        word = word.lower()
        self._word = word
        # get the word sound path
        self._fileName = self._word + '.mp3'
        # concatenate the word path
        self._filePath = os.path.join(self._dirSpeech, self._fileName)

        # word sound exist?
        if os.path.exists(self._filePath):
            # yes return path
            return self._filePath
        else:
            # no return  None

            return None

    # get the word url
    def _getURL(self):
        '''
        私有函数，生成发音的目标URL
        http://dict.youdao.com/dictvoice?type=0&audio=
        '''
        self._url = r'http://dict.youdao.com/dictvoice?type=' + str(
            self._type) + r'&audio=' + self._word

    # download the pronunciation
    def down(self):
        # get the lowercase of word
        self.word = self._word.lower()
        # check whether the word sound exist?
        tmp = self._getWordMp3FilePath(self.word)
        # if not
        if tmp is None:
            # get the download url
            self._getURL()
            # down load to target path
            urllib.request.urlretrieve(self._url, filename=self._filePath)
        # return the file path
        return self._filePath

