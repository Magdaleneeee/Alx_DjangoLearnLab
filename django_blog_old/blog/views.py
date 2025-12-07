from django.shortcuts import render

def index(request):
    """
    Simple view to render the blog home page.
    """
    return render(request, 'blog/index.html')
