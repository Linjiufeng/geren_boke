from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.http import HttpResponse
import json
from django.core import serializers

# Create your views here.
def index(request):
    return render(request, "index1.html")

def login(request):
    if request.method == "GET":
        # 获取请求源地址，没有的话，则获取"/",存session中
        url = request.META.get("HTTP_REFERER", "/")
        request.session['url'] = url
        # print("GET_url", url)
        # 先判断session中是否有登录信息
        # print("session", request.session['id'], request.session['uphone'])
        if 'id' in request.session and 'uphone' in request.session:
            # 如果有则从哪来回哪去
            # print("来自于session有登录信息")
            return redirect(url)
        else:
            # 否则继续判断cookie中是否有登录信息
            if 'id' in request.COOKIES and 'uphone' in request.COOKIES:
                # 如果有，则取出来判断
                id = request.COOKIES['id']
                uphone = request.COOKIES['uphone']
                users = Users.objects.filter(id=id, uphone=uphone)
                if users:
                    # 如果正确则保存进Session,并从哪来回哪去
                    request.session['id']=id
                    request.session['uphone']=uphone
                    # print("来自cookie的正确数据")
                    return redirect(url)
                else:
                    # 如果不正确，先删除cookies中原有的值，再回到首页
                    # 构建响应对象并删除cookie的值再返回
                    form = LoginForm()
                    resp = render(request, "login.html", {'form': form})
                    resp.delete_cookie('id')
                    resp.delete_cookie('uphone')
                    # print("来自cookie的不正确数据")
                    return resp
            else:
                # 如果没有，则去登录页面
                # 创建LoginForm()并交给login.html
                form = LoginForm()
                # print("来自cookie无登录信息")
                return render(request, 'login.html', locals())

        # 创建LoginForm()并交给login.html
        form = LoginForm()
        # print("来自于session有无登录信息")
        return render(request, "login.html", locals())
    else:
        # 获取手机号码和密码，验证登录
        uphone = request.POST['uphone']
        upwd = request.POST['upwd']
        users = Users.objects.filter(uphone=uphone, upwd=upwd)
        # 成功：向下执行
        if users:
            # 将id和uphone保存进session
            request.session['id'] = users[0].id
            request.session['uphone'] = uphone
            # 从session中获取源地址
            url = request.session['url']

            # print("POST_url", url)
            resp = redirect(url)
            # 判断是否记住密码(保存进cookie)
            if 'savepwd' in request.POST:
                expire = 60*60*24*365
                resp.set_cookie("id", users[0].id, expire)
                resp.set_cookie('uphone', uphone, expire)
            # 从哪来回哪去
            return resp
        # 失败：回到首页
        else:
            form = LoginForm()
            return render(request, 'login.html', locals())

def cart(request):
    return render(request, "cart.html")

def register(request):
    # 判断请求方式
    # get:盾register.html
    # post:处理请求提交的数据
    if request.method == "GET":
        return render(request, "register.html")
    else:
        # post请求处理
        # 获取uphone的内容，并判断是否存在
        uphone = request.POST["uphone"]
        users = Users.objects.filter(uphone=uphone)
        if users:
            # uphone已经存在
            return render(request, "register.html", {"errMsg": "手机号码已存在"})
        else:
            # 将前端数据取出来赋值给users
            users = Users()
            users.uphone = uphone
            users.upwd = request.POST["upwd"]
            users.uemail = request.POST['uemail']
            users.uname = request.POST['uname']
            # 将users保存进数据库
            # 成功去往首页，失败的话则给出提示
            try:
                users.save()
                return redirect('/')
            except Exception as ex:
                print(ex)
                return render(request,'register.html',{'errMsg':'请联系管理员'})

def register_post(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        # 1.获取前端传递过来的uphone
        uphone = request.POST.get("uphone")
        # 获取uphone的内容，并判断是否存在
        # print("uphone", uphone)
        users = Users.objects.filter(uphone=uphone)
        # print("users", users)
        if users:
            # uphone已经存在
            return HttpResponse("该用户已存在，请重新输入")
        else:
            return HttpResponse("通过")

# 有关登录用户检查的业务逻辑处理
def check_login(request):
    # 判断session中是否有登录信息(id,uphone)
    if "id" in request.session and 'uphone' in request.session:
        id = request.session.get('id')
        uname = Users.objects.get(id=id).uname
        dic = {
            "loginStatus": 1,
            "uname": uname,
        }
    else:
        dic = {
            "loginStatus": 0,
        }
    return HttpResponse(json.dumps(dic))

def type_goods(request):
    all_lst = []
    # 先查询所有的GoodsType信息，再循环遍历得到每个goodstype
    types = GoodsType.objects.all()
    for type in types:
        # type表示的是每个商品类型
        # 将type转换成json的串
        type_json = json.dumps(type.to_dict())
        # 获取type对应的所有的商品
        g_lst = type.goods_set.all()
        # 将g_lst转换成json串
        g_lst_json = serializers.serialize('json', g_lst)
        # 将type_json和g_lst_json封闭到字典中
        dic = {
            'type': type_json,
            'goods': g_lst_json,
        }
        all_lst.append(dic)
    return HttpResponse(json.dumps(all_lst))