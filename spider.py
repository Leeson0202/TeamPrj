from os import error
from requests import *
from bs4 import BeautifulSoup
import json
from spider1 import *
from spider2 import *
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



def get_HTTP_response(url=None, params=None):
    if url:
        try:
            r = get(url, headers=header, params=params,
                    timeout=30)  # 伪装浏览器进行爬取
            r.raise_for_status()                     # 自动检测爬虫状态=200
            r.encoding = 'utf-8'         # 转换格式
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
        word_spell = Mean_tag__2vGcf = ''    # 初始化
        clearfixs = list()
        sentences = dict()
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
                else:
                    Mean_tag__2vGcf = ''

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
                else:
                    sentences = dict()
            return word_spell[0].text, Mean_tag__2vGcf, clearfixs, sentences
        except:
            return word_spell[0].text, Mean_tag__2vGcf, clearfixs, sentences


def word_sort(path):
    lines = list()  # 初始化
    try:
        with open(path,'r', encoding='utf-8') as ff:
            lines = ff.readlines()
            lines = list(set(x.strip() for x in lines))
            pass
    except :
        print('文件加载失败')
        return
    lines.sort()
    try:
        with open(path, "w", encoding='utf-8') as f:
            for i in lines:
                f.write(i+'\n')
        print("保存成功")
    except:
        print("保存失败")
        return
        




def main():
    # url = url_head_1 + 'dict/zimu_' + chr(ord('a')) + '_1.html'  # 单个字母测试
    # for a in range(ord('a'), ord('z') + 1):
    #     # url = url_head_1 + '/dict/zimu_' + chr(a) + '_1.html'     # 生成一个字母的首url链接
    #     # # print(url)
    #     # spider_1(url)     # 进入spider_1
    #     # ---------------------------------去重排序算法
    #     path = './datas/txt/'+chr(a)+'.txt'
    #     word_sort(path=path)

    for a in range(ord('a'), ord('z') + 1):
        path1 = './datas/txt/' + chr(a) + '.txt'
        path2 = './datas/json/' + chr(a) + '.json'
        spider_2(path1, path2)


if __name__ == '__main__':
    main()
