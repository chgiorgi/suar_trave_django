from braces.views import SelectRelatedMixin, PrefetchRelatedMixin

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction

from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
from .form import ToursForm, ImageForm, MainImageForm, CommentForm, OrderForm, UserProfileForm, VideoForm
from .models import Tour, Images, Comment, Order, UserProfile,Videos
from django.contrib.messages.views import SuccessMessageMixin

User = get_user_model()


class Home(generic.ListView):
    model = Tour
    template_name = 'index.html'
    context_object_name = 'tours'

    # def get(self, request, *args, **kwargs):
    #     tour_object = self.objects.all
    #     context = {
    #         'tours': Tour(),
    #         'get_tours': tour_object
    #     }
    #


class TourCreateForm(generic.FormView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'add_tour'
    template_name = 'create_tour.html'

    def get(self, request, *args, **kwargs):
        context = {
            'tour_form': ToursForm(),
            'image_form': ImageForm(),
            'MainImageForm': MainImageForm(),
            'videoform':VideoForm()
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
            for file in request.FILES.getlist('video'):
                video = Videos()
                video.tour = tour_form
                video.video.save(name=file.name, content=file)
                video.save()

            context['success'] = True
        else:
            print(tourform.errors)
            for err in tourform.errors:
                context['error'] = tourform[err].errors[0]
        return self.render_to_response(context)


class Destination(generic.ListView, SelectRelatedMixin):
    template_name = 'destination.html'
    model = Tour

    context_object_name = 'tours'


class TourDetail(generic.DetailView):
    model = Tour
    template_name = 'tour_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = {
            'single_tour': self.object,
            'tours': Tour.objects.all(),
            'tour_comments': CommentForm(),
            'order_form': OrderForm(),

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
    login_url = '/accounts/login'
    model = Comment

    def post(self, request, *args, **kwargs):
        text = request.POST['editing']
        pk = kwargs['pk']
        self.object = self.get_object()
        Comment.objects.filter(pk=pk).update(text=text)
        return HttpResponseRedirect(reverse('tours:tour_detail', kwargs={'slug': kwargs['slug']}))


class MakeOrder(LoginRequiredMixin, generic.CreateView, SuccessMessageMixin):
    model = Tour
    template_name = 'tour_detail.html'
    login_url = '/accounts/login'

    def post(self, request, *args, **kwargs):

        ordform = OrderForm(request.POST, request.user)
        if ordform.is_valid():
            print(7777777777777777777777777777777777777777777777777777777777777)
            desired_date = ordform.clean_desired_date()
            p_quantity = ordform.clean_person_quantity()
            p_number = ordform.clean_phone_number()
            status = 'pending'
            tour = kwargs['pk']
            user = request.user
            Order.objects.create(tour_id=tour, user=user, status=status, phone_number=p_number,
                                 person_quantity=p_quantity, desired_date=desired_date)
            messages.success(request,
                             "Thanks for booking. \n your tour booked  we will contact you about further details")
            return HttpResponseRedirect(reverse('tours:tour_detail', kwargs={'slug': kwargs['slug']}))
        else:
            messages.success(request,
                             "Please enter correct Phone number")
            return HttpResponseRedirect(reverse('tours:tour_detail', kwargs={'slug': kwargs['slug']}))


class UserProfileView(generic.DetailView):
    model = User
    template_name = 'user_profile.html'

    def get(self, request, *args, **kwargs):
        current_user = User.objects.get(pk=request.user.id)
        print(current_user)
        self.object = self.get_object()
        context = {
            'req_user': current_user,
            'order': Order(),
            'prof_pic': UserProfileForm(),
            'user': self.object
        }
        return self.render_to_response(context)


class UserPicture(generic.FormView, LoginRequiredMixin):
    template_name = 'user_profile.html'
    model = UserProfile

    def post(self, request, *args, **kwargs):
        picform = UserProfileForm(request.POST, request.FILES)
        if picform.is_valid():
            current_user = request.user
            for file in request.FILES.getlist('avatar'):
                prof_pic = UserProfile()
                prof_pic.user = current_user
                prof_pic.avatar.save(name=file.name, content=file)
                prof_pic.save()
            return HttpResponseRedirect(reverse('tours:user_profile', kwargs={'pk': request.user.id}))
        else:
            raise FileNotFoundError


class CancelOrder(generic.DeleteView):
    model = Order
    template_name = 'user_profile.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(reverse('tours:user_profile', kwargs={'pk': kwargs['pk']}))
