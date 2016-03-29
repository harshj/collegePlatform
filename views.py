from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from collegeplatform.forms import (
									mailForm,
									studentForm,
									)

def home(request):
	if request.method == 'POST':
		form = mailForm(request.POST)
		msg = "Hi this is the test mail from Harsh Jain. Please ignore this."
		subject = "Test Mail - Django"
		sender = "postmaster@sandboxf5a92d594ed448a6bcb04392b6c76e65.mailgun.org"
		recepeint = []
		recepeint.append(request.POST['recepeint'])
		send_mail(subject, msg,sender, recepeint, fail_silently = False)
		return HttpResponse("Success")
	else:	
		form = mailForm()
		
	return render(
					request, 
					'base.html', 
					{
						'form' : form
					}
				)
				
def student(request):
	if request.method == 'POST':
		form = studentForm(request.POST)
		return HttpResponse("Success")
	else:	
		form = studentForm()
	
	return render(
					request,
					'student',
					{
						'form' : form
					}
					)