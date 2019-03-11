from braces.views import SelectRelatedMixin, PrefetchRelatedMixin

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction

from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from .form import ToursForm, ImageForm, MainImageForm, CommentForm
from .models import Tour, Images, Comment


class Home(generic.ListView):
    model = Tour
    template_name = 'index.html'
    context_object_name = "tours"


class TourCreateForm(generic.FormView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'add_tour'
    template_name = 'create_tour.html'

    #
    # @transaction.atomic
    # def post(self, request, *args, **kwargs):
    # 	context = {}
    # 	tourform = ToursForm(request.POST, request.FILES)
    # 	if tourform.is_valid():
    # 		try:
    # 			tour_form = tourform.save(commit=True)
    # 		except:
    # 			print("error")
    #
    # 		for file in request.FILES.getlist('image'):
    # 			image = Images()
    # 			image.tour = tour_form
    # 			image.image.save(name=file.name, content=file)
    # 			image.save()
    #
    # 		for file in request.FILES.getlist('main_image'):
    # 			image = Images()
    # 			image.is_main = True
    # 			image.tour = tour_form
    # 			image.image.save(name=file.name, content=file)
    # 			image.save()
    #
    # 		context['success'] = True
    # 	else:
    # 		print(tourform.errors)
    # 		for err in tourform.errors:
    # 			context['error'] = tourform[err].errors[0]
    # 	return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        context = {
            'tour_form': ToursForm(),
            'image_form': ImageForm(),
            'MainImageForm': MainImageForm()
        }
        return self.render_to_response(context)


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


class Destination(generic.ListView, SelectRelatedMixin):
    template_name = 'destination.html'
    model = Tour
    # select_related = ['images']
    context_object_name = "tours"


class TourDetail(generic.DetailView):
    model = Tour
    template_name = 'tour_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = {
            'single_tour': self.object,
            'tours': Tour.objects.all(),
            'tour_comments': CommentForm()
        }
        # print(self.object, self.get_context_data(object=self.object))
        # print(request)

        return self.render_to_response(context)


class CreateComment(generic.CreateView, LoginRequiredMixin):
    model = Tour
    template_name = 'tour_detail.html'
    login_url = '/accounts/login'

    def post(self, request, *args, **kwargs):
        context = {}
        commentform = CommentForm(request.POST, request.user)
        if commentform.is_valid():
            text = request.POST.get('text')
            user = request.user
            tour = self.get_object().id
            comment = Comment.objects.create(text=text, user=user, tour_id=tour)
            self.object = self.get_object()


        else:
            context['error'] = commentform.errors
        return HttpResponseRedirect(reverse('tours:tour_detail', kwargs=kwargs))


class DeleteComment(generic.DeleteView):
    model = Comment
    template_name = 'tour_detail.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(reverse('tours:tour_detail', kwargs={'slug': kwargs['slug']}))


class EditComment(LoginRequiredMixin, generic.UpdateView):
    login_url = 'user_management/login/'
    model = Comment

    def post(self, request, *args, **kwargs):
        text = request.POST['editing']
        pk=kwargs['pk']
        self.object = self.get_object()
        Comment.objects.filter(pk=pk).update(text=text)
        return HttpResponseRedirect(reverse('tours:tour_detail', kwargs={'slug': kwargs['slug']}))
