from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

# 登录
from apps.shop.models import User, ShopCar


# cookie
# session
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('name')
        password= request.POST.get('password')
        # 判断用户名和密码不能为空
        if username and password:
            users = User.objects.filter(name=username)
            if users:
                user = users.first()
                if user.password == password:
                    # 表示登录成功
                    # 查询用户购车的商品数
                    count = user.shopcar_set.count()
                    userinfo = {
                        'uid': user.uid,
                        'name': user.name,
                        'count': count,
                    }
                    # request.session.setdefault('uid', str(user.uid))
                    # request.session.setdefault('name', user.name)
                    # request.session.setdefault('count', str(count))
                    request.session['userinfo'] = userinfo
                    return redirect('/shop/index')
                else:
                    return render(request, 'login.html', {'msg': '用户名或密码错误'})
            else:
                # 用户不存在
                return render(request, 'login.html', {'msg': '用户不能存在'})
        else:
            return render(request, 'login.html', {'msg': '用户名或密码不能为空'})
            # 用户密码不能为空
    else:
        return render(request, 'login.html', {'msg': '错误请求方式!'})


def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        users = User.objects.filter(name=username)
        if users:
            return render(request, 'register.html', {'msg': '用户名已存在'})
        else:
            if password != password2:
                return render(request, 'register.html', {'msg': '前后密码输入不一致'})
            else:
                user = User()
                user.name = username
                user.password = make_password(password)
                user.save()
                return render(request, 'account/register_success_page.html')
    else:
        return render(request, 'register.html', {'msg': '请求方式错误'})


def loginout(request):
    del request.session['userinfo']
    return redirect('/shop/index/')
