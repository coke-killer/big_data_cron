from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect, HttpResponse


def login_auto(request):
    return render(request, 'login.html')

def login_check(request):
    '''登录校验'''
    # 接收数据
    username = request.POST.get('username')
    password = request.POST.get('pwd')
    print(username)
    print(password)
    # return HttpResponse('OK')
    # #
    # # 校验数据
    if not all([username, password]):
        print('数据不完整')
        return render(request, 'login.html', {'errmsg':'数据不完整'})
    # 业务处理:登录校验
    user = authenticate(username=username, password=password)
    if user is not None:
        print('用户存在')
        # 用户名密码正确
        if user.is_active:
            print('用户已经激活')
            # 用户已激活
            # 记录用户的登录状态
            login(request, user)
            # 跳转到工程页面
            return HttpResponseRedirect(reverse('watch_dog_app:all_project', args=(1,)))

            # # pj_info = ProjectsInfo.objects.get(id=pj_id)
            # # # return render(request, 'watch_dog_app/select_projects.html', {'pj_info': pj_info})
            # # response = render(reverse('watch_dog_app:all_project',args=(1,)))  # HttpResponseRedirect
            # #
            #
            # # 判断是否需要记住用户名
            # remember = request.POST.get('remember')
            # if remember == 'on':
            #     # 记住用户名
            #     response.set_cookie('username', username, max_age=7*24*3600)
            # else:
            #     response.delete_cookie('username')
            # # 返回response
            # return response
            # # return HttpResponse('OK')
        else:
            # 用户未激活
            return render(request, 'login.html', {'errmsg':'账户未激活'})
    else:
        # 用户名或密码错误
        return render(request, 'login.html', {'errmsg':'用户名或密码错误'})