from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json, hashlib

from login.models import User


# Create your views here.
@csrf_exempt
def login(request):
    if request.session.get('is_login', None):
        id = request.session.get('user_id')
        pw = request.session.get('user_pw')
        try:
            user = User.objects.filter(phone=id, password=pw)
            text = {'tx': '已经登录', 'isOK': 'OK', 'username': user[0].username,
                    'email': user[0].email, 'phone': user[0].phone,
                    'word_num': user[0].word_num, 'false_word': user[0].false_word}
            return HttpResponse(status=200, content=json.dumps(text), content_type='application/json')
        except Exception as e:
            text = {'tx': '服务器发生错误', 'isOK': 'NO'}
            return HttpResponse(status=500, content=json.dumps(text), content_type='application/json')

    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        try:
            user = User.objects.filter(phone=phone, password=hash_code(password))
            if user:
                request.session['is_login'] = True
                request.session['user_id'] = user[0].phone
                request.session['user_pw'] = user[0].password
                text = {'tx': '登录成功', 'isOK': 'OK', 'phone': user[0].phone, 'username': user[0].username,
                        'email': user[0].email, 'word_num': user[0].word_num, 'false_word': user[0].false_word}
                return HttpResponse(status=200, content=json.dumps(text), content_type='application/json')
            else:
                text = {'tx': '登录失败,无此用户', 'isOK': 'NO'}
                return HttpResponse(status=403, content=json.dumps(text), content_type='application/json')
        except Exception as e:
            text = {'tx': '服务器发生错误', 'isOK': 'NO'}
            return HttpResponse(status=500, content=json.dumps(text), content_type='application/json')


@csrf_exempt
def register(request):
    if request.session.get('is_login', None):
        text = {'tx': '登录状态下不能注册', 'isOK': 'NO'}
        return HttpResponse(content=json.dumps(text), content_type='application/json', status=302)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        try:
            if User.objects.filter(phone=phone).exists():
                text = {'tx': '手机号重复', 'isOK': 'NO'}
                return HttpResponse(status=300, content_type='application/json', content=json.dumps(text))
            else:
                User.objects.create(username=username, password=hash_code(password), email=email, phone=phone)
                text = {'tx': '注册成功', 'isOK': 'OK'}
                return HttpResponse(status=200, content=json.dumps(text), content_type='application/json')
        except Exception as e:
            print(e)
            text = {'tx': '服务器发生错误', 'isOK': 'NO'}
            return HttpResponse(status=500, content=json.dumps(text), content_type='application/json')


# @csrf_exempt
# def get_info(request):
#    if request.method == 'POST':
#        phone = request.POST.get('phone')
#        try:
#            user = User.objects.get(phone=phone)
#           text = {'tx': '请求成功', 'username': user.username, 'phone': user.phone,
#                    'email': user.email, 'password': user.password,
#                    'word_num': user.word_num, 'false_word': user.false_word}
#            return HttpResponse(status=200, content=json.dumps(text), content_type='application/json')
#        except Exception as e:
#            text = {'tx': '服务器发生错误', 'isOK': 'NO'}
#            return HttpResponse(status=500, content=json.dumps(text), content_type='application/json')


def logout(request):
    if request.session.get('is_login', None):
        try:
            request.session.flush()
            text = {'tx': '退出登录成功', 'isOK': 'OK'}
            return HttpResponse(content=json.dumps(text), content_type='application/json', status=200)
        except Exception as e:
            text = {'tx': '服务器发生错误', 'isOK': 'NO'}
            return HttpResponse(status=500, content=json.dumps(text), content_type='application/json')


def hash_code(s, salt='youdian'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()
