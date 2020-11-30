from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from login.models import User
from info.models import Info
import json


# Create your views here.


@csrf_exempt
def edit_info(request):
    '''
    增加(修改)激励语（个性签名）
    '''
    if request.method == 'POST':
        phone = request.POST.get('phone')
        info = request.POST.get('info')
        try:
            user = User.objects.get(phone=phone)
            if not user.user_info:
                user.user_info = Info.objects.create(scripts=info)
                user.save()
                text = {'tx': '修改个性签名成功', 'isOK': 'OK', 'scripts': user.user_info.scripts}
                return HttpResponse(status=200, content=json.dumps(text), content_type='application/json')
            else:
                u_info = Info.objects.get(id=user.user_info_id)
                u_info.scripts = info
                u_info.save()
                text = {'tx': '修改个性签名成功', 'isOK': 'OK', 'scripts': info}
                return HttpResponse(status=200, content=json.dumps(text), content_type='application/json')
        except Exception as e:
            print(e)
            text = {'tx': '服务器出现错误', 'isOK': 'NO'}
            return HttpResponse(status=500, content=json.dumps(text), content_type='application/json')
