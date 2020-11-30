import json


with open("./datas/json/ss.json", 'r+') as ff:
    try:
        ff.seek(ff.seek(0,2)-2,0)
        if ff.read() =='[]':
            ff.seek(ff.seek(0,2)-1,0)
            ff.write('{}]')
        else:
            ff.seek(ff.seek(0,2)-1,0)
            ff.write(' ,{}]')
    except:
        pass


# file_data = ""
# with open(file, "r", encoding="utf-8") as f:
#     for line in f:
#         if old_str in line:
#             line = line.replace(old_str,new_str)
#         file_data += line
# with open(file,"w",encoding="utf-8") as f:
#     f.write(file_data)