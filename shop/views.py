from django.shortcuts import render
from django.http import HttpResponse, response
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json

# Create your views here.
def index(request):
    allProds = []
    catProds = Product.objects.values('category','id')
    cats = {item['category'] for item in catProds}

    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = ceil(n/4)
        allProds.append([prod, range(1,nSlides), nSlides])

    params = {'allProds':allProds}
    return render(request, 'shop/index.html',params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name','')
        email= request.POST.get('email','')
        phone= request.POST.get('phone','')
        desc= request.POST.get('desc','')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html',{'thank':thank})

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId','')
        email = request.POST.get('email','')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                # allProds = Product.objects.all()
                # prices = dict()
                # for item in allProds:
                #     prices['pr'+str(item.id)] = item.price
                for item in update:
                    updates.append({'text':item.update_desc, 'time':item.timestamp})
                    # response = json.dumps([updates, order[0].items_json, json.dumps( prices)], default=str)                      
                    response = json.dumps({'status':'success',"updates":updates, "items_json":order[0].items_json}, default=str)                      
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noItem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')


def search(request):
    found = True
    if request.method == "GET":
        searchVal = request.GET.get('searchVal','')
        allProds = Product.objects.filter(product_name__icontains=searchVal) | Product.objects.filter(desc__icontains=searchVal) | Product.objects.filter(category__icontains=searchVal) | Product.objects.filter(subcategory__icontains=searchVal)
        if (len(allProds)==0):
            found = False
        return render(request, 'shop/search.html',{"products":allProds, 'found':found, 'length':len(allProds)})
    return render(request, 'shop/search.html')

def productView(request,myid): 
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product':product[0]})
    
def checkout(request):
    # To display cart item's price
    # allProds = Product.objects.all()
    # products = dict()
    # for item in allProds:
    #     products['pr'+str(item.id)] = item.price
        
    # params = {'products':products}
    thank = False
    if request.method=="POST":
        firstName = request.POST.get('firstName','')
        lastName = request.POST.get('lastName','')
        username = request.POST.get('username','')
        amount = request.POST.get('amount','')
        email= request.POST.get('email','')
        address= request.POST.get('address','') +" "+ request.POST.get('address2','')
        country= request.POST.get('country','')
        phone= request.POST.get('phone','')
        state= request.POST.get('state','')
        zip_code= request.POST.get('zip_code','')
        items_json= request.POST.get('itemsJson','')
        order = Order(name=firstName+" "+lastName, username=username, email=email, address=address, country=country, state=state, zip_code=zip_code, phone=phone, items_json=items_json, amount=amount)
        order.save()

        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        params = {'id': id, 'thank':thank}
        return render(request, 'shop/checkout.html', params)

    return render(request, 'shop/checkout.html')