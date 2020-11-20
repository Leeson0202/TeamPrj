from sql.__init__  import *
import json
import time

#
# path = '../datas/json/b.json'
# host = 'localhost'
# port = 3306
# user = 'root'
# password = '123456'
# database = 'youdian'


def in_sql(path, host, port, user, password, database = None):
    """
    这里进入数据库 并进行操作
    """
    start = time.time()
    cursor = MySQLConnection(host, port, user, password, database)

    with open(path, 'r') as fp:
        content = json.load(fp)


    for index,i in enumerate(content):
        sentence = ';'.join(
            ["{}:{}".format(x, y) for x in i['sentence'].keys() for y in i['sentence'].values()]
        )
        if  not i['tag']:
            i['tag'] = '不常用'

        sql = """insert into word values(0,"{}","{}","{}","{}");""".format(pymysql.escape_string(i['spell']),
                                                                             pymysql.escape_string(i['tag']),
                                                                             pymysql.escape_string(''.join(i['clearfix'])),
                                                                             pymysql.escape_string(sentence))
        cursor.insert_table(sql)
        percent = index/len(content) *100
        end = time.time()
        print('\r{:>4.1f}%  {:>.1f}s  {}\t\t\t\t\t'.format(
            percent, end - start, i['spell']), end='')  # 显示进度


# in_sql(path, host, port, user, password, database)
