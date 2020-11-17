from __init__ import *
import __init__
import json
import threading
from bs4 import BeautifulSoup
import time

url_head_2 = "http://www.iciba.com/word?w="

threadlock = threading.Lock()

def handle(word, letter, percent, f_json, f_record, f_error, start):
    """
    :param word: 单词
    :param letter:  字母
    :return:  None

    """
    url = url_head_2 + word  # 对应单词的url
    # url = 'http://www.iciba.com/word?w=AMIDS'
    response = __init__.get_HTTP_response(url=url)
    if not response:  # 否则下一个单词
        f_error.seek(0, 2)
        f_error.write(word + ' 1\n')
        f_error.flush()
        return
    else:

        soup = __init__.BeautifulSoup(response.text, 'html.parser')  # 一锅汤
        box = soup.find_all(name='div', attrs={
            "class": "Content_center__3EE2R"})[0]  # 划小区域
        if not box.ul:  # 如果这个盒子不存在 下一个单词 ；  否则提取具体信息
            f_error.seek(0, 2)
            f_error.write(word + ' 2\n')
            f_error.flush()
            return
        else:
            spell, tag, clearfixs, sentences = __init__.MyBeautifulSoup(
                soup=box.ul, rex=2)  # 进入spider 提取详细单词信息
            if not spell:  # 如果提取失败 下一个单词
                return
            else:
                theword = __init__.Vocabulary(
                    spell, tag, clearfixs, sentences)  # 创建单词对象
                word_detail = json.dumps(theword.__dict__)  # 将单词对象 转化为json格式

                # -----------------------------------------------储存数据
                save(word_detail, letter, word,
                     percent, f_json, f_record, start)

def save(word_detail, letter, word, percent, f_json, f_record, start):
    pass
    threadlock.acquire()  # 加个同步锁就好了
    ok = 0
    try:
        f_json.seek(f_json.seek(0, 2) - 2, 0)  # 文件指针移动到最后一个
        if f_json.read() == '[]':  # 判断 是否为空
            f_json.seek(f_json.seek(0, 2) - 1, 0)
            f_json.write(word_detail + ']')
            ok = 1
        else:  # 不为空
            f_json.seek(f_json.seek(0, 2) - 1, 0)
            f_json.write(',\n' + word_detail + ']')
            ok = 1

    except:
        pass
    finally:
        f_json.flush()
        if ok == 1:  # 记录对应的日志 用于下一次继续爬取
            f_record.seek(0)
            f_record.truncate()  # 清空
            try:
                f_record.writelines(letter + '\n' + word + '\n')
            except Exception as e:
                print(e)

            f_record.flush()
    end = time.time()
    print('\r{:>3.0f}%  {:>.1f}s  {}\t\t\t\t\t'.format(
        percent, end - start, word), end='')  # 显示进度
    threadlock.release()


threads = []


def spider_2(path1=None, path2=None, letter=None, key_word=None, start=None):
    """
    1. 读取文件 获得每个单词并对单词进行strip处理
    2. 判断 是否从上次位置继续爬取
    2. 获取response 并判断是否存在 
    3. 一锅汤 处理提取信息
    4. 处理信息后 储存到本地的json文件
    5. 如果单词保存成功就记录日志

    """

    word_list = list()  # 初始化单词列表
    try:
        with open(path1, 'r', encoding="utf-8") as f:  # 读取 字母.txt 文件
            word_list = f.readlines()
    except:
        print("文件不存在")
        return  # 没有文件则返回

    f_json = open(path2, 'r+')
    f_error = open("./datas/daily/errors.txt", 'r+')
    f_record = open('./datas/daily/record.txt', 'w')

    index = 0  # 本来是从0开始
    if key_word:  # 判断 是否从上次位置继续爬取
        i = 0
        for i, myword in enumerate(word_list):
            if myword.strip() == key_word.strip():
                index = i + 1  # 如果找到下一个单词 记录下标
                break
        if i == len(word_list):
            index = 0
    else:  # 否则初始化json文件 重新爬取
        f_json.truncate()  # 清空
        f_json.writelines('[]')  # 初始化 并保持
        f_json.flush()
        if letter == 'a':
            f_error.truncate()  # 清空
            f_error.flush()
    word_list = word_list[index:]

    # ----------------------------------------------------------------------开始爬取详情部分:
    if len(word_list)>0:
        for i, word in enumerate(word_list):
            percent = (i / len(word_list)) * 100  # 进度百分比
            word = word.strip()  # 消去单词两端的空格
            if not word:
                continue
            # handle(path2, word, letter,percent)

            t = threading.Thread(target=handle, args=(
                word, letter, percent, f_json, f_record, f_error, start))
            threads.append(t)
        num = 50  # 设置的线程数
        t = None
        for i, t in enumerate(threads):
            while len(threading.enumerate()) > num:
                pass
            try:
                t.start()
            except:
                pass
        t.join()
        f_json.close()
        f_error.close()
        f_record.close()
    else:
        return
