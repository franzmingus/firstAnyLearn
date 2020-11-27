from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request=request,
                  template_name="lists/home.html",
                  context={"site_name": "Lists"})
