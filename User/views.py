from django.shortcuts import render,redirect
from User.models import*
from Guest.models import*
from Seller.models import*
from django.db.models import Sum
from django.http import JsonResponse

# homepage
def Homepage(request):
    userdata=tbl_user.objects.get(id=request.session['uid'])
    return render(request,"User/Homepage.html",{'user':userdata})

# myprofile
def myprofile(request):
    userdata=tbl_user.objects.get(id=request.session['uid'])
    return render(request,"User/Myprofile.html",{'user':userdata})

# editprofile
def editprofile(request):
    userdata=tbl_user.objects.get(id=request.session['uid'])
    if request.method=="POST":
        userdata.user_name=request.POST.get("txt_name")
        userdata.user_contact=request.POST.get("txt_contact")
        userdata.user_email=request.POST.get("txt_email")
        userdata.user_address=request.POST.get("address")
        userdata.save()
        return render(request,"User/Myprofile.html",{'msg':"profile updated"})
    return render(request,"User/Editprofile.html",{'user':userdata})
# changepassword
def changepassword(request):
    user=tbl_user.objects.get(id=request.session['uid'])
    if request.method=="POST":
        old=request.POST.get("txt_opass")
        new=request.POST.get("txt_npass")
        re=request.POST.get("txt_rpass")

        if user.user_password == old:
            if new == re:
                user.user_password = new
                user.save()
                return render(request,"User/Myprofile.html",{"msg":"password changed successfully"})
            else:
                return render(request,'User/Changepassword.html',{'msg':"New passward do not match"})
        else:
            return render(request,'User/Changepassword.html',{'msg':"old password is incorrect"})
            
    else:
        return render(request,"User/Changepassword.html")
                      
# complaint
def complaint(request):
    complaint=tbl_complaint.objects.all()
    user=tbl_user.objects.get(id=request.session['uid'])
    if request.method=="POST":
        title=request.POST.get("txt_title")
        content=request.POST.get("complaint")
        tbl_complaint.objects.create(
            complaint_title=title,
            complaint_content=content,
            user=user
        )
        return redirect("User:complaint")
    else:
        return render(request,"User/Complaint.html",{"complaint":complaint}) 

# feedback
def feedback(request):
    feedback=tbl_feedback.objects.all()
    if request.method =="POST":
        content=request.POST.get("content")
        user=tbl_user.objects.get(id=request.session['uid'])
        tbl_feedback.objects.create(
        feedback_content=content,
        user=user
        )
        return redirect("User:feedback")
    return render(request,"User/Feedback.html",{"feedback":feedback})

def viewproduct(request):
    product=tbl_product.objects.all()
    category=tbl_category.objects.all()
    brands=tbl_brand.objects.all()
    ar = [1, 2, 3, 4, 5]
    parry = []
    for i in product:
        total_stock = tbl_stock.objects.filter(
            productid=i.id
        ).aggregate(total=Sum('stock_quality'))['total'] or 0

        total_cart = tbl_cart.objects.filter(
            productid=i.id,
            cart_status__gt=1
        ).aggregate(total=Sum('cart_quantity'))['total'] or 0

        i.total_stock = total_stock - total_cart
        print(i.total_stock)
        

    return render(request,"User/viewproduct.html",{'brand':brands,'category':category,'product':product,'ar':ar})
    
def viewmore(request, pid):
    product = tbl_product.objects.get(id=pid)
    gallery = tbl_gallery.objects.filter(productid=product)

    total_stock = tbl_stock.objects.filter(
        productid=product
    ).aggregate(total=Sum('stock_quality'))['total'] or 0

    total_cart = tbl_cart.objects.filter(
        productid=product,
        cart_status__gt=1
    ).aggregate(total=Sum('cart_quantity'))['total'] or 0

    available = total_stock - total_cart

    ratecount = tbl_rating.objects.filter(product=product).count()
    avg = 0

    if ratecount > 0:
        tot = tbl_rating.objects.filter(product=product)\
            .aggregate(total=Sum('rating_data'))['total'] or 0
        avg = tot // ratecount

    shop = product.shop
    ar = [1, 2, 3, 4, 5]  

    return render(request, 'User/Viewmore.html', {
        'product': product,
        'gallery': gallery,
        'available': available,
        'avg': avg,
        'ratecount': ratecount,
        'shop': shop,
        'ar': ar
    })

def viewcart(request,id):
    viewcart=tbl_cart.objects.get(id=id)

    return render(request,'User/Viewcart.html')

def addtocart(request,pid):
    productdata=tbl_product.objects.get(id=pid)
    userdata=tbl_user.objects.get(id=request.session['uid'])
    bookingcount=tbl_booking.objects.filter(booking_status=0,userid=userdata).count()
    if bookingcount>0:
        booking=tbl_booking.objects.get(booking_status=0,userid=userdata)
        cartcount=tbl_cart.objects.filter(bookingid=booking,productid=productdata).count()
        if cartcount>0:
          return render(request,"User/Viewproduct.html",{"msg":"Product already added to cart"})    
        else:
            tbl_cart.objects.create(
                productid=productdata,bookingid=booking
            )
            return render(request,"User/Viewproduct.html",{"msg":"Product is added to cart"})   
    else:
        booking=tbl_booking.objects.create(userid=userdata)
        tbl_cart.objects.create(
                productid=productdata,bookingid=booking
            )
        return render(request,"User/Viewproduct.html",{"msg":"Product is added to cart"})
    

def mycart(request):
    if request.method=="POST":
        bookingdata=tbl_booking.objects.get(id=request.session["bookingid"])
        bookingdata.booking_amount=request.POST.get("carttotalamt")
        bookingdata.booking_status=1
        bookingdata.save()
        cart = tbl_cart.objects.filter(bookingid=bookingdata)
        for i in cart:
                i.cart_status = 1
                i.save()
        return redirect("User:payment",request.session["bookingid"])
    else:
        bookcount = tbl_booking.objects.filter(userid=request.session["uid"],booking_status=0).count()
        if bookcount > 0:
                book = tbl_booking.objects.get(userid=request.session["uid"],booking_status=0)
                request.session["bookingid"] = book.id
                cart = tbl_cart.objects.filter(bookingid=book)
                for i in cart:
                    total_stock = tbl_stock.objects.filter(productid=i.productid.id).aggregate(total=Sum('stock_quality'))['total']
                    total_cart = tbl_cart.objects.filter(productid=i.productid.id, cart_status=1).aggregate(total=Sum('cart_quantity'))['total']
                    if total_stock is None:
                            total_stock = 0
                    if total_cart is None:
                            total_cart = 0
                    total =  total_stock - total_cart
                    i.total_stock = total
                return render(request,"User/Mycart.html",{'cartdata':cart})
        else:
                return render(request,"User/Mycart.html")

def DelCart(request,did):
   tbl_cart.objects.get(id=did).delete()
   return redirect("User:Mycart")

def CartQty(request):
   qty=request.GET.get('QTY')
   cartid=request.GET.get('ALT')
   cartdata=tbl_cart.objects.get(id=cartid)
   cartdata.cart_quantity=qty
   cartdata.save()
   return redirect("User:Mycart") 

def mybooking(request):
    uid=request.session['uid']
    bookingdata=tbl_booking.objects.filter(userid=uid, booking_status__gt=0).order_by('-id')
    return render(request,'User/mybooking.html',{'bookingdata':bookingdata})

def payment(request,id):
    bookingdata=tbl_booking.objects.get(id=id)
    amount=bookingdata.booking_amount
    if request.method=="POST":
        bookingdata.booking_status=2
        bookingdata.save()
        cart = tbl_cart.objects.filter(bookingid=bookingdata)
        for i in cart:
            i.cart_status = 2
            i.save()
        return redirect('User:mybooking')
    return render(request,'User/Payment.html',{'amt':amount})

def rating(request,mid):
    parray = [1, 2, 3, 4, 5] # This array creates the 5 stars
    stardata = tbl_rating.objects.filter(product=mid).order_by('-datetime')
    counts = stardata.count()
    
    context = {
        'mid': mid,
        'ar': parray, # ALWAYS send this
        'data': stardata,
        'count': counts,
    }

    if counts > 0:
        res = sum(i.rating_data for i in stardata)
        context['avg'] = res // counts
    else:
        context['avg'] = 0

    return render(request, "User/Rating.html", context)



def viewrating(request,mid):
    parray = [1, 2, 3, 4, 5] # This array creates the 5 stars
    stardata = tbl_rating.objects.filter(product=mid).order_by('-datetime')
    counts = stardata.count()
    
    context = {
        'mid': mid,
        'ar': parray, # ALWAYS send this
        'data': stardata,
        'count': counts,
    }

    if counts > 0:
        res = sum(i.rating_data for i in stardata)
        context['avg'] = res // counts
    else:
        context['avg'] = 0

    return render(request, "User/ViewRating.html", context)
def ajaxstar(request):
    parray=[1,2,3,4,5]
    rating_data=request.GET.get('rating_data')
    
    user_review=request.GET.get('user_review')
    pid=request.GET.get('pid')
    # wdata=tbl_booking.objects.get(id=pid)
    tbl_rating.objects.create(user=tbl_user.objects.get(id=request.session['uid']),user_review=user_review,rating_data=rating_data,product=tbl_product.objects.get(id=pid))
    stardata=tbl_rating.objects.filter(product=pid).order_by('-datetime')
    return render(request,"User/AjaxRating.html",{'data':stardata,'ar':parray})

def starrating(request):
    r_len = 0
    five = four = three = two = one = 0
    # cdata = tbl_booking.objects.get(id=request.GET.get("pdt"))
    rate = tbl_rating.objects.filter(product=request.GET.get("pdt"))
    ratecount = tbl_rating.objects.filter(product=request.GET.get("pdt")).count()
    for i in rate:
        if int(i.rating_data) == 5:
            five = five + 1
        elif int(i.rating_data) == 4:
            four = four + 1
        elif int(i.rating_data) == 3:
            three = three + 1
        elif int(i.rating_data) == 2:
            two = two + 1
        elif int(i.rating_data) == 1:
            one = one + 1
        else:
            five = four = three = two = one = 0
        # print(i.rating_data)
        # r_len = r_len + int(i.rating_data)
    # rlen = r_len // 5
    # print(rlen)
    result = {"five":five,"four":four,"three":three,"two":two,"one":one,"total_review":ratecount}
    return JsonResponse(result)



def logout(request):
    del request.session['uid']
    return redirect("Guest:login")