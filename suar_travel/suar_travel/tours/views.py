from django.views import generic


# Create your views here.
from .models import Tour


class Home(generic.ListView):
	model = Tour

	template_name = 'index.html'
