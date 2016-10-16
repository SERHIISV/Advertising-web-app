from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from django.contrib import messages


from ads.models import Ad, City, Images
from ads.forms import AdForm, CityForm, ImageForm


class HomePage(ListView):
    model = City
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['cities'] = City.objects.all().order_by('title')
        return context


class AdsCityList(ListView):
    template_name = 'ads.html'
    paginate_by = 5
    context_object_name = 'ads'

    def get_queryset(self):
        return Ad.objects.filter(city__pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(AdsCityList, self).get_context_data(**kwargs)
        context['city'] = City.objects.get(pk=self.kwargs['pk'])
        return context


class Advert(DetailView):
    model = Ad
    template_name = 'ad.html'

    def get_context_data(self, **kwargs):
        context = super(Advert, self).get_context_data(**kwargs)
        context['ad'] = Ad.objects.get(id=self.kwargs.get('pk'))
        if Images.objects.filter(ad=self.kwargs.get('pk')).exists():
            context['images'] = Images.objects.filter(ad=self.kwargs.get('pk'))
        return context


class Addition(CreateView):

    def get(self, request):
        ad_form = AdForm
        image_form_set = formset_factory(ImageForm)
        return render(request, 'addition.html', {'ad_form': ad_form, 'image_form_set': image_form_set})

    def post(self, request):
        ad_form = AdForm(request.POST)
        formset = formset_factory(ImageForm, max_num=5)
        image_form_set = formset(request.POST, request.FILES)
        if ad_form.is_valid() and image_form_set.is_valid():
            new_ad = ad_form.save(commit=False)
            new_ad.save()
            for form in image_form_set.forms:
                if form.cleaned_data:
                    image = form.save(commit=False)
                    image.ad = new_ad
                    image.save()
            messages.success(request, 'Your ad successfully saved!')
            return redirect('/advert/%s/' % new_ad.id)
        else:
            return render(request, 'addition.html', {'ad_form': ad_form, 'image_form_set': image_form_set})


class AddCity(CreateView):
    template_name = 'addcity.html'
    form_class = CityForm
    success_url = '/addition/'

    def form_valid(self, form):
        return super(AddCity, self).form_valid(form)
