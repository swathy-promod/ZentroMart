from django.shortcuts import render,redirect
from Adminstrator.models import *
from Guest.models import *
from Seller.models import*
from dboy.models import*
from django.core.mail import send_mail
from django.conf import settings
import random

# user
def User(request):
    district=tbl_district.objects.all()
    if request.method == "POST":
        name=request.POST.get("txt_name")
        gender=request.POST.get("rd_gender")
        contact=request.POST.get("txt_contact")
        email=request.POST.get("txt_email")
        address=request.POST.get("txt_address")
        password=request.POST.get("txt_pwd")
        photo=request.FILES.get("file_photo")
        proof=request.FILES.get("file_proof")
        placeid=tbl_place.objects.get(id=request.POST.get("sel_place"))

        tbl_user.objects.create(
            user_name=name,
            user_gender=gender,
            user_contact=contact,
            user_email=email,
            user_address=address,
            user_password=password,
            user_photo=photo,
            user_proof=proof,
            place=placeid  
        )
        return redirect("Guest:User")
    else:
        return render(request,"Guest/NewUser.html",{'district':district})

# ajaxplace
def ajaxplace(request):
    districtid=request.GET.get("did")
    place=tbl_place.objects.filter(district=districtid)
    return render(request,"Guest/AjaxPlace.html",{'place':place})

# login
def login(request):
    if request.method=="POST":
            email=request.POST.get("txt_login")
            password=request.POST.get("txt_password")
            admincount=tbl_adminregistration.objects.filter(adminregistration_email=email,adminregistration_password=password).count()
            usercount=tbl_user.objects.filter(user_email=email,user_password=password).count()
            sellercount=tbl_shop.objects.filter(shop_email=email,shop_password=password).count()
            dboycount=tbl_dboy.objects.filter(dboy_email=email,dboy_password=password).count()
            
            if admincount>0:
                admin=tbl_adminregistration.objects.get(adminregistration_email=email,adminregistration_password=password)
                request.session['aid']=admin.id
                return redirect("Admin:Homepage")
            elif usercount>0:
                user=tbl_user.objects.get(user_email=email,user_password=password)
                if user.user_status == 0:
                    return render(request,"Guest/Login.html",{'msg':"Registration is pending"})
                elif user.user_status == 2:
                    return render(request,"Guest/Login.html",{'msg':"Registration is rejected"})
                else: 
                    request.session['uid']=user.id
                    return redirect("User:Homepage")
            elif sellercount>0:
                seller=tbl_shop.objects.get(shop_email=email,shop_password=password)
                if seller.shop_status == 0:
                    return render(request,"Guest/Login.html",{'msg':"Registration is pending"})
                elif seller.shop_status == 2:
                    return render(request,"Guest/Login.html",{'msg':"Registration is rejected"})
                else: 
                    request.session['sid']=seller.id
                    return redirect("Seller:Homepage")
            elif dboycount>0:
                dboy=tbl_dboy.objects.get(dboy_email=email,dboy_password=password)
                if dboy.dboy_status == 0:
                    return render(request,"Guest/Login.html",{'msg':"Registration is pending"})
                elif dboy.dboy_status == 2:
                    return render(request,"Guest/Login.html",{'msg':"Registration is rejected"})
                else: 
                    request.session['bid']=dboy.id
                    return redirect("dboy:Homepage")
                          
            else:
                return render(request,"Guest/Login.html")
    else:    
        return render(request,"Guest/Login.html")

def shopreg(request):
    district=tbl_district.objects.all()
    if request.method == "POST":
        name=request.POST.get("txt_n")
        contact=request.POST.get("txt_c")
        email=request.POST.get("txt_e")
        address=request.POST.get("txt_a")
        password=request.POST.get("txt_pass")
        photo=request.FILES.get("pho")
        proof=request.FILES.get("pro")
        placeid=tbl_place.objects.get(id=request.POST.get("sel_place"))
        tbl_shop.objects.create(
            shop_name=name,
            shop_contact=contact,
            shop_email=email,
            shop_address=address,
            shop_password=password,
            shop_photo=photo,
            shop_proof=proof,
            place=placeid  
        )
        return redirect("Guest:shopreg")
    else:
        return render(request,"Guest/shopregistration.html",{'district':district})

def dboy(request):
    district=tbl_district.objects.all()
    if request.method == "POST":
        name=request.POST.get("txt_n")
        contact=request.POST.get("txt_c")
        email=request.POST.get("txt_e")
        address=request.POST.get("txt_a")
        password=request.POST.get("txt_pass")
        photo=request.FILES.get("pho")
        proof=request.FILES.get("pro")
        placeid=tbl_place.objects.get(id=request.POST.get("sel_place"))
        tbl_dboy.objects.create(
            dboy_name=name,
            dboy_contact=contact,
            dboy_email=email,
            dboy_address=address,
            dboy_password=password,
            dboy_photo=photo,
            dboy_proof=proof,
            place=placeid  
        )
        return redirect("Guest:dboy")
    else:
        return render(request,"Guest/Deliveryboy.html",{'district':district})


def index(request):
    return render(request,"Guest/index.html")

def forgotpassword(request):
    if request.method == "POST":
        email = request.POST.get("txt_email")
        user = tbl_user.objects.get(user_email=email)
        otp = random.randint(111111,999999)
        request.session["otp"] = otp
        request.session["fid"] = user.id
        send_mail(
            'Forgot password OTP', #subject
            "\rHello \r" + str(otp) +"\n This is the OTP to reset ur password.\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
            settings.EMAIL_HOST_USER,
            [email],
        )
        return render(request,"Guest/Forgotpassword.html",{"msg":email})
    else:
        return render(request,"Guest/Forgotpassword.html")

def otp(request):
    if request.method == "POST":
        inp_otp = int(request.POST.get("txt_otp"))
        if inp_otp == request.session["otp"]:
            return redirect("Guest:newpass")
        else:
            return render(request,"Guest/OTP.html",{"msg":"OTP Does not Matches..!!"})
    else:
        return render(request,"Guest/OTP.html")

def newpass(request):
    if request.method == "POST":
        user = tbl_user.objects.get(id=request.session["fid"])
        if request.POST.get("txt_new_pass") == request.POST.get("txt_con_pass"):
            user.user_password = request.POST.get("txt_con_pass")
            user.save()
            return render(request,"Guest/Newpassword.html",{"msg1":"Password Updated Sucessfully...."})
        else:
            return render(request,"Guest/Newpassword.html",{"msg":"Error in confirm password..!!!"})
    else:
        return render(request,"Guest/Newpassword.html")