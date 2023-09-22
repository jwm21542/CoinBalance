from django.db import models

# Create your models here.
class Group(models.Model):
    gnum = models.IntegerField(primary_key=True, auto_created = True)
    gname = models.CharField(max_length=255)
    gdesc = models.CharField(max_length=255)
    currency = models.CharField(max_length=30)
    category = models.CharField(max_length=40)

class Groupmember(models.Model):
    gmnum = models.IntegerField(primary_key=True, auto_created=True)
    gnum = models.IntegerField()
    mnum = models.IntegerField()
    mname = models.CharField(max_length=255)

class Member(models.Model):
    mnum = models.IntegerField(primary_key=True, auto_created=True)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length= 255)
    password = models.CharField(max_length = 14)
    name = models.CharField(max_length = 50)
    image = models.FileField(upload_to = 'members/')
    dob = models.DateField()

class Expense(models.Model):
    enum = models.IntegerField(primary_key=True, auto_created = True)
    gnum = models.IntegerField()
    expenseTotal = models.IntegerField()
    paidBy = models.CharField(max_length = 50)
    ename = models.CharField(max_length=255)
    edesc = models.CharField(max_length=255, null = False)
    
class Split(models.Model):
    snum = models.IntegerField(primary_key= True,auto_created=True)
    enum = models.IntegerField()
    gnum = models.IntegerField()
    mnum = models.IntegerField()
    mname = models.CharField(max_length=255, null = False)
    splitamount = models.FloatField()
    owedto = models.IntegerField()
    owedtoname = models.CharField(max_length = 255, null = False)

class Comment(models.Model):
    cnum = models.IntegerField(primary_key=True, auto_created=True)
    enum = models.IntegerField()
    comment = models.CharField(max_length= 2000)
    author = models.CharField(max_length = 255)
    cdate = models.DateField()
    cpic = models.CharField(max_length=255)

class Notification(models.Model):
    anum = models.IntegerField(primary_key=True, auto_created=True)
    sendernum = models.IntegerField()
    receivernum = models.IntegerField()
    content = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    adate = models.DateField()

class Payment(models.Model):
    pnum = models.IntegerField(primary_key=True, auto_created=True)
    payernum = models.IntegerField()
    receivernum = models.IntegerField()
    amount = models.IntegerField()
    pdate = models.DateField()
    gnum = models.IntegerField()


