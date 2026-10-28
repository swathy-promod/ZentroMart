from django.shortcuts import render

# Create your views here.

def Sum(request):
    if request.method == "POST":
        a = int(request.POST.get("txt_num1"))
        b = int(request.POST.get("txt_num2"))
        c = a+b
        return render(request,"Basics/Sum.html",{'Sum':c})
    else:
        return render(request,"Basics/Sum.html")

def Sum2(request):
    if request.method == "POST":
        a = int(request.POST.get("txt_num1"))
        b = int(request.POST.get("txt_num2"))
        c = a+b
        return render(request,"Basics/Sum2.html",{'Sum':c})
    else:
        return render(request,"Basics/Sum2.html")

def Calculator(request):
    if request.method == "POST":
        a = int(request.POST.get("txt_num1"))
        b = int(request.POST.get("txt_num2"))
        btn=request.POST.get('btn_operation')
        if btn=="+":
            c=a+b
        elif btn=="-":
            c=a-b
        elif btn=="*":
            c=a*b
        elif btn=="/":
            c=a/b
        return render(request,"Basics/Calculator.html",{'c':c})
    else:           
        return render(request,"Basics/Calculator.html")

def Largest(request):
    if request.method == "POST":
        a = int(request.POST.get("txt_num1"))
        b = int(request.POST.get("txt_num2"))
        if a>b:
            c=a
        else:
            c=b
        
        return render(request,"Basics/Largest.html",{'c':c})
    else:
        return render(request,"Basics/Largest.html")
    
def Largest3(request):
    if request.method == "POST":
        a = int(request.POST.get("txt_num1"))
        b = int(request.POST.get("txt_num2"))
        c = int(request.POST.get("txt_num3"))
        if a>b and a>c:
            c=a
        elif b>c:
            c=b
        else:
            c=c
        
        return render(request,"Basics/Largest3.html",{'c':c})
    else:
        return render(request,"Basics/Largest3.html")
    
def RankList(request):
    if request.method=="POST":
        fn=request.POST.get('txt_fname')
        ln=request.POST.get('txt_lname')
        rno=int(request.POST.get('txt_roll'))
        dpt=request.POST.get('sel_dept')
        sem=int(request.POST.get('sel_sem'))
        m1=int(request.POST.get('txt_mark1'))
        m2=int(request.POST.get('txt_mark2'))
        m3=int(request.POST.get('txt_mark3'))

        fullname=fn+""+ln
        total=m1+m2+m3
        if total>=90:
            grade="A+"
        elif total>=80:
            grade="A"
        elif total>=70:
            grade="B+"
        elif total>=60:
            grade="B"
        elif total>=30:
            grade="D"
          
        return render(request,"Basics/RankList.html",{'fullname':fullname,'rno':rno,'dpt':dpt,'sem':sem,'total':total,'grade':grade})
    else:
        return render(request,"Basics/RankList.html")       
    
def BasicSalaryCalculations(request):
    if request.method=="POST":
        fn=request.POST.get('txt_fname')
        ln=request.POST.get('txt_lname')
        gen=request.POST.get("rd_gender")
        mar=request.POST.get("rd_martial")
        dpt=request.POST.get('sel_dept')
        bs=float(request.POST.get("txt_bs"))

        fullname=fn+""+ln
        if bs>=10000:
            TA=bs*0.40
            DA=bs*0.35
            HRA=bs*0.30
            LIC=bs*0.25
            PF=bs*0.20
        elif bs>=5000 and bs<10000:
            TA=bs*0.35
            DA=bs*0.30
            HRA=bs*0.25
            LIC=bs*0.20
            PF=bs*0.15
        else:
            TA=bs*0.30
            DA=bs*0.25
            HRA=bs*0.20
            LIC=bs*0.15
            PF=bs*0.10

        ded=LIC+PF
        netamt=bs+TA+DA+HRA-(LIC+PF)
        return render(request,"Basics/BasicSalaryCalculations.html",{'fullname':fullname,'TA':TA,'DA':DA,'HRA':HRA,'LIC':LIC,'PF':PF,'gen':gen ,'martial':mar ,'dpt':dpt, 'ded':ded, 'netamt':netamt,'bs':bs})
    else:
        return render(request,"Basics/BasicSalaryCalculations.html")