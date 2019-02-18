from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.forms import modelformset_factory
from django.urls import reverse
from django.views import generic

from .form import ToursForm, ImageForm, MainImageForm
from .models import Tour, Images


class Home(generic.ListView):
    model = Tour

    template_name = 'index.html'


class TourForms(generic.ListView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Tour
    permission_required = 'add_tour'
    template_name = 'create_tour.html'

    def get_queryset(self):
        self.tourform = ToursForm()
        self.formset = ImageForm()
        self.main_image = MainImageForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tour_form'] = self.tourform
        context['image_form'] = self.formset
        context['MainImageForm'] = self.main_image
        return context


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
