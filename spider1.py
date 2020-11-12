from __init__ import *
from bs4 import BeautifulSoup


url_head_1 = "https://www.koolearn.com"



def spider_1(url=None):
    word_list = list()   # 初始化 单词列表
    url_list = list()    # 初始化 url列表
    url_list.append(url)   # 进表
    ok = False          # 当前进度是否保存
    f_txt = open('./datas/txt/'+url[-8:-7]+'.txt', "w", encoding='utf-8')

    try:
        while url_list:  # 判断列表是否还有 url
            ok = False
            word_list = list()   # 单词列表清空
            print('\r',url_list[0],end='')    # 输出当前 url
            response = get_HTTP_response(url=url_list[0])   # 得到响应
            del url_list[0]  # 删除列表

            # -----------------------------------------------------------解析部分
            soup = BeautifulSoup(response.text, 'html.parser')   # 一锅汤

            box = soup.find_all(name='div', attrs={
                                "class": "word-box"})[0]  # 找到 单词 box
            word_list.extend(MyBeautifulSoup(box, rex=1)) # 获取单词列表

            f_txt.seek(0,2)
            for i in word_list[::-1]:
                f_txt.write(i+'\n')
            f_txt.flush()
            ok = True

            next = soup.find_all(
                name='a', attrs={"class": "next"})          # 查找 下一页

            if next and next[0].get('href'):    # 判断是否有下一页 有就添加到 url列表
                urlappend = url_head_1 + next[0].get('href') # 提取url
                url_list.append(urlappend)
            else:      # 没有下一页 退出
                break
    except Exception as error:
        print(error)
    finally:
        if ok:
            try:
                f_txt.seek(0, 2)
                for i in word_list[::-1]:
                    f_txt.write(i + '\n')
                f_txt.flush()
            except:
                print("保存失败")
