from django.db import models

class Student(models.Model):
	COURSE = (
				('IT','Information Technology'),
				('CS','Computer Science'),
				('EC','Electronics and Communication'),
			)
				
	YEAR = (
				('FR', 'Freshman'),
				('SO', 'Sophomore'),
				('JR', 'Junior'),
				('SR', 'Senior'),
				('GR', 'Graduate'),
			)
	
	name = models.CharField(max_length = 30)
	roll_no = models.CharField(max_length = 11, primary_key = True)
	course = models.CharField(max_length = 2, choices = COURSE)
	year = models.CharField(max_length = 2, choices = YEAR)