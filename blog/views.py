from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogpost

# Create your views here.

def index(request):
    allPosts = Blogpost.objects.all()
    return render(request, 'blog/index.html',{'allPosts':allPosts})
 
def blogpost(request, id):
    newer = older = 0
    post = Blogpost.objects.filter(post_id=id)[0]

    if len(Blogpost.objects.filter(post_id=id+1))==1:
        newer = Blogpost.objects.filter(post_id=id+1)[0]

    if len(Blogpost.objects.filter(post_id=id-1))==1:
        older = Blogpost.objects.filter(post_id=id-1)[0]
    

    print(older, newer, post)
    return render(request, 'blog/blogpost.html', {'post':post, 'newer':newer, 'older':older})

def search(request):
    found = True
    if request.method == "GET":
        searchVal = request.GET.get('searchVal','')
        allPosts = Blogpost.objects.filter(title__icontains=searchVal) | Blogpost.objects.filter(head0__icontains=searchVal) | Blogpost.objects.filter(head1__icontains=searchVal) | Blogpost.objects.filter(subheading__icontains=searchVal)
        if (len(allPosts)==0):
            found = False
        return render(request, 'blog/search.html',{"Blogposts":allPosts, 'found':found, 'length':len(allPosts)})
    return render(request, 'blog/search.html')
 