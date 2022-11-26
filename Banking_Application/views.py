import sqlite3
# from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
import random
def Home(request):
    return render(request, 'index.html')
def users(request):
    return render(request, 'index.html')
def bank(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'index.html')
def contact(request):
    return render(request, 'index.html')
def login(request):
    return render(request, 'index.html')
def register(request):
    return render(request, 'Account.html')
def Check_Balance(request):
    return render(request, 'Balance.html')
def Withdraw_Amount(request):
    return render(request, 'Withdraw.html')
def Deposit_Amount(request):
    return render(request, 'Deposit.html')
def Accounts(request):
    list1=[]
    list1.insert(0,request.GET.get('First Name', 'default'))
    list1.insert(1,request.GET.get('Last Name', 'default'))
    list1.insert(2,request.GET.get('Date Of Birth', 'default'))
    list1.insert(3,request.GET.get('Mother Name', 'default'))
    list1.insert(4,request.GET.get('Father Name', 'default'))
    list1.insert(5,request.GET.get('Phone No', 'default'))
    Account_No=""
    PIN_No=""
    for i in range(10):
        Account_No+=str(random.randint(0,9))
    list1.insert(6,Account_No)
    for i in range(4):
        PIN_No+=str(random.randint(0,9))
    list1.insert(7,PIN_No)
    list1.insert(8,'0')
    connector=sqlite3.connect('employee.db')
    ct=connector.cursor()
    ct.execute('CREATE TABLE IF NOT EXISTS Accounts_Table (First_Name TEXT,Last_Name TEXT, Date_Of_Birth TEXT, Mother_Name TEXT, Father_Name TEXT, Phone_No TEXT, Account_No TEXT, PIN_NO TEXT, Balance TEXT)')
    ct.execute('INSERT INTO Accounts_Table VALUES(?,?,?,?,?,?,?,?,?)', list1)
    parameters={'Account_Num' : Account_No, 'PIN_Num': PIN_No}
    ct.close()
    connector.commit()
    return render(request, 'Details.html', parameters)
def Balance(request):
    list1=[]
    list1.insert(0,request.GET.get('Account_Num', 'default'))
    PIN=request.GET.get('PIN_Num', 'default')
    connector=sqlite3.connect('employee.db')
    ct=connector.cursor()
    ct.execute("SELECT * FROM Accounts_Table WHERE Account_No=?", list1)
    row=ct.fetchall()
    if len(row) >=1:
        val=row[-1]
        ct.close()
        connector.commit()
        bal=val[-1]
        list1.insert(1, "-")
        parameters={'Current_Bal' : bal, 'PIN_Num': PIN, 'Account_Num' : list1[0], 'str': list1[1]}
        return render(request, 'Balance.html', parameters)
    else:
        return render(request, 'Account.html')
def Deposit(request):
    list1=[]
    list1.insert(0,request.GET.get('Account_Num', 'default'))
    PIN=request.GET.get('PIN_Num', 'default')
    amount=request.GET.get('Amount', 'default')
    connector=sqlite3.connect('employee.db')
    ct=connector.cursor()
    ct.execute("SELECT * FROM Accounts_Table WHERE Account_No=?", list1)
    row=ct.fetchall()
    if len(row) >=1:
        val=row[-1]
        bal=val[-1]
        list1.insert(1,str(int(val[-1])+int(amount)))
        list1.reverse()
        ct.execute("UPDATE Accounts_Table SET Balance=? WHERE Account_No=?", list1)
        ct.close()
        connector.commit()
        parameters={'curr_bal' : bal, 'PIN_Num': PIN, 'Account_Num' : list1[1], 'upd_bal' : list1[0]}
        return render(request, 'Deposit.html', parameters)
    else:
        return render(request, 'Account.html')
def Withdraw(request):
    list1=[]
    list1.insert(0,request.GET.get('Account_Num', 'default'))
    PIN=request.GET.get('PIN_Num', 'default')
    amount=request.GET.get('Amount', 'default')
    connector=sqlite3.connect('employee.db')
    ct=connector.cursor()
    ct.execute("SELECT * FROM Accounts_Table WHERE Account_No=?", list1)
    row=ct.fetchall()
    if len(row) >=1:
        val=row[-1]
        bal=val[-1]
        if int(val[-1])-int(amount) > 0:
            list1.insert(1,str(int(val[-1])-int(amount)))
            list1.reverse()
            ct.execute("UPDATE Accounts_Table SET Balance=? WHERE Account_No=?", list1)
            ct.close()
            connector.commit()
            parameters={'curr_bal' : bal, 'PIN_Num': PIN, 'Account_Num' : list1[1], 'upd_bal' : list1[0]}
        else:
            list1.insert(1, "Insufficient Balance")
            parameters={'curr_bal' : bal, 'PIN_Num': PIN, 'Account_Num' : list1[0], 'upd_bal' : list1[1]}
        return render(request, 'Withdraw.html', parameters)
    else:
        return render(request, 'Account.html')

