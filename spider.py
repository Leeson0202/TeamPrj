from requests import *
from bs4 import BeautifulSoup
import json
import re
import os
import time

header = {"user-agent": 'Mozilla/5.0'}           # 创建一个字段 浏览器5.0
url_head_1 = "https://www.koolearn.com"
url_head_2 = "http://www.iciba.com/word?w="


class vocabulary:
    # clearfix为一个列表 sentences 为一个元组
    def __init__(self, word_spell=None, Mean_tag__2vGcf=None, clearfix=None, sentences=None):
        self.word_spell = word_spell     # 单词的拼写
        self.Mean_tag__2vGcf = Mean_tag__2vGcf  # 四六级、高中
        self.clearfix = clearfix        # 词性和翻译
        self.sentence = sentences    # 单词的例句

    def keys(self):
             #当对实例化对象使用dict(obj)的时候, 会调用这个方法,这里定义了字典的键, 其对应的值将以obj['name']的形式取,
                # 但是对象是不可以以这种方式取值的, 为了支持这种取值, 可以为类增加一个方法'''
        return ('word_spell', 'Mean_tag__2vGcf', 'clearfix','sentence')

    def __getitem__(self, item):
        '''内置方法, 当使用obj['name']的形式的时候, 将调用这个方法, 这里返回的结果就是值'''
        return getattr(self, item)



def get_HTTP_response(url=None, params=None):
    if url:
        try:
            r = get(url, headers=header, params=params,
                    timeout=30)  # 伪装浏览器进行爬取
            r.raise_for_status()                     # 自动检测爬虫状态=200
            r.encoding = r.apparent_encoding         # 转换格式
            return r  # 返回response
        except:
            print("响应失败")
    else:
        return


def MyBeautifulSoup(soup=None, rex=None):
    if rex == 1:
        word_list = soup.find_all('a')
        return [x.string for x in word_list]
    else:
        word_spell = Mean_tag__2vGcf = clearfixs = sentences = None   # 初始化
        word_box = None
        try:
            word_box = soup.find_all(
                name='div', attrs={"class": "FoldBox_fold__1GZ_2"})  # 找到 单词简介box
            if word_box:
                word_box = word_box[0]
                word_spell = word_box.find_all(
                    name='h1', attrs={"class": "Mean_word__3SsvB"})  # 找到单词拼写
                if (not word_spell):
                    word_spell = word_box.find_all(
                        name='h2', attrs={"class": "Mean_sentence__2NXAD"})  # 找到单词拼写

                Mean_tag__2vGcf = word_box.find_all(
                    name='p', attrs={"class": "Mean_tag__2vGcf"})   # 找到 标签 四六级
                if Mean_tag__2vGcf:  # 如果 有标签
                    Mean_tag__2vGcf = Mean_tag__2vGcf[0].text

                Mean_part = word_box.find_all(
                    name='ul', attrs={"class": "Mean_part__1RA2V"})  # 找到 词性 及 翻译
                if Mean_part:
                    clearfixs = [x.text for x in Mean_part[0].contents]
                else:
                    Mean_part = word_box.find_all(
                        name='h3', attrs={"class": "Mean_title__2BwLF"})  # 找到 词性 及 翻译
                    if Mean_part:
                        clearfixs = Mean_part[0].nextSibling.contents[0]

                sentences_box = soup.find_all(
                    name='div', attrs={"class": "SceneSentence_scene__1Dnz6"})  # 找到 例句box
                if sentences_box:
                    sentences_e = sentences_box[0].find_all(
                        name='p', attrs={"class": "NormalSentence_en__3Ey8P"})  # 例句
                    sentences_c = sentences_box[0].find_all(
                        name='p', attrs={"class": "NormalSentence_cn__27VpO"})  # 例句翻译
                    sentences = {
                        e.text: c.text for e in sentences_e[0:4] for c in sentences_c[0:4]}
            return word_spell[0].text, Mean_tag__2vGcf, clearfixs, sentences
        except:
            return word_spell[0].text, Mean_tag__2vGcf, clearfixs, sentences


def spider_2(path1=None,path2 = None):
    dictionary = list()
    with open(path1, 'r', encoding="utf-8") as f:  # 读取字母文件
        word_list = f.readlines()
    for word in word_list:
        word = word.strip()
        print(word)
        url = url_head_2 + word

        # dictionary = list()
        # url = 'http://www.iciba.com/word?w=AMIDS'
        response = get_HTTP_response(url=url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            box = soup.find_all(name='div', attrs={
                                "class": "Content_center__3EE2R"})[0]
            word_spell = Mean_tag__2vGcf = clearfixs = sentences = None
            if box.ul:
                word_spell, Mean_tag__2vGcf, clearfixs, sentences = MyBeautifulSoup(
                    soup=box.ul, rex=2)
            dictionary.append(vocabulary(
                word_spell, Mean_tag__2vGcf, clearfixs, sentences))
            # try:
            #     print(dictionary[-1].Mean_tag__2vGcf,dictionary[-1].clearfix[0])
            # except:
            #     pass
    dictionary_list= list()
    for x in dictionary:
        dictionary_list.append(dict(x))
        
        # dictionary_list.append(globals()['{}'.format(x.woed_spell)] = {})
        pass
    dictionary_json = json.dumps(dictionary_list)
    with open(path2,'w') as f:
        f.writelines(dictionary_json)
        print("保存成功")
        

def spider_1(url=None):
    word_list = list()   # 初始化 单词列表
    url_list = list()    # 初始化 url列表
    url_list.append(url)   # 进表

    while url_list:  # 判断列表是否还有 url
        print(url_list[0])    # 输出当前 url
        response = get_HTTP_response(url=url_list[0])   # 得到响应
        del url_list[0]  # 删除列表
        # 解析部分
        soup = BeautifulSoup(response.text, 'html.parser')   # 一锅汤
        box = soup.find_all(name='div', attrs={
                            "class": "word-box"})[0]  # 找到 单词 box
        word_list.extend(MyBeautifulSoup(box, rex=1))                  # 获取单词列表
        next = soup.find_all(
            name='a', attrs={"class": "next"})          # 查找 下一页
        if next and next[0].get('href'):    # 判断是否有下一页 有就添加到 url列表
            urlappend = url_head_1 + next[0].get('href')
            url_list.append(urlappend)
        else:      # 没有下一页 排序 保存到txt文件
            try:
                with open('./datas/txt/'+url[-8:-7]+'.txt', "w", encoding='utf-8') as f:
                    for i in word_list[::-1]:
                        f.write(i+'\n')
                print("保存成功")
            except:
                print("保存失败")
            break


def main():
    # for a in range(ord('a'), ord('z') + 1):
    #     # url = url_head_1 + 'dict/zimu_' + chr(ord('a')) + '_1.html'  # 单个字母测试
    #     url = url_head_1 + '/dict/zimu_' + chr(a) + '_1.html'     # 生成一个字母的首url链接
    #     # print(url)
    #     spider_1(url)     # 进入spider_1

    for a in range(ord('a'), ord('z') + 1):
        path1 = './datas/txt/' + chr(a) + '.txt'
        path2 = './datas/json/' + chr(a) + '.json'
        spider_2(path1,path2)


if __name__ == '__main__':
    main()
