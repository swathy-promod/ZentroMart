from django.shortcuts import render,redirect
from Guest.models import*
from User.models import *
# homepage
def homepage(request):
    dboydata=tbl_dboy.objects.get(id=request.session['bid'])
    return render(request,"dboy/Homepage.html",{'dboy':dboydata})

# myprofile
def myprofile(request):
    dboy_data=tbl_dboy.objects.get(id=request.session['bid'])
    return render(request,'dboy/Myprofile.html',{'dboy':dboy_data})

def editprofile(request):
    dboydata=tbl_dboy.objects.get(id=request.session['bid'])
    if request.method=="POST":
        dboydata.dboy_name=request.POST.get("txt_n")
        dboydata.dboy_contact=request.POST.get("txt_c")
        dboydata.dboy_email=request.POST.get("txt_e")
        dboydata.dboy_address=request.POST.get("a")
        dboydata.save()
        return render(request,"dboy/Myprofile.html",{'msg':"profile updated"})
    return render(request,"dboy/Editprofile.html",{'dboy':dboydata})

#change password
def changepassword(request):
    dboy=tbl_dboy.objects.get(id=request.session['bid'])
    if request.method=="POST":
        old=request.POST.get("txt_opass")
        new=request.POST.get("txt_npass")
        re=request.POST.get("txt_rpass")

        if dboy.dboy_password == old:
            if new == re:
                dboy.shop_password = new
                dboy.save()
                return render(request,"dboy/Myprofile.html",{"msg":"password changed successfully"})
            else:
                return render(request,'dboy/Changepassword.html',{'msg':"New passward do not match"})
        else:
            return render(request,'dboy/Changepassword.html',{'msg':"old password is incorrect"})
            
    else:
        return render(request,"dboy/Changepassword.html")
    
def viewbooking(request):
    dboy = tbl_dboy.objects.get(id=request.session['bid'])
    place = dboy.place.id
    bookingdata = tbl_booking.objects.filter(tbl_cart__cart_status=4,userid__place=place).order_by('-id')
    return render(request,'dboy/viewbooking.html',{'bookingdata': bookingdata}
    )

def MyOrder(request):
    bookingdata = tbl_booking.objects.filter(tbl_cart__cart_status__gte=5,tbl_cart__deliveryboy__id=request.session['bid']).order_by('-id')
    return render(request,'dboy/MyOrder.html',{'bookingdata': bookingdata}
    )
def order_collect(request, id):
    cart = tbl_cart.objects.get(id=id)
    cart.deliveryboy=tbl_dboy.objects.get(id=request.session['bid'])
    cart.cart_status = 5  
    cart.save()
    return redirect('dboy:Myorder')
def out_for_delivery(request, id):
    cart = tbl_cart.objects.get(id=id)
    cart.cart_status = 6
    cart.save()
    return redirect('dboy:Myorder')
def delivered(request, id):
    cart = tbl_cart.objects.get(id=id)
    cart.cart_status = 7
    cart.save()
    return redirect('dboy:Myorder')



def logout(request):
    del request.session['bid']
    return redirect("Guest:login")