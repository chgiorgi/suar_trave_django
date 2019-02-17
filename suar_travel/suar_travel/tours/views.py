from django.forms import modelformset_factory
from django.views import generic

from . import form
from .models import Tour, Images


class Home(generic.ListView):
	model = Tour

	template_name = 'index.html'


class TourForms(generic.DetailView):
	model = Tour
	template_name = 'create_tour.html'

	def get(self, request, *args, **kwargs):
		ImageFormSet = modelformset_factory(Images, form=form.ImageForm, extra=3)
		self.tourform = form.ToursForm()
		self.formset = ImageFormSet(queryset=Images.objects.none())
		context = self.get_context_data(object=self.object)
		return self.render_to_response(context)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['tour_form'] = self.tourform
		context['image_form'] = self.formset
		return context


class TourCreate(generic.CreateView):
	pass
