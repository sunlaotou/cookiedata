from django.shortcuts import render ,HttpResponse ,redirect
from  app01.models import *
# Create your views here.
def login(request):
    if request.method =="POST":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        # print (user,pwd)
        use = User.objects.filter(user=user,pwd=pwd).first()
        # print(use)
        if use:
            respone = HttpResponse("登陆成功")
            respone.set_cookie("is_login",True ) #超时时间 max_age=2
            import datetime
            # data = datetime.datetime(year=2018,month=10) "expires= data"
            respone.set_cookie("username", use.user,path="/index/")  , """expires默认None ,cookie失效的实际日期/时间  浏览器只会把cookie回传给带有该路径的页面，这样可以避免将
                                                 cookie传给站点中的其他的应用。
                                                 / 表示根路径，特殊的：根路径的cookie可以被任何url的页面访问 """

            return  respone
    return render(request,"login.html")
def index(request):
    print (request.COOKIES)
    is_log = request.COOKIES.get("is_login")
    print (is_log)
    if is_log:
        usernamre = request.COOKIES.get("username")
        import datetime
        now = datetime.datetime.now()
        print(now)
        last_time = request.COOKIES.get("last_visit_time")
        respone = render(request, "index.html", locals())
        respone.set_cookie("last_visit_time",now)
        return  respone
    else:
        return redirect("/login/")
def test(request):
    print (request.COOKIES)
    return HttpResponse("ok")
def login_session(request):
    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    # print (user,pwd)
    use = User.objects.filter(user=user, pwd=pwd).first()
    if use:
        import datetime
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request.session["is_login"]=True
        request.session["username"]=use.user
        request.session["last_visit_time"]=now
        return HttpResponse("登录成功")
    return render(request, "login.html")
def index_session(request):
    print (request.session.get("is_login"))
    name = request.session.get("username")
    date = request.session.get("last_visit_time")

    login = request.session.get("is_login")
    if  not login:
       return redirect("/login/")
    return render(request,"index.html",locals())