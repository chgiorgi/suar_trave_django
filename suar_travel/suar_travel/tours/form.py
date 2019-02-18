from django import forms

from .models import Tour, Images


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
