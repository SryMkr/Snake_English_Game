# import package
# the function of this library is for pronunciation
import os
import requests
import re
from Other_library import save_pho


# phonetic class
class oxford():
    phoneticSpelling = ""

    def __init__(self, word):
        word = word.lower()  # 小写
        word = word.replace(" ", "_")
        self._word = word  # 单词

        # get file path
        self._dirRoot = os.path.dirname(os.path.abspath(__file__))
        self._dirSpeech = os.path.join(self._dirRoot, 'Words_phonetic')  # 英音库

        # file exist?
        if not os.path.exists('Words_phonetic'):
            # create if no
            os.makedirs('Words_phonetic')

        self._fileName = self._word + '.txt'
        self._filePath = os.path.join(self._dirSpeech, self._fileName)
    # get url
    def _getPho(self):
        # phonetic exist?
        if os.path.exists(self._filePath):
            # yes retuen
            return self._filePath
        else:
            # no download

            request = requests.get("https://en.oxforddictionaries.com/definition/" + self._word)
            html = request.text
            regularExpression = r'<span\s+class="phoneticspelling">/([^\/]*)/</span>'
            matchObject = re.search(regularExpression, html, re.I)
            if matchObject:
                if matchObject.group(1):
                    self.phoneticSpelling = matchObject.group(1)
            # save txt
            save_pho(self._filePath, self.phoneticSpelling)








