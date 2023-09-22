import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from .models import *
from django.db.models import Sum
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.shortcuts import redirect
from .forms import DocumentForm
from .forms import UpdateImage
import uuid
from datetime import datetime
import csv
# Create your views here.
def testing(request):
  template = loader.get_template('testing.html')
  member = request.session.get('loginInfo', [])[0]
  mnum = member['mnum']
  groupCount = len(Groupmember.objects.filter(mnum = mnum).values())
  gnumList = Groupmember.objects.filter(mnum = mnum).values_list('gnum',flat = True)
  expenseTotal = 0
  for gnum in gnumList :
     expense = len(Expense.objects.filter(gnum = gnum).values())
     expenseTotal += expense
  paymentTotal = Payment.objects.filter(payernum = mnum).aggregate(
      total=Sum('amount'))['total']
  if groupCount == None :
     groupCount = 0
  if  expenseTotal == None: 
     expenseTotal = 0
  if paymentTotal == None:
     paymentTotal = 0
  context = {
     'groupCount' : groupCount,
     'expenseTotal' : expenseTotal,
     'paymentTotal' : paymentTotal,
  }
  return HttpResponse(template.render(context, request))

def index(request):
  template = loader.get_template('index.html')
  member = None
  if 'loginInfo' in request.session :
    return testing(request)
    member = request.session.get('loginInfo', {})
  else :
    template = loader.get_template('index.html')

  context = {
    'fruits': ['Apple', 'Banana', 'Cherry'],
    'loginInfo': member,
  }
  return HttpResponse(template.render(context, request))

def gotoReg(request) : 
    template = loader.get_template('register.html')
    form = DocumentForm(request.POST, request.FILES)

    context = {
      'form': form
    }
    return HttpResponse(template.render(context, request))
  
def register(request):
    form = DocumentForm(request.POST, request.FILES)
    print(form.is_valid)
    if not form.is_valid():
      print(form.errors)
    if form.is_valid():
      # Access additional fields using form.cleaned_data
      usernameIn = form.cleaned_data['username']
      passwordIn = form.cleaned_data['password']
      password2 = form.cleaned_data['password2']
      dobIn = form.cleaned_data['dob']
      emailIn = form.cleaned_data['email']
      nameIn = form.cleaned_data['name']
      imageIn = form.cleaned_data['image']
      # Additional processing if needed
      print("Username: "+ usernameIn)
      print("Password: " + passwordIn)
      print("DOB: " + str(dobIn))
      print("Email: " + emailIn)
      print("Name: " + nameIn)
      print("Image: " + str(imageIn))
      form.save()
      
    return render(request, 'index.html')

def logout(request):
  template = loader.get_template("index.html")
  request.session.pop('loginInfo', None)
  storage = messages.get_messages(request)
  storage.used = True
  context = {

  }
  return redirect(index)

def submit_form(request):
  template = loader.get_template('testing.html')
  user = request.POST.get('username', '')
  userCheck = Member.objects.filter(username=user).exists()
  loginCheck = False
  if userCheck : 
    pwd = request.POST.get('password', '')
    passwordCheck = Member.objects.filter(username=user, password = pwd).exists()
    if passwordCheck : 
      loginCheck = True
      members = Member.objects.filter(username = user, password = pwd)
      members_dictionary = [{'mnum': member.mnum, 'username' : member.username, 'password':member.password, 'dob' : str(member.dob), 'email' : member.email, 'image': str(member.image), 'name' : member.name} for member in members]
      request.session['loginInfo'] = members_dictionary
    else : 
      loginCheck = False
      messages.error(request, "Invalid Password.")
  else :
    loginCheck = False
    messages.error(request, "Username does not exist.")
  context = {
    'loginCheck' : loginCheck,
  }
  if loginCheck == True :
    return HttpResponse(template.render(context, request))
  else:
    return index(request)


def groups(request):
  template = loader.get_template("group.html")
  member = request.session['loginInfo']
  m = member[0]
  groupmemberList = Groupmember.objects.filter(mnum = m['mnum'])
  gnums = []
  for group in groupmemberList : 
    gnums.append(group.gnum)
  groupList = []
  for gnum in gnums :
    group = Group.objects.get(gnum = gnum)

    groupList.append(group)
  context = {
    'groupList' : groupList,
  }
  return HttpResponse(template.render(context, request))

def createGroup(request):
  template = loader.get_template("createGroup.html")
  form_token = str(uuid.uuid4())
  request.session['form_token'] = form_token
  context = {
    'form_token' : form_token
  }
  return HttpResponse(template.render(context, request))

def get_usernames(request):
    usernames = []  # Replace with your data retrieval logic
    member = request.session.get('loginInfo', [])[0]
    username = member.get('username')
    userList = Member.objects.exclude(username = username)
    for user in userList :
      usernames.append(user.username)
    return JsonResponse({'usernames': usernames})

def saveGroup(request):
    form_token = request.POST.get('form_token')
    session_token = request.session.get('form_token')

    if form_token == session_token:
      users = request.POST.getlist('username[]', '')
      gname = request.POST.get('gname', '')
      gdesc = request.POST.get('gdesc', '')
      category = request.POST.get('category', '')
      currency = request.POST.get('currency', '')
      newGroup = Group(gname = gname, gdesc = gdesc, category = category, currency = currency)
      newGroup.save()
      addedGroup = Group.objects.latest('gnum')
      print(addedGroup)
      for user in users:
        member = Member.objects.get(username = user)
        groupmember = Groupmember(gnum = addedGroup.gnum, mnum = member.mnum, mname = member.name)
        groupmember.save()
    form_token = str(uuid.uuid4())
    request.session['form_token'] = form_token
      
    return groups(request)

def editGroup(request):
  gnum = request.GET.get('gnum')
  group = Group.objects.get(gnum = gnum)
  data = Groupmember.objects.filter(gnum = gnum).values()
  groupmembers = list(data)
  usernames = []
  for m in groupmembers:
    member = Member.objects.get(mnum = m['mnum'])
    print(member.username)
    usernames.append(member.username)
  uList = json.dumps(usernames)
  context = {
    'group' : group,
    'groupMembers' : uList,
  }
  template = loader.get_template('editGroup.html')
  return HttpResponse(template.render(context, request))

def saveEdit(request):
  gnum = request.POST.get('gnum', '')
  users = request.POST.getlist('username[]', '')
  gname = request.POST.get('gname', '')
  gdesc = request.POST.get('gdesc', '')
  category = request.POST.get('category', '')
  currency = request.POST.get('currency', '')
  group = Group.objects.get(gnum = gnum)
  group.gname = gname
  group.gdesc = gdesc
  group.category = category
  group.currency = currency
  group.save()
  for user in users:
    member = Member.objects.get(username = user)
    groupmember = Groupmember(gnum = gnum, mnum = member.mnum, mname = member.name)
    groupmember.save()
  return groups(request)

def usernameCheck(request):
  if request.method == 'POST':
      try:
          # Access JSON data from the request using request.POST
          data_value = request.POST.get('username', None)

          # Use the data as needed
          username_exists = Member.objects.filter(username=data_value).exists()
          if username_exists:
              result = "False"
          else:
              result = "True"

          # Return an appropriate response
          return JsonResponse({'result': result})
      except json.JSONDecodeError:
          return JsonResponse({'error': 'Invalid JSON data'}, status=400)
  else:
      return JsonResponse({'error': 'Unsupported request method'}, status=405)
  
def groupDetail(request):
   template = loader.get_template("groupDetail.html")
   gnum = request.GET.get('gnum','')
   group = Group.objects.get(gnum = gnum)
   expenses = Expense.objects.filter(gnum = gnum)
   totalExp = 0
   splitList = []
   #calculating total expense
   for expense in expenses :
      totalExp += expense.expenseTotal
      split = Split.objects.filter(enum = expense.enum)
      splitList.append(list(split))
   #function to calculate who is in debt (2), and who is owed(1), as well as all names of members(3)
   result = balances(gnum)
   receivers = result[0]
   givers = result[1]
   names = result[2]

   payments = Payment.objects.filter(gnum = gnum).aggregate(
      total= Sum('amount'))['total']
   #sending payment history data
   allPayments = Payment.objects.filter(gnum = gnum)
   paymentData = []
   totalPayment = 0
   for payment in allPayments : 
      payernum = payment.payernum
      payer = Member.objects.get(mnum = payernum)
      receivernum = payment.receivernum
      receiver = Member.objects.get(mnum = receivernum)
      amount = payment.amount
      totalPayment = totalPayment + amount
      pdate = payment.pdate
      data = {'payer' : payer.name, 'receiver':receiver.name, 'amount' : amount, 'pdate' : pdate}
      paymentData.append(data)
   context = {
      'group' : group,
      'totalExp' : totalExp,
      'expenses' : expenses,
      'names' : names,
      'receivers' : receivers,
      'givers' : givers,
      'totalPay' : payments,
      'paymentData' : paymentData,
      'totalPayment' : totalPayment,
   }
   return HttpResponse(template.render(context, request))

def balances(gnum):
  mnumList = Groupmember.objects.filter(gnum = gnum).values_list('mnum', flat=True)
  receivers = []
  givers = []
  membernames = []
  for mnum in mnumList : 
    member = Member.objects.get(mnum = mnum)
    name = member.name
    membernames.append(name)
    print(str(name))
    receivedPayment = Payment.objects.filter(gnum = gnum, receivernum = mnum).aggregate(
      total=Sum('amount'))['total']
    if receivedPayment == None :
       receivedPayment = 0
    
    amountOwed = Split.objects.filter(gnum = gnum, owedto = mnum).aggregate(
      total= Sum('splitamount'))['total']
    if amountOwed == None : 
       amountOwed = 0

    amountIOwe = Split.objects.filter(gnum = gnum, mnum = mnum).aggregate(
      total=Sum('splitamount'))['total']
    if amountIOwe == None :
       amountIOwe = 0

    amountPaid = Payment.objects.filter(gnum = gnum, payernum = mnum).aggregate(
       total = Sum('amount'))['total']
    if amountPaid == None : 
       amountPaid = 0

    netTotal = amountOwed - amountIOwe + amountPaid - receivedPayment
    if netTotal > 0 : 
       receivers.append({'name':name, 'value':netTotal})
    elif netTotal < 0 :
       givers.append({'name':name, 'value':netTotal})
    receivers = sorted(receivers, key=lambda x: x['value'])
    givers = sorted(givers, key =lambda x: x['value'])
  return receivers, givers, membernames

def createExpense(request):
  template = loader.get_template('createExpense.html')
  gnum = request.GET.get('gnum','')
  group = Group.objects.get(gnum= gnum)
  mnumList = Groupmember.objects.filter(gnum = gnum).values_list('mnum', flat=True)
  members = []
  for mnum in mnumList : 
    member = Member.objects.get(mnum = mnum)
    name = member.name
    mnum = member.mnum
    entry = {'name' : name, 'mnum' : mnum}
    members.append(entry)
  context = {
     'members' : members,
     'group' : group,
     
  }
  return HttpResponse(template.render(context, request))
def saveExpense(request):
   gnum = request.POST.get('gnum', '')
   group = Group.objects.get(gnum=gnum)
   ename = request.POST.get('ename','')
   edesc = request.POST.get('edesc','')
   expenseTotal = request.POST.get('expenseTotal', '')
   paidBy = request.POST.get('paidBy', '')
   mnum = request.POST.getlist('splitPayer[]', '')
   splitPayment = request.POST.getlist('splitAmount[]','')
   print('gnum : ' + gnum)
   print('ename: ' + ename)
   print('edesc: ' + edesc)
   print('expenseTotal: ' + expenseTotal)
   splitData = []
   paidByNum = 0
   for i in range(len(mnum)) :
    print('mnum: ' + mnum[i])
    member = Member.objects.get(mnum = mnum[i])

    if member.name != paidBy :
       data = {'mnum': mnum[i], 'splitamount' : splitPayment[i], 'mname' : member.name}
       splitData.append(data)
    else : 
       paidByNum = mnum[i]
   for j in splitPayment:
    print('splitPayment: ' + j)
   newExpense = Expense(gnum = group.gnum, ename = ename, edesc = edesc, expenseTotal = expenseTotal, paidBy = paidBy)
   newExpense.save()
   addedExpense = Expense.objects.latest('enum')
   enum = addedExpense.enum
   for split in splitData :
      mnumber = split['mnum']
      mname = split['mname']
      splitamount = split['splitamount']
      owedto = paidByNum
      owedtoName = paidBy
      newSplit = Split(enum = enum, mnum = mnumber, mname= mname, splitamount = splitamount, owedto = owedto, owedtoname = owedtoName, gnum = gnum)
      newSplit.save()
   return HttpResponseRedirect('/groupDetail/?gnum='+gnum)

def expenseDetail(request):
   template = loader.get_template('expenseDetail.html')
   enum = request.GET.get('enum', '')
   expense = Expense.objects.get(enum = enum)
   allSplit = Split.objects.filter(enum = enum)
   comment = Comment.objects.filter(enum = enum)
   group = Group.objects.get(gnum = expense.gnum)
   members = request.session.get('loginInfo')
   member = None
   for m in members:
    member = m
   
   context = {
      'expense' : expense,
      'allSplit' : allSplit,
      'comment' : comment,
      'group' : group,
      'member' : member,
   }
   return HttpResponse(template.render(context,request))

def viewSettings(request):
  members = request.session.get('loginInfo')
  member = None
  for m in members:
    member = m
  template = loader.get_template('viewSettings.html')
  print(member['image'])
  form = UpdateImage(request.POST, request.FILES)
  context = {
     'member' : member,
     'form' : form,
  }
  return HttpResponse(template.render(context, request))

def updateImage(request) : 
    form = UpdateImage(request.POST, request.FILES)
    print(form.is_valid)
    if not form.is_valid():
      print(form.errors)
    if form.is_valid():
      # Access additional fields using form.cleaned_data
      mnumIn = form.cleaned_data['mnum']
      imageIn = form.cleaned_data['image']
      member = Member.objects.get(mnum = mnumIn)
      member.image = imageIn
      member.save()
    context = {
       
    }
    return HttpResponseRedirect('/viewSettings/')

def saveSettings(request):
   mnum = request.POST.get('mnum', '')
   username = request.POST.get('username', '')
   name = request.POST.get('name','')
   password = request.POST.get('password', '')
   email = request.POST.get('email','')
   dob = request.POST.get('dob', '')
   member = Member.objects.get(mnum = mnum)
   member.username = username
   member.name = name
   member.password = password
   member.email = email
   member.dob = dob
   member.save()
   member = Member.objects.get(mnum=mnum)
   template = loader.get_template('viewSettings.html')
   members = Member.objects.filter(mnum = mnum)
   members_dictionary = [{'mnum': member.mnum, 'username' : member.username, 'password':member.password, 'dob' : str(member.dob), 'email' : member.email, 'image': str(member.image), 'name' : member.name} for member in members]
   request.session['loginInfo'] = members_dictionary
   context = {
      'member': member,
   }
   return HttpResponse(template.render(context, request))

def addComment(request):
   enum = request.POST.get('enum', '')
   author = request.POST.get('commenter', '')
   cpic = request.POST.get('cpic', '')
   comment = request.POST.get('comment','')
   cdate = datetime.today().strftime('%Y-%m-%d')
   comment = Comment(enum = enum, author = author, cpic= cpic, comment = comment, cdate = cdate)
   comment.save()
   return HttpResponseRedirect('/expenseDetail/?enum='+ enum)

def createPayment(request):
   gnum = request.GET.get('gnum' , '')
   gmemberList = Groupmember.objects.filter(gnum = gnum).values_list(flat = True)
   memberList = []
   for gm in gmemberList :
      mnum = gm
      member = Member.objects.get(mnum = mnum)
      memberList.append(member)
   context = {
      'memberList' : memberList,
      'gnum' : gnum,
   }   
   template = loader.get_template('createPayment.html')
   return HttpResponse(template.render(context, request))

def savePayment(request):
   gnum = request.POST.get('gnum', '')
   payernum = request.POST.get('payernum', '')
   receivernum = request.POST.get('receivernum', '')
   amount = request.POST.get('amount','')
   pdate = request.POST.get('pdate', '')
   payment = Payment(gnum = gnum, payernum = payernum, receivernum = receivernum, amount = amount, pdate = pdate)
   payment.save()
   return HttpResponseRedirect('/groupDetail/?gnum='+gnum)

def viewExpense(request):
   member = request.session.get('loginInfo', [])[0]
   template = loader.get_template('viewExpense.html')
   gnums = Groupmember.objects.filter(mnum = member['mnum']).values_list('gnum', flat=True)
   expenseList = []
   for gnum in gnums :
      expenses = Expense.objects.filter(gnum = gnum)
      group = Group.objects.get(gnum=gnum)
      currency = group.currency
      for expense in expenses :
         e = {
            'expenseTotal' : expense.expenseTotal,
            'paidBy' : expense.paidBy,
            'ename' : expense.ename,
            'edesc' : expense.edesc,
            'currency' : currency,
         }
         expenseList.append(e)
   
   context = {
    'expenseList' : expenseList,
   }
   return HttpResponse(template.render(context,request))

def download_csv(request):
    # Your data list
   member = request.session.get('loginInfo', [])[0]
   template = loader.get_template('viewExpense.html')
   gnums = Groupmember.objects.filter(mnum = member['mnum']).values_list('gnum', flat=True)
   expenseList = []
   for gnum in gnums :
      expenses = Expense.objects.filter(gnum = gnum)
      group = Group.objects.get(gnum=gnum)
      currency = group.currency
      for expense in expenses :
         e = {
            'expenseTotal' : expense.expenseTotal,
            'paidBy' : expense.paidBy,
            'ename' : expense.ename,
            'edesc' : expense.edesc,
            'currency' : currency,
         }
         expenseList.append(e)


    # Create an HTTP response with CSV content
   response = HttpResponse(content_type='text/csv')
   response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    # Create a CSV writer and write data to the response
   writer = csv.writer(response)
    
    # Write the CSV header row if needed
   writer.writerow(['Expense Total', 'Paid By', 'Expense Name', 'Expense Description', 'Currency'])

    # Write the data rows
   for row in expenseList:
     writer.writerow([row['expenseTotal'], row['paidBy'], row['ename'], row['edesc'], row['currency']])

   return response

def aboutUs(request):
   template = loader.get_template('aboutUs.html')
   context = {
      
   }
   return HttpResponse(template.render(context, request))