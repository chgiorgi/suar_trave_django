from django import forms

from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import Tour, Images, Comment, Order, UserProfile, Videos
from django.forms.widgets import SelectDateWidget

from phonenumber_field.formfields import PhoneNumberField


class ToursForm(forms.ModelForm):
    title = forms.CharField(max_length=250, min_length=2)
    destination = forms.CharField(min_length=2)
    description = forms.Textarea()
    price = forms.IntegerField(required=True)
    duration = forms.DurationField(required=True)
    active = forms.BooleanField()

    class Meta:
        model = Tour
        fields = ('title', 'destination', 'description', 'price', 'duration', 'active')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'comment-textarea'}),
        }


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image ', widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Images
        fields = ('image',)


class MainImageForm(forms.ModelForm):
    main_image = forms.ImageField(label='Main Image ', widget=forms.ClearableFileInput())

    class Meta:
        model = Images
        fields = ('main_image',)


class OrderForm(forms.ModelForm):
    desired_date = forms.DateField(widget=SelectDateWidget)
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget)
    person_quantity = forms.IntegerField(required=True)

    class Meta:
        model = Order
        fields = ('desired_date', 'person_quantity', 'phone_number')

    def clean_desired_date(self):
        clean_d_date = self.cleaned_data['desired_date']
        return clean_d_date

    def clean_phone_number(self):
        clean_p_number = self.cleaned_data['phone_number']
        return clean_p_number

    def clean_person_quantity(self):
        clean_p_quantity = self.cleaned_data['person_quantity']
        return clean_p_quantity

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['desired_date'].widget.attrs.update({'class': 'field-form'})
        self.fields['phone_number'].widget.attrs.update({'class': 'field-form'})
        self.fields['person_quantity'].widget.attrs.update({'class': 'field-form'})


class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(label='Profile Pic', widget=forms.ClearableFileInput())

    class Meta:
        model = UserProfile
        fields = ('avatar',)


class VideoForm(forms.ModelForm):
    video = forms.FileField(label='Upload Videos', widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Videos
        fields = ('video',)
