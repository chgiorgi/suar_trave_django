from braces.views import SelectRelatedMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.views import generic

from .form import ToursForm, ImageForm, MainImageForm, CommentForm
from .models import Tour, Images, Comment


class Home(generic.ListView):
	model = Tour
	template_name = 'index.html'
	context_object_name = "tours"


class TourCreate(generic.FormView, LoginRequiredMixin, PermissionRequiredMixin):
	permission_required = 'add_tour'
	template_name = 'create_tour.html'

	@transaction.atomic
	def post(self, request, *args, **kwargs):
		context = {}
		tourform = ToursForm(request.POST, request.FILES)
		if tourform.is_valid():
			try:
				tour_form = tourform.save(commit=True)
			except:
				print("error")

			for file in request.FILES.getlist('image'):
				image = Images()
				image.tour = tour_form
				image.image.save(name=file.name, content=file)
				image.save()

			for file in request.FILES.getlist('main_image'):
				image = Images()
				image.is_main = True
				image.tour = tour_form
				image.image.save(name=file.name, content=file)
				image.save()

			context['success'] = True
		else:
			print(tourform.errors)
			for err in tourform.errors:
				context['error'] = tourform[err].errors[0]
		return self.render_to_response(context)

	def get(self, request, *args, **kwargs):
		context = {
			'tour_form': ToursForm(),
			'image_form': ImageForm(),
			'MainImageForm': MainImageForm()
		}
		return self.render_to_response(context)


class Destination(generic.ListView, SelectRelatedMixin):
	template_name = 'destination.html'
	model = Tour
	# select_related = ['images']
	context_object_name = "tours"


class TourDetail(generic.DetailView):
	model = Tour
	template_name = 'tour_detail.html'

	def post(self, request, *args, **kwargs):
		context = {}
		commentform = CommentForm(request.POST, request.user)
		if commentform.is_valid():
			print('55585555555555555555555555555')
			text = request.POST.get('text')
			user = request.user
			tour = self.get_object().id
			comment = Comment.objects.create(text=text, user=user, tour_id=tour)

			context={
				'single_tour': self.get_object(),
				'tour_comments': CommentForm(),
				'tours': Tour.objects.all()
			}
		else:
			print(commentform.errors, 52225663)
			context['error'] = commentform.errors

		return self.render_to_response(context)

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		context = {
			'single_tour': self.object,
			'tours': Tour.objects.all(),
			'tour_comments': CommentForm()
		}
		print(self.object, self.get_context_data(object=self.object))
		print(request)

		return self.render_to_response(context)
