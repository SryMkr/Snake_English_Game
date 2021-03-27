'''
author SryMkr
date: 2021.3.13
the function of this library is for words' phonetics
有时候单词比较多会不下载，但是也不是找不到的原因，闹不清楚
最好的办法就是我们已经下载好了，尽量减少网络的还有机器的依赖
'''

# import packages
import os
import requests
import re
from xlutils.copy import copy
import xlrd


# write content into excel.xls  format: list[word,phonetic]
def write_excel_xls_append(path, value):
    # get the len of value
    index = len(value)
    # open a workbook
    workbook = xlrd.open_workbook(path)
    # get all sheet names
    sheets = workbook.sheet_names()
    # get the first sheet
    worksheet = workbook.sheet_by_name(sheets[0])
    # get the rows of sheet
    rows_old = worksheet.nrows
    # copy the workbook
    new_workbook = copy(workbook)
    # get the first worksheet
    new_worksheet = new_workbook.get_sheet(0)
    for i in range(0, index):
            # column always is 0 and 1 第一列写单词 第二列写发音
            new_worksheet.write(rows_old, i, value[i])
    # save file 覆盖原文件
    new_workbook.save(path)


# check whether the words in excel.xls
def read_excel_xls(path,word):
    # open workbook
    workbook = xlrd.open_workbook(path)
    # get all sheets by sheet names
    sheets = workbook.sheet_names()
    # get the first sheet
    worksheet = workbook.sheet_by_name(sheets[0])
    # get the correspond content
    words = worksheet.col_values(0)
    # if word in words
    if word in words:
        return True
    else:
        return False


# phonetic alphabet class
class OxfordDictionary():

    # initialize empty string
    phoneticSpelling = ""

    # create directory for phonetic
    def __init__(self, word, filename):
        # convert to lowercase word
        word = word.lower()
        # move space
        self._word = word.strip()
        # filename
        self._fileName = filename
        # get the absolute current path
        self._dirRoot = os.path.dirname(os.path.abspath(__file__))
        # concatenate the file path
        self._dirSpeech = os.path.join(self._dirRoot, 'Words_phonetic')

        # file exist?
        if not os.path.exists('Words_phonetic'):
            # create if no
            os.makedirs('Words_phonetic')

        # get the filename path
        self._filePath = os.path.join(self._dirSpeech, self._fileName)

    # get the download url
    def _getPho(self):
        # phonetic exist?
        if read_excel_xls(self._filePath,self._word):
            # yes pass
            pass
        # no download
        else:
            list = []
            list.append(self._word)
            # get the url
            request = requests.get("https://en.oxforddictionaries.com/definition/" + self._word)
            # convert the whole content to text
            html = request.text
            # locate the target content
            regularExpression = r'<span\s+class="phoneticspelling">/([^\/]*)/</span>'
            # scan all content and return the first matched content with ignoring the l_u case letter
            matchObject = re.search(regularExpression, html, re.I)
            # if get
            if matchObject:
                # if phonetic exist
                if matchObject.group(1):
                    self.phoneticSpelling = matchObject.group(1)
                else:
                    self.phoneticSpelling = None
            # make the list format
            list.append(self.phoneticSpelling)
            # write into the excel.xls
            write_excel_xls_append(self._filePath, list)


# get the word phonetic in excel.xls
def get_word_pho(path,word):
    # open workbook
    workbook = xlrd.open_workbook(path)
    # get all sheets by sheet names
    sheets = workbook.sheet_names()
    # get the first sheet
    worksheet = workbook.sheet_by_name(sheets[0])
    # get the correspond content
    words = worksheet.col_values(0)
    # if word in words
    if word in words:
        # return the word index
        word_index = words.index(word)
        # return the phonetic
        return worksheet.cell_value(word_index, 1)
    else:
        return None