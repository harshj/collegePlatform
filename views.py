from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST,require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template import loader
from .forms import SignupForm,LoginForm, PostComment,PostNews,PostRank,EditForm# ForgotPassword, SetPasswordForm, LoginForm
from .models import Student, create_otp, get_valid_otp_object,Notification, Commentary,Bookmark
from django.shortcuts import get_object_or_404
import datetime
from datetime import date

# Create your views here.
def signup(request):
    if request.user.is_authenticated():
        return HttpResponse("YOU ARE LOGGED IN");
    if request.method=='GET':
        context={'f':SignupForm()};
        return render(request,'signupapplication/auth/signup.html',context);
    else:
        f=SignupForm(request.POST,request.FILES);
        if not f.is_valid():
             return render(request,'signupapplication/auth/signup.html',{'f':f});
        else:
            user=f.save(commit=False)
            user.set_password(f.cleaned_data['password'])
            user.image=f.cleaned_data['image']
            user.is_active=False
            str=user.mainrollno
            user.first_three_digit_rollno=str[0:3]
            user.branch=str[6:9]
            user.year='20'+str[9:12]
            user.save()
            #return HttpResponse(user.mainrollno);
            otp=create_otp(student=user,purpose='FP')
            student=Student.objects.get(username=user.username)
            return render(request,'signupapplication/auth/receiveotp.html',{'u':student,'otp':otp});

        
def editprofileredirect(request,id1=None):
    return redirect(reverse('editprofile'));

def editprofile(request):
    if request.method=='GET':
        #querying
        e=Student.objects.get(id=request.user.id).email
        f = EditForm(initial={'email': e})
        return render(request,'signupapplication/auth/editprofilepage.html',{'f':f});
    else:
        stud_object=get_object_or_404(Student,id=request.user.id)
        #return HttpResponse("JAVED ALI");
        f=EditForm(request.POST,request.FILES,instance=stud_object)
        if not f.is_valid():
            #return HttpResponse("KUCH GALTI HAIN");
            return render(request,'signupapplication/auth/editprofilepage.html',{'f':f});
        else:
            #return HttpResponse(f.cleaned_data['image'])
            stud_object=f.save(commit=False)
            stud_object.email=f.cleaned_data['email']
            stud_object.image=f.cleaned_data['image']
            stud_object.save()
            return redirect(reverse('profile',kwargs={'id':request.user.id}));
            #return HttpResponse("SUCCESSFULY UPDATED PROFILE");
            

def unlike(request, id2):
    i=Notification.objects.get(id=int(id2))
    i.likes=i.likes-1
    o=Student.objects.get(id=request.user.id)
    i.save()
    o.save()
    i.likers.remove(o)
    #i.save()
    #o.save()
    #i.likes=i.likes+1    
    #return HttpResponse('LIKED')
    return redirect(reverse('moredetail',kwargs={'id1':request.user.id,'id2':id2}));
def like(request,id1=None,id2=None):
#    return HttpResponse("donkeu");
    i=Notification.objects.get(id=int(id2))
    i.likes=i.likes+1
    o=Student.objects.get(id=int(id1))
    i.save()
    o.save()
    i.likers.add(o)
    #i.save()
    #o.save()
    #i.likes=i.likes+1    
    #return HttpResponse('LIKED')
    return redirect(reverse('moredetail',kwargs={'id1':id1,'id2':id2}));
def bookmark(request,id2=None):
    #return HttpResponse(request.user);
    fprime=PostRank(request.POST);
    
    #return HttpResponse(request.POST);
    if not fprime.is_valid():
        
        return redirect(reverse('moredetail',kwargs={'id1':request.user.id,'id2':id2}));
    info_displayed=Notification.objects.filter(id=int(id2))
    #return HttpResponse(info_displayed);
    getval=fprime.cleaned_data['rank']
    m1=Bookmark(stud=request.user,noti=info_displayed[0],rank=getval)
    m1.save()
    return redirect(reverse('moredetail',kwargs={'id1':request.user.id,'id2':id2}));

def unbookmark(request,id1=None,id2=None):
    info_displayed=Notification.objects.filter(id=int(id2))
    m1=Bookmark.objects.get(stud=request.user,noti=info_displayed[0])
    
    m1.delete()
    return redirect(reverse('moredetail',kwargs={'id1':request.user.id,'id2':id2}));

def activate(request,id=None,otp=None):
    student=get_object_or_404(Student,id=int(id));
    print(student.username)
    otp_object=get_valid_otp_object(student=student,purpose='FP',otp=otp)
    if not otp_object:
        raise Http404();
    student.is_active=True
    student.save()
    otp_object.delete()
    return render(request,'signupapplication/auth/activatesuccess.html',{'u':student})

@require_http_methods(['GET', 'POST'])
def moredetail(request,id1=None,id2=None):
    uid=int(id1)
    u= Student.objects.get(pk=uid)
    #indicate=0
    fprime=PostRank()
    if request.method=='GET':
        #context={'f':PostComment()};
        f=PostComment()
        info_displayed=Notification.objects.get(id=int(id2))
        uid=int(id1)
        pic=request.user.image
        uname=request.user.username
        commentdetails=Commentary.objects.filter(description=id2)
        indicateseen=0
        seenlist=info_displayed.seenby.all()
        for i in seenlist:
            if(i.username==request.user.username):
                indicateseen=1
        if(indicateseen==0):
            info_displayed.seens=info_displayed.seens+1
            info_displayed.save()
            u.save()
            info_displayed.seenby.add(request.user)
        
        likerlist=info_displayed.likers.all()
        indicate=0
        for i in info_displayed.bookmark_agent.all():
            if(i.username==request.user.username):
                indicate=1
                
        
        return render(request,'signupapplication/auth/moredetailinfo.html',{'co':commentdetails,'i':info_displayed,'uid':uid,'uname':uname, 'f': f,'pic':pic, 'likerlist':likerlist, 'u':u,'indicate':indicate,'fprime':fprime})
    else:
        #return HttpResponse("WAYWARD");
        info_displayed=Notification.objects.get(id=int(id2))
        uid=int(id1)
        uname=request.user.username
        commentdetails=Commentary.objects.filter(description=id2)
        likerlist=info_displayed.likers.all()
        f=PostComment(request.POST);
        pic=request.user.image
        indicate=0
        for i in info_displayed.bookmark_agent.all():
            if(i.username==request.user.username):
                indicate=1
        if not f.is_valid():
            return render(request,'signupapplication/auth/moredetailinfo.html',{'co':commentdetails,'i':info_displayed,'uid':uid,'uname':uname, 'f': f,'pic':pic, 'likerlist':likerlist, 'u':u,'indicate':indicate,'fprime':fprime})
            
        else:
            comment= f.save(commit=False)
            commenttext=f.cleaned_data['comment']
            if commenttext.strip() is None: 
                print('wrong comment')
                return render(request,'signupapplication/auth/moredetailinfo.html',{'co':commentdetails,'i':info_displayed,'uid':uid,'uname':uname, 'f': f,'pic':pic, 'likerlist':likerlist, 'u':u,'indicate':indicate,'fprime':fprime})
            comment.person= request.user;
            comment.description= info_displayed;
            comment.save();
            print('added successfully')
            return render(request,'signupapplication/auth/moredetailinfo.html',{'co':commentdetails,'i':info_displayed,'uid':uid,'uname':uname, 'f': f,'pic':pic, 'likerlist':likerlist, 'u':u,'indicate':indicate,'fprime':fprime})
        
        
        
def profile(request,id):
    year=Student.objects.get(id=int(id)).year
    branch=Student.objects.get(id=int(id)).branch
    newsi=Notification.objects.filter(year=year,branch=branch)
    newsbyme=Notification.objects.filter(by=request.user)
    uname=request.user.username
    u=request.user
    uid=request.user.id
    uid=id
    pic=request.user.image
    newsid=Notification.objects.filter(year=year,branch=branch)
    if(request.method=='GET'):
        f=PostNews()
    #today = datetime.date.today()
    #d0 = news[0].date_modified
    #delta=today-d0
    #today = datetime.date.today()
    #delta=today-d0
        return render(request,'signupapplication/auth/profileinfo.html',{'u':u,'newsi':newsi,'newsbyme':newsbyme,'uname':uname,'uid':uid,'newsid':newsid,'pic':pic,'f':f})
    else:
        f=PostNews(request.POST)
        if not f.is_valid():
             return render(request,'signupapplication/auth/profileinfo.html',{'u':u,'newsi':newsi,'newsbyme':newsbyme,'uname':uname,'uid':uid,'newsid':newsid,'pic':pic,'f':f})
        else:
            news=f.save(commit=False)
            newstext=f.cleaned_data['description']
            newstitle=f.cleaned_data['title']
            if newstext.strip() is None or newstitle.strip is None:
                 return render(request,'signupapplication/auth/profileinfo.html',{'u':u,'newsi':newsi,'newsbyme':newsbyme,'uname':uname,'uid':uid,'newsid':newsid,'pic':pic,'f':f})
            news.by=request.user;
            news.branch=request.user.branch;
            news.year=request.user.year;
            news.save();
            return render(request,'signupapplication/auth/profileinfo.html',{'u':u,'newsi':newsi,'newsbyme':newsbyme,'uname':uname,'uid':uid,'newsid':newsid,'pic':pic,'f':f})


@require_http_methods(['GET', 'POST'])
def modifynews(request,id1=None,id2=None):
    news_obj=get_object_or_404(Notification,id=id2)
    #return HttpResponse(news_obj.title);
    if request.method=='GET':
        f=PostNews(instance=news_obj)
        return render(request,'signupapplication/auth/modifynews.html',{'f':f,'id1':id1,'id2':id2})
    else:
        f=PostNews(request.POST,instance=news_obj)
        if f.is_valid():
            news_obj=f.save(commit=False)
            news_obj.save()
            print("HIHIHIHIHIHIHIHIHIH")
            #return HttpResponse("ok");
            #return render(request,'signupapplication/auth/modifynews.html',{'f':f,'id':id1})
            return redirect(reverse('profile',kwargs={'id':id1}));
        else:
            return render(request,'signupapplication/auth/modifynews.html',{'f':f,'id1':id1,'id2':id2})

@require_http_methods(['GET', 'POST'])
def deletenews(request,id1=None,id2=None):
    news_obj=get_object_or_404(Notification,id=id2)
    news_obj.delete()
    return redirect(reverse('profile',kwargs={'id':id1}));
       





@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated():
        #return HttpResponse("You are logged in");
        return render(request,'signupapplication/auth/base1.html');
    if request.method == 'GET':
        context = { 'f' : LoginForm()};
        return render(request, 'signupapplication/auth/login.html', context);
    else:
        f = LoginForm(request.POST);
        #return HttpResponse("HELLO TO AMERICA")
        if not f.is_valid():
            return render(request, 'signupapplication/auth/login.html', {'f' : f});
        else:
            #return HttpResponse("HELLO TO AMERICA");
            user = f.authenticated_user
            auth_login(request, user)
            idofstud = Student.objects.get(username=user.username).id
            return redirect(reverse('profile',kwargs={'id':idofstud}));