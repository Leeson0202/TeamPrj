# TeamPrj
薪火杯
运行此软件需要安装的包
beautifsoup4、json、requests、pymysql


最外层__init__.py 文件为启动文件且为核心文件


数据库：
Drop databases youdian;
create databases youdian;

数据表格格式：
create table word(
id int unsigned not null primary key auto_increment,
spell varchar(255) not null,
tag varchar(128) default null,
clearfix varchar(1000) not null,
sentence text
);


json文件格式：
[
{"spell": "a", "tag": "CTE4", "clearfix": ["n.\u68d8\u624b\u7684\u95ee\u9898"], "sentence": {"However, the dollar is a hot potato, tasteless but wasteful to discard.": "\u4f46\u662f, \u73b0\u5728\u7684\u7f8e\u5143\u662f\u70eb\u624b\u7684\u5c71\u828b, \u98df\u4e4b\u65e0\u5473,\u5f03\u4e4b\u53ef\u60dc.", "If I were you, I'd drop that client a hot potato.": "\u5047\u5982\u6211\u662f\u4f60\u7684\u8bdd, \u6211\u5c31\u628a\u90a3\u4e2a\u96be\u4ee5\u5e94\u4ed8\u7684\u987e\u5ba2\u9a6c\u4e0a\u7529\u6389.", "He dropped the topic like a hot potato.": "\u4ed6\u653e\u5f03\u4e86\u8fd9\u4e2a\u68d8\u624b\u7684\u8bdd\u9898.", "Consequently the brain drain has become a hot potato which needs to solve.": "\u4eba\u624d\u6d41\u5931\u95ee\u9898\u5df2\u6210\u4e3a\u5c71\u897f\u90ae\u653f\u4e9f\u5f85\u89e3\u51b3\u7684\u91cd\u8981\u95ee\u9898.", "Steve: It'sure is. If you were broke, she'd drop you like a hot potato.": "\u53f2\u8482\u592b: \u5f53\u7136\u554a! \u5982\u679c\u4f60\u53e3\u888b\u6ca1\u94b1\u4e86, \u4f60\u5c31\u4f1a\u50cf\u70eb\u624b\u5c71\u828b\u4e00\u6837\u88ab\u5979\u7529\u6389."}},
{"spell": "a bed of roses", "tag": "CTE4", "clearfix": ["\u79f0\u5fc3\u5982\u610f\u7684\u5883\u9047"], "sentence": {"It's to be remembered that life is not a bed of roses.": "\u5e94\u5f53\u8bb0\u4f4f,\u751f\u6d3b\u4e2d\u5e76\u4e0d\u662f\u4e00\u5207\u90fd\u90a3\u4e48\u5982\u610f\u7684.", "We all knew that life was unlikely to be a bed of roses back in England.": "\u6211\u4eec\u90fd\u77e5\u9053\u56de\u5230\u82f1\u683c\u5170\u4ee5\u540e\u7684\u751f\u6d3b\u4e0d\u592a\u53ef\u80fd\u5e78\u798f\u5b8c\u7f8e\u3002", "Marriage is not always a bed of roses.": "\u5a5a\u59fb\u5e76\u4e0d\u603b\u662f\u79f0\u5fc3\u5982\u610f\u7684.", "A coal miner's work is not a bed of roses.": "\u7164\u77ff\u5de5\u4eba\u7684\u6d3b\u8ba1\u53ef\u4e0d\u8f7b\u677e.", "Life in Tokyo is far from a bed of roses.": "\u5728\u4e1c\u4eac\u751f\u6d3b\u51b3\u4e0d\u662f\u751f\u6d3b\u5728\u6e29\u67d4\u5bcc\u8d35\u4e61."}}
]
