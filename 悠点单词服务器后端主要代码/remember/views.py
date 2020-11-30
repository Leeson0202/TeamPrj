from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json, re
from remember.models import word
from login.models import User
from django.core import serializers


# Create your views here.


@csrf_exempt
def select(request):
    '''
    选择需要记忆的单词模块
    '''
    if request.method == 'POST':
        try:
            tag = request.POST.get('tag')
            word_list = word.objects.filter(tag__icontains=tag).values()
            word_data = list(word_list)

            # [dict(index=x) for index, x in enumerate(word_list)]
            # for index, line in enumerate(word_list):
            #   word_data[index+1] = line

            text = {'word': word_data, 'isOK': 'OK', 'tx': '获取成功'}
            return HttpResponse(content=json.dumps(text), content_type='application/json', status=200)
        except Exception as e:
            print(e)
            text = {'tx': '服务器发生错误', 'isOK': 'NO'}
            return HttpResponse(status=500, content=json.dumps(text), content_type='application/json')


@csrf_exempt
def add(request):
    '''
    增加词汇量，斩功能触发
    '''
    if request.method == 'POST':
        phone = request.POST.get('phone')
        try:
            user = User.objects.get(phone=phone)
            user.word_num = int(user.word_num) + 1
            user.save()
            text = {'tx': '增加词汇成功', 'isOK': 'OK'}
            return HttpResponse(status=200, content=json.dumps(text), content_type='application/json')
        except Exception as e:
            text = {'tx': '服务器发生错误', 'isOK': 'NO'}
            return HttpResponse(status=500, content=json.dumps(text), content_type='application/json')


@csrf_exempt
def false(request):
    '''
    记录用户易错的单词（错上两次以上触发）
    '''
    if request.method == 'POST':
        phone = request.POST.get('phone')
        false_word = request.POST.get('false_word')
        try:
            user = User.objects.get(phone=phone)
            if not re.search(false_word, user.false_word):
                user.false_word = str(user.false_word) + ';' + false_word
                user.save()
                text = {'tx': '记录成功', 'isOK': 'OK'}
                return HttpResponse(status=200, content=json.dumps(text), content_type='application/json')
            else:
                text = {'tx': '记录重复，不需反复提交', 'isOK': 'OK'}
                return HttpResponse(status=200, content=json.dumps(text), content_type='application/json')
        except Exception as e:
            print(e)
            text = {'tx': '服务器发生错误', 'isOK': 'NO'}
            return HttpResponse(status=500, content=json.dumps(text), content_type='application/json')


@csrf_exempt
def get_word(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        try:
            wd = word.objects.get(id=id)
            tx = {'tx': '获取单词成功', 'isOK': 'OK', 'word_id': wd.id, 'word_spell': wd.spell, 'word_tag': wd.tag,
                  'word_sentence': wd.sentence,
                  'word_clearfix': wd.clearfix}
            return HttpResponse(status=200, content=json.dumps(tx), content_type='application/json')
        except Exception as e:
            print(e)
            text = {'tx': '服务器发生错误', 'isOK': 'NO'}
            return HttpResponse(status=500, content=json.dumps(text), content_type='application/json')


@csrf_exempt
def get_word_id(request):
    if request.method == 'POST':
        tag = request.POST.get('tag')
        try:
            word_list = word.objects.filter(tag__icontains=tag)
            s = str(word_list[0].id)
            for line in word_list:
                if s == str(line.id):
                    pass
                else:
                    s = s + ',' + str(line.id)
            text = {'id': s, 'tx': '获取成功', 'isOK': 'OK'}
            return HttpResponse(status=200, content=json.dumps(text), content_type='application/json')
        except Exception as e:
            print(e)
            text = {'tx': '服务器发生错误', 'isOK': 'NO'}
            return HttpResponse(status=500, content=json.dumps(text), content_type='application/json')
