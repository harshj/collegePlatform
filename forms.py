from django import forms
from .models import Student, Commentary,Notification,Bookmark
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.http import Http404, JsonResponse, HttpResponse
class LoginForm(forms.Form):
    username = forms.CharField(max_length = 25);
    password = forms.CharField(widget = forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        self.authenticated_user = None;
        super(LoginForm, self).__init__(*args, **kwargs)
    
    def clean_username(self):
        data_username = self.cleaned_data['username']
        if Student.objects.filter(username = data_username).count() != 1:
            raise forms.ValidationError('Invalid Username')
        return data_username

    def clean(self):
        data_username = self.cleaned_data.get('username', '')
        data_passwd = self.cleaned_data.get('password', '')
        user = authenticate(username=data_username, password = data_passwd)
        #return HttpResponse(user.is_active)
        if data_username and data_passwd and not user:
            raise forms.ValidationError('Username/Password doesnot match')
            #return HttpResponse("HELLO")
        if user and user.is_active == False:
            raise forms.ValidationError('Inactive User')
        self.authenticated_user = user
        return self.cleaned_data;
    
class PostNews(forms.ModelForm):
#    Title=forms.CharField(max_length=100)
#    News=forms.CharField(max_length=100)
    def clean_Title(self):
        data_Title=self.cleaned_data['title']
        if len(data_Title.split())==0:
            print('comment split, error raised')
            raise forms.ValidationError("Enter a Title please")
        return data_Title
    
    def clean_News(self):
        print('entered here')
        data_News=self.cleaned_data['description']
        if len(data_News.split())==0:
            print('comment split, error raised')
            raise forms.ValidationError("Enter a News please")
        return data_News
    class Meta:
        model=Notification
        fields=['title','description']  



    
class PostComment(forms.ModelForm):
    comment=forms.CharField(max_length=100)
    def clean_comment(self):
        print('entered here')
        data_comment=self.cleaned_data['comment']
        if len(data_comment.split())==0:
            print('comment split, error raised')
            raise forms.ValidationError("Enter a comment please")
        return data_comment
    class Meta:
        model=Commentary
        fields=['comment']

class PostRank(forms.ModelForm):
    rank=forms.IntegerField()
    def clean_rank(self):
        data_rank=self.cleaned_data['rank']
        print (data_rank)
        if(data_rank>=0 and data_rank<=5):
            print('wrong wrong')
            return data_rank
        raise forms.ValidationError("Add Appropriate value")

    class Meta:
        model=Bookmark
        fields=['rank']
    
class EditForm(forms.ModelForm):
    
    email=forms.EmailField(help_text='A valid email address ,please')
    #uname=forms.CharField(max_length=20)
    #old_password=forms.CharField(widget=forms.PasswordInput)#password=forms.CharField(max_length=20,widget=forms.PasswordInput)
    #old_password=forms.CharField(max_length=10)
    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(max_length=20,widget=forms.PasswordInput)
    
    def clean_email(self):
        c=100
        email=self.cleaned_data.get('email','')
        if not email:
            raise forms.ValidationError("This Field is required")
        try:
            validate_email(email)
            c=100
        except ValidationError:
            c=200
        #if not email:
            #raise forms.ValidationError("This Field is required")
        if (c==200):
            raise forms.ValidationError("This is not valid Email address")
        return email
    
    
    def clean_confirm_password(self):
        data_password = self.cleaned_data.get('password')
        data_confirm_password = self.cleaned_data.get('confirm_password')
        if (data_password and data_confirm_password 
                and data_password != data_confirm_password):
            raise forms.ValidationError("The two passwords field didn't match")
        return data_confirm_password
    
    class Meta:
        model =Student
        fields=['image']
    
    
    
    
class SignupForm(forms.ModelForm):
    email=forms.EmailField(help_text='A valid email address ,please')
    #uname=forms.CharField(max_length=20)
    mainrollno=forms.CharField(max_length=11)
    #password=forms.CharField(max_length=20,widget=forms.PasswordInput)
    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(max_length=20,widget=forms.PasswordInput)
    #image=forms.ImageField(upload_to='uploads/')
    
    def clean_email(self):
        c=100
        email=self.cleaned_data.get('email','')
        if not email:
            raise forms.ValidationError("This Field is required")
        try:
            validate_email(email)
            c=100
        except ValidationError:
            c=200
        #if not email:
            #raise forms.ValidationError("This Field is required")
        if (c==200):
            raise forms.ValidationError("This is not valid Email address")
        if Student.objects.filter(email=email).exists():
            raise forms.ValidationError('User with this email already exist')
        return email
     
    
    def clean_mainrollno(self):
        num=self.cleaned_data.get('mainrollno','')
        check1=0
        check2=0
        check3=0
        if(len(num)==11):
            check1=1
        else:
            check1=0
        if(check1==0):
            raise forms.ValidationError("Not A valid rollno")
        str=int(num[3:6])
        if(str==164):
            check2=1
        if(check2==0):
            raise forms.ValidationError("Not a valid rollno")
        if(num[6]=='0' and (num[7]=='1') and ((num[8]=='5') or (num[8]=='6') or (num[8]=='7'))):
            check3=1
        c=check1 & check2 & check3
        if(c==0):
            raise forms.ValidationError("Not a valid rollno")
        if Student.objects.filter(mainrollno=num).exists():
            raise forms.ValidationError('User with this rollnumber already exists') 
        return num
    
    def clean_confirm_password(self):
        data_password=self.cleaned_data.get('password')
        data_confirm_password=self.cleaned_data.get('confirm_password')
        if(data_password and data_confirm_password and data_password!=data_confirm_password):
            raise forms.ValidationError("The two passwords donot match")
        return data_confirm_password
    
    class Meta:
        model=Student
        fields=['email','username','mainrollno','image']