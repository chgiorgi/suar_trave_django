from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import modelformset_factory
from django.urls import reverse
from django.views import generic

from . import form
from .models import Tour, Images


class Home(generic.ListView):
	model = Tour

	template_name = 'index.html'


class TourForms(generic.ListView):
	model = Tour
	template_name = 'create_tour.html'

	def get_queryset(self):
		ImageFormSet = modelformset_factory(Images, form=form.ImageForm)
		self.tourform = form.ToursForm()
		self.formset = ImageFormSet(queryset=Images.objects.none())

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['tour_form'] = self.tourform
		context['image_form'] = self.formset
		return context


class TourCreate(generic.RedirectView, LoginRequiredMixin, PermissionRequiredMixin):
	permission_required = 'add_tour'

	def get_redirect_url(self, *args, **kwargs):
		return reverse('tours:index')

	def get(self, request, *args, **kwargs):
		print(kwargs, '55555555555')
		print(request.POST.get('title'),'2222222222222')
		return super().get(request, *args, **kwargs)
