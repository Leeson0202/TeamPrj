from spider import *

url_head_2 = "http://www.iciba.com/word?w="



def spider_2(path1=None, path2=None):

    dictionary = list()
    word_list = list()   # 初始化单词列表
    try:
        with open(path1, 'r', encoding="utf-8") as f:  # 读取字母文件
            word_list = f.readlines()
    except :
        print("文件不存在")

    for word in word_list:
        word = word.strip()  # 消去单词两端的空格

        if not word:
            continue
        print(word)
        url = url_head_2 + word  # 对应单词的url

        # url = 'http://www.iciba.com/word?w=AMIDS'
        response = get_HTTP_response(url=url)
        if response:
            word_spell = Mean_tag__2vGcf =  ''  # 初始化变量
            clearfixs = list()
            sentences = dict()

            soup = BeautifulSoup(response.text, 'html.parser')  # 一锅汤
            box = soup.find_all(name='div', attrs={
                                "class": "Content_center__3EE2R"})[0]   # 划小区域
            if box.ul:   # 如果这个盒子存在 提取具体信息 否则下一个单词
                word_spell, Mean_tag__2vGcf, clearfixs, sentences = MyBeautifulSoup(
                    soup=box.ul, rex=2)
                if not word_spell:  # 如果提取失败 下一个单词
                    continue

            else: 
                continue

            dictionary.append(vocabulary(
                word_spell, Mean_tag__2vGcf, clearfixs, sentences))
        else:
            continue

    dictionary_list = list()
    for x in dictionary:
        dictionary_list.append(dict(x))
    
    
    dictionary_json = json.dumps(dictionary_list)
    with open(path2, 'w') as f:
        f.writelines(dictionary_json)
        print("保存成功")
