from django.shortcuts import render

# Create your views here.
def submit_app(request):
	if request.method == "POST":
		form = MakeForm(request.POST)
		if form.is_valid():
	