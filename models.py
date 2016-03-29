from django.db import models
from random import randint
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Student(AbstractUser):
    first_three_digit_rollno=models.CharField(max_length=3)
    branch=models.CharField(max_length=3)
    year=models.CharField(max_length=4)
    image=models.ImageField(upload_to='uploads/')
    mainrollno=models.CharField(max_length=11)
    #bookmark=models.ManyToManyField(Notification,through="Bookmark",related_name="bookmarked_by",null=True,blank=True)
    
class Notification(models.Model):
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=1000)
    date_created=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
    by=models.ForeignKey(Student)
    branch=models.CharField(max_length=3)
    year=models.CharField(max_length=4)
    likes=models.PositiveSmallIntegerField(default=0)
    #likes=models.CharField(max_length=4)
    bookmark_agent=models.ManyToManyField(Student,through="Bookmark",null=True,blank=True, related_name="bookmark")
    likers=models.ManyToManyField(Student, related_name="news_liked", null=True,blank=True)
    seens=models.PositiveSmallIntegerField(default=0)
    seenby=models.ManyToManyField(Student,related_name="have_seen",null=True,blank=True)
    
    def __str__(self):
        return self.title
class Commentary(models.Model):
    comment=models.CharField(max_length=100)
    description=models.ForeignKey(Notification)
    person=models.ForeignKey(Student)
    date_created=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)


class Bookmark(models.Model):
    stud = models.ForeignKey(Student, related_name="abc")
    noti = models.ForeignKey(Notification)
    #rank=models.PositiveSmallIntegerField(default=0)
    rank=models.IntegerField()
    

def create_otp(student=None,purpose=None):
    if not student:
        raise ValueError("Invalid Arguments");
    choices=[]
    for choice_purpose,verbose in StudentOTP.OTP_PURPOSE_CHOICES:
        choices.append(choice_purpose)
    if not purpose in choices:
        raise ValueError('Invalid Arguments');
    if StudentOTP.objects.filter(student=student,purpose=purpose):
        old_otp.delete();
    otp=randint(1000,9999)
    otp_object=StudentOTP.objects.create(student=student,purpose=purpose,otp=otp)
    return otp

def get_valid_otp_object(student=None,otp=None,purpose=None):
    if not student:
        raise ValueError("invalid Arguments");
    choices=[]
    for choice_purpose,verbose in StudentOTP.OTP_PURPOSE_CHOICES:
        choices.append(choice_purpose)
    if not purpose in choices:
        raise ValueError("Invalid Arguments");
    try:
        otp_object=StudentOTP.objects.get(student=student,purpose=purpose,otp=otp)
        return otp_object
    except StudentOTP.DoesNotExist:
        return None


    
    
class StudentOTP(models.Model):
    OTP_PURPOSE_CHOICES=(
        ('FP','Forgot Password'),
        ('AA','Activate Account'),
    );
    student=models.ForeignKey(Student)
    otp=models.CharField(max_length=4)
    purpose=models.CharField(max_length=2,choices=OTP_PURPOSE_CHOICES)
    created_on=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together=['student','purpose']