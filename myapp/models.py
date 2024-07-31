from django.contrib.auth.models import AbstractUser
from django.db import models

class user_data(AbstractUser):
    userid=models.IntegerField(primary_key=True)
    test_attempt=models.IntegerField(null=True,blank=True)
    dob=models.DateField(null=True,blank=True)
    contact=models.ImageField(null=True,blank=True)
    gender=models.CharField(max_length=200, null=True,blank=True)
    profilelink1=models.CharField(max_length=200,null=True,blank=True)
    profilelink2=models.CharField(max_length=200,null=True,blank=True)
    profilelink3=models.CharField(max_length=200,null=True,blank=True)
    pfp=models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.username

class Report(models.Model):
    userid=models.ForeignKey(user_data,on_delete=models.CASCADE)
    percentage=models.FloatField()
    field = models.CharField(max_length=255)
    totalEMarks=models.FloatField(null=True, blank=True)
    totalFMarks=models.FloatField(null=True, blank=True)
    totalMarks=models.IntegerField(null=True, blank=True)
    totalQue=models.IntegerField(null=True, blank=True)
    time=models.DateField(auto_now=True)
    level=models.IntegerField(null=True, blank=True)
    # eng_marks=models.IntegerField()
    def __str__(self):
        return str(self.userid)

class quiz(models.Model):
    field_of_study=models.CharField(max_length=50)
    question_text = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.PositiveSmallIntegerField()

class seminars(models.Model):
    name=models.CharField(max_length=225)
    organizer=models.CharField(max_length=225)
    date=models.DateField()
    link=models.URLField()
  
class ngo(models.Model):
    name=models.CharField(max_length=225)
    location=models.CharField(max_length=225)
    link=models.URLField()
    note=models.CharField(max_length=225,null=True,blank=True)


class techcourse(models.Model):
  name=models.CharField(max_length=225)
  level=models.CharField(max_length=20)
  link=models.URLField()
  image=models.CharField(max_length=200, blank=True, null=True)

class engcourse(models.Model):
  name=models.CharField(max_length=225)
  level=models.CharField(max_length=20)
  link=models.URLField()
  image=models.CharField(max_length=200, blank=True, null=True)

class makedonation(models.Model):
  userid=models.ForeignKey(user_data,on_delete=models.CASCADE)
  name=models.CharField(max_length=225)
  donateto=models.CharField(max_length=225)
  donation=models.BigIntegerField()
  comment=models.TextField()