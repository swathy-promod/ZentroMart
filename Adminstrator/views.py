from django.shortcuts import render,redirect
from Adminstrator.models import * 
from Guest.models import *
from User.models import*


# district 
def District(request):
        district_data=tbl_district.objects.all()
        if request.method=="POST":
                District=request.POST.get("txt_district")
                tbl_district.objects.create(
                        district_name=District)
                return redirect("Admin:District")
        else:
                district_data=tbl_district.objects.all()
        return render(request,"Adminstrator/District.html",{'district':district_data})

# category 
def Category(request):
        category_data=tbl_category.objects.all() 
        if request.method=="POST":
                Category=request.POST.get("txt_category")
                tbl_category.objects.create(
                        Category_name=Category)
                return redirect("Admin:Category")
        else:
               category_data=tbl_category.objects.all() 
        return render(request,"Adminstrator/Category.html",{'category':category_data})

# admin registration 
def adminregistration(request):
        adminregistration_data=tbl_adminregistration.objects.all()  
        if request.method=="POST":
                name=request.POST.get("txt_name")
                contact=request.POST.get("txt_contact")
                email=request.POST.get("txt_email")
                password=request.POST.get("txt_password")
                tbl_adminregistration.objects.create(
                        adminregistration_name=name,
                        adminregistration_contact=contact,
                        adminregistration_email=email,
                        adminregistration_password=password)
                return redirect("Admin:AdminRegistration")
        else:
               adminregistration_data=tbl_adminregistration.objects.all()  
        return render(request,"Adminstrator/AdminRegistration.html",{'adminregistration':adminregistration_data})

# place
def place(request):
        district=tbl_district.objects.all()
        place_data=tbl_place.objects.all()
        if request.method=="POST":
                place=request.POST.get("txt_place")
                pin=request.POST.get("txt_pin")
                district=tbl_district.objects.get(id=request.POST.get("sel_district"))
                tbl_place.objects.create(
                        place_name=place,
                        place_pin=pin,
                        district=district)
                return redirect("Admin:Place")
        return render(request,"Adminstrator/Place.html",{'district':district,'place':place_data})

# sub category
def subcategory(request):
        category=tbl_category.objects.all()
        subcategory_data=tbl_subcategory.objects.all()
        if request.method== "POST":
                subcategory=request.POST.get("txt_subcategory")
                category=tbl_category.objects.get(id=request.POST.get("sel_category"))
                tbl_subcategory.objects.create(
                        subcategory_name=subcategory,
                        Category_name=category)
                return redirect("Admin:SubCategory")
        return render(request,"Adminstrator/SubCategory.html",{'subcategory':subcategory_data,'category':category})

# user list
def userlist(request):
        userlist=tbl_user.objects.all()
        return render(request,"Adminstrator/UserList.html",{'userlist':userlist})

# viewcomplaint
def viewcomplaint(request):
        complaint=tbl_complaint.objects.filter(complaint_status=0)
        replyed=tbl_complaint.objects.filter(complaint_status=1)

        return render(request,"Adminstrator/viewcomplaint.html",{'viewcomplaint':complaint,'replyed':replyed})

# viewfeedback
def viewfeedback(request):
        feedback=tbl_feedback.objects.all()
        return render(request,"Adminstrator/viewfeedback.html",{'viewfeedback':feedback})

# useraccept
def useraccept(request,uid):
        accdata=tbl_user.objects.get(id=uid)
        accdata.user_status=1
        accdata.save()
        return render(request,'Adminstrator/Userlist.html',{'msg':'accepted'})

# userreject
def userreject(request,uid):
        rjedata=tbl_user.objects.get(id=uid)
        rjedata.user_status=2
        rjedata.save()
        return render(request,'Adminstrator/Userlist.html',{'msg':'rejected'})

# homepage
def homepage(request):
        return render(request,"Adminstrator/Homepage.html",{'homepage':homepage})

# reply
def reply(request,id):
    complaint=tbl_complaint.objects.get(id=id)
    if request.method=="POST":
        reply=request.POST.get("txt_reply")
        complaint.complaint_reply=reply
        complaint.complaint_status=1
        complaint.save()
        return redirect("Admin:viewcomplaint")
    return render(request,'Adminstrator/Reply.html')

# district delete
def deletedistrict(request,id):
        tbl_district.objects.get(id=id).delete()
        return redirect("Admin:District")

# category delete
def deletecategory(request,id):
        tbl_category.objects.get(id=id).delete()
        return redirect("Admin:Category")

# admin regisstration delete
def deleteadminregistration(request,id):
        tbl_adminregistration.objects.get(id=id).delete()
        return redirect("Admin:AdminRegistration")

# place delete
def deleteplace(request,id):
        tbl_place.objects.get(id=id).delete()
        return redirect("Admin:Place")

# subcategory delete
def deletesubcategory(request,id):
        tbl_subcategory.objects.get(id=id).delete()
        return redirect("Admin:SubCategory")

# district edit
def editdistrict(request,id):
        district=tbl_district.objects.get(id=id)
        if request.method=="POST":
                districtdata=request.POST.get("txt_district")
                district.district_name=districtdata
                district.save()
                return redirect("Admin:District")
        return render(request,"Adminstrator/District.html",{'editdata':district})
        
# admin registration edit
def editadminregistration(request,id):
        adminregistration=tbl_adminregistration.objects.get(id=id)
        if request.method=="POST":
                adminregistrationname=request.POST.get("txt_name")
                adminregistration.adminregistration_name=adminregistrationname

                adminregistrationcontact=request.POST.get("txt_contact")
                adminregistration.adminregistration_contact=adminregistrationcontact

                adminregistrationemail=request.POST.get("txt_email")
                adminregistration.adminregistration_email=adminregistrationemail

                adminregistrationpassword=request.POST.get("txt_password")
                adminregistration.adminregistration_password=adminregistrationpassword
                adminregistration.save()
                return redirect("Admin:AdminRegistration")
        return render(request,"Adminstrator/AdminRegistration.html",{'editdata':adminregistration})

# category edit       
def editcategory(request,id):
        category=tbl_category.objects.get(id=id)
        if request.method=="POST":
                categorydata=request.POST.get("txt_category")
                category.Category_name=categorydata
                category.save()
                return redirect("Admin:Category")
        return render(request,"Adminstrator/Category.html",{'editdata':category})

# place edit
def editplace(request,id):
        dis=tbl_district.objects.all()
        edit=tbl_place.objects.get(id=id)
        if request.method == "POST":
                name=request.POST.get("txt_place")
                pin=request.POST.get("txt_pin")
                district=tbl_district.objects.get(id=request.POST.get("sel_district"))
                edit.place_name=name
                edit.place_pin=pin
                edit.district=district
                edit.save()
                return redirect("Admin:Place")

        return render(request,"Adminstrator/Place.html",{'editdata':edit,'district':dis})

# subcatgeory edit
def editsubcategory(request,id):
        catg=tbl_category.objects.all()
        edit=tbl_subcategory.objects.get(id=id)
        if request.method=="POST":
                subcategory=request.POST.get("txt_subcategory")
                Category=tbl_category.objects.get(id=request.POST.get("sel_category"))
                edit.subcategory_name=subcategory
                edit.Category_name=Category
                edit.save()
                return redirect("Admin:SubCategory")
        return render(request,"Adminstrator/SubCategory.html",{'editdata':edit,'category':catg})

# sellerlist
def sellerlist(request):
    seller_data=tbl_shop.objects.all()
    return render(request,'Adminstrator/sellerlist.html',{'seller': seller_data})

# selleraccept
def selleraccept(request,sid):
    accdata=tbl_shop.objects.get(id=sid)
    accdata.shop_status = 1
    accdata.save()
    return render(request,'Adminstrator/sellerlist.html',{'msg':"accepted"})

# sellerreject
def sellerreject(request,sid):
    rjdata=tbl_shop.objects.get(id=sid)
    rjdata.shop_status = 2
    rjdata.save()
    return render(request,'Adminstrator/sellerlist.html',{'msg':"rejected"})

# dboylist
def dboylist(request):
    dboy_data=tbl_dboy.objects.all()
    return render(request,'Adminstrator/dboylist.html',{'dboy': dboy_data})

# dboyaccept
def dboyaccept(request,bid):
    accdata=tbl_dboy.objects.get(id=bid)
    accdata.dboy_status = 1
    accdata.save()
    return render(request,'Adminstrator/dboylist.html',{'msg':"accepted"})

# dboyreject
def dboyreject(request,bid):
    rjdata=tbl_dboy.objects.get(id=bid)
    rjdata.dboy_status = 2
    rjdata.save()
    return render(request,'Adminstrator/dboylist.html',{'msg':"rejected"})

# brand
def brand(request):
    brand_data=tbl_brand.objects.all()
    if request.method=="POST":
       brand=request.POST.get("txt_br")
       tbl_brand.objects.create( 
       brand_name=brand)
       return redirect("Admin:Brand")
    else:
        brand_data=tbl_brand.objects.all()
    return render(request,'Adminstrator/Brand.html',{'brand':brand_data})

# brand delete
def deletebrand(request,id):
    tbl_brand.objects.get(id=id).delete()
    return redirect("Admin:Brand")

# brand edit
def editbrand(request,id):
    brand=tbl_brand.objects.get(id=id)
    if request.method=="POST":
       branddata=request.POST.get("txt_br")
       brand.brand_name=branddata
       brand.save()
       return redirect("Admin:Brand")
    return render(request,'Adminstrator/Brand.html',{'editdata':brand})

def logout(request):
    del request.session['uid']
    return redirect("Guest:login")