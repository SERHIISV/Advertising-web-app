from django import forms
from django.core.exceptions import ValidationError

from ads.models import Ad, Images, City


class AdForm(forms.ModelForm):

    class Meta:
        model = Ad
        fields = '__all__'


class ImageForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Images
        fields = ['image']


class CityForm(forms.ModelForm):
    title = forms.CharField(max_length=255)

    class Meta:
        model = City
        fields = '__all__'

    def clean_title(self):
        title = self.cleaned_data['title'].upper()

        if City.objects.filter(title=title).exists():
            message = u"City %s has already exist." % title
            raise ValidationError(message)
        else:
            return title
