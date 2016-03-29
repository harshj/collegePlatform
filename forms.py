from django import forms
from django.core.validators import RegexValidator
from collegeplatform.models import Student

class mailForm(forms.Form):	
	recepeint = forms.EmailField(
										label = "Email of the Recepeint \n \n" ,
										
										)
										
class studentForm(forms.Form):
	class Meta:
		model = Student	
		fields = '__all__'