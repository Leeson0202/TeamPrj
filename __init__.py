from scrapy.spider1 import *
from scrapy.spider2 import *
from scrapy.spider3 import *
from sql.in_sql import *
from requests import *
from watch.watch import  *
import time

header = {"user-agent": 'Mozilla/5.0'}  # 创建一个字段 浏览器5.0
url_head_1 = "https://www.koolearn.com"
url_head_2 = "http://www.iciba.com/word?w="
host = 'localhost'
port = 3306
user = 'root'
password =   '123456'
database = 'youdian'


class Vocabulary:
    # spell tag clearfix sentences分别为: str str 列表 词典
    def __init__(self, spell=None, tag=None, clearfix=None, sentences=None):
        self.spell = spell  # 单词的拼写
        self.tag = tag  # 四六级、高中
        self.clearfix = clearfix  # 词性和翻译
        self.sentence = sentences  # 单词的例句


def get_HTTP_response(url=None, params=None):
    """
    获取response并返回
    """
    if url:
        try:
            r = get(url, headers=header, params=params,
                    timeout=30)  # 伪装浏览器进行爬取
            r.raise_for_status()  # 自动检测爬虫状态=200
        except:
            return None
        r.encoding = 'utf-8'  # 转换格式
        return r  # 返回response
    else:
        return None


def MyBeautifulSoup(soup=None, rex=None):
    '''
    提取关键词 并返回给相应的函数
    '''

    if rex == 1:
        word_list = soup.find_all('a')
        word_list = [x.string for x in word_list]
        my_word_list = list()
        for i in word_list:
            x = ''
            for j in i:
                if (ord(j) < 91 and ord(j) > 40) or (ord(j) > 95 and ord(j) < 123) or ord(j) == 32 or ord(j) == 45:
                    x += j
                else:
                    break
            my_word_list.append(x)
        return my_word_list
    else:
        spell = tag = ''  # 初始化
        clearfixs = list()
        sentences = dict()
        word_box = None
        try:
            word_box = soup.find_all(
                name='div', attrs={"class": "FoldBox_fold__1GZ_2"})  # 找到 单词简介box
            if word_box:
                word_box = word_box[0]
                spell = word_box.find_all(
                    name='h1', attrs={"class": "Mean_word__3SsvB"})  # 找到单词拼写
                if (not spell):
                    spell = word_box.find_all(
                        name='h2', attrs={"class": "Mean_sentence__2NXAD"})  # 找到单词拼写

                tag = word_box.find_all(
                    name='p', attrs={"class": "Mean_tag__2vGcf"})  # 找到 标签 四六级
                if tag:  # 如果 有标签
                    tag = tag[0].text
                else:
                    tag = ''

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
                if sentences_box:  # 有例句则 提取出字典
                    sentences_e = sentences_box[0].find_all(
                        name='p', attrs={"class": "NormalSentence_en__3Ey8P"})  # 例句
                    sentences_c = sentences_box[0].find_all(
                        name='p', attrs={"class": "NormalSentence_cn__27VpO"})  # 例句翻译
                    if len(sentences_c) > 4:  # 提取并合成字典
                        sentences_e = [e.text for e in sentences_e[0:5]]
                        sentences_c = [c.text for c in sentences_c[0:5]]
                        sentences = dict(zip(sentences_e, sentences_c))
                    else:
                        sentences_e = [e.text for e in sentences_e]
                        sentences_c = [c.text for c in sentences_c]
                        sentences = dict(zip(sentences_e, sentences_c))
                else:
                    sentences = dict()
            return spell[0].text, tag, clearfixs, sentences
        except:
            return spell[0].text, tag, clearfixs, sentences


def word_sort(path):
    """
    词汇爬取后 进行去重 排序
    """
    lines = list()  # 初始化
    try:
        with open(path, 'r', encoding='utf-8') as ff:
            lines = ff.readlines()
            lines = list(set(x.strip() for x in lines))
            pass
    except:
        print('文件加载失败')
        return
    lines.sort()
    try:
        with open(path, "w", encoding='utf-8') as f:
            for i in lines:
                f.write(i + '\n')
        return
    except:
        return


def to_progress(id=0):
    """
    1. 根据id 进入不同的函数

    """
    if id == 1:  # ----爬取字母列表
        # url = url_head_1 + 'dict/zimu_' + chr(ord('a')) + '_1.html'  # 单个字母测试
        thread = list()
        for a in range(ord('a'), ord('z') + 1):
            url = url_head_1 + '/dict/zimu_' + \
                chr(a) + '_1.html'  # 生成一个字母的首url链接
            path = './datas/txt/' + chr(a) + '.txt'
            t = threading.Thread(
                target=spider_1, args=(url, path))  # 进入spider_1
            thread.append(t)
        for i in thread:
            i.start()
        i.join()
        exit()

    elif (id == 2):  # ----搜索词汇
        # spider3.spider3(word)
        pass

    elif (id == 3):  # ----重新搜索词汇详情
        for i in range(ord('a'), ord('a') + 1):
            path1 = './datas/txt/' + chr(i) + '.txt'
            path2 = './datas/json/' + chr(i) + '.json'
            start = time.time()
            spider_2(path1, path2, letter=chr(i), key_word='', start=start)
        print("------------单词爬取保存成功-------------")
        exit()

    elif (id == 4):  # ----继续搜索词汇详情
        a = 'a'
        key_word = 'A bed of roses'
        try:
            with open("./datas/daily/record.txt", 'r') as ff:  # 读取记录
                lines = ff.readlines()
            a, key_word = lines[0].strip(), lines[1].strip()  # 获取上次字母和单词位置
        except:
            to_progress(id=3)
            exit()
        for i in range(ord(a), ord('z') + 1):
            path1 = './datas/txt/' + chr(i) + '.txt'
            path2 = './datas/json/' + chr(i) + '.json'
            start = time.time()
            spider_2(path1, path2, letter=chr(i),
                     key_word=key_word, start=start)
        exit()
    elif(id == 5):
        for i in range(ord('a'), ord('z') + 1):
            path2 = './datas/json/' + chr(i) + '.json'
            in_sql(path2, host, port, user, password, database)
            print("\r  {}   导入成功".format(chr(i)))
        print("------------ mysql 录入成功 -------------")
        exit()
    elif(id == 6):
        for i in range(ord('a'), ord('z') + 1):
            path1 = './datas/json/' + chr(i) + '.json'
            path2 = './watch/json/new_' + chr(i) + '.json'
            watch(path1,path2)
            print("\r  {}   提取成功".format(chr(i)))
        print("------------ 提取完成 -------------")
        exit()

    else:
        exit()


def main():
    """
    主函数
    """
    while True:
        id = eval(input("""
1. 收集词汇表        2. 搜索词汇
3. 重新收集词汇详情  4.继续搜索词汇详情
5. 导入数据库        6.提取手表格式
0. 退出
请输入序号---------》"""))

        if id > 0:
            to_progress(id)  # 进入分进程函数
        else:
            return


if __name__ == '__main__':
    main()
