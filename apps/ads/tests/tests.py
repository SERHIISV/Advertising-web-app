import datetime

from django.forms import formset_factory
from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from ads.models import Ad, City, Images
from ads.forms import AdForm, ImageForm, CityForm
from ads.views import HomePage, Addition, AddCity, Advert, AdsCityList


class AdsTestCase(TestCase):
    def setUp(self):
        self.city = City.objects.create(title="Ankara")

        self.ad = Ad.objects.create(title="Some title",
                                    content="Some content",
                                    city=City.objects.get(pk=1),
                                    date=datetime.date.today(),
                                    contact="Some contact")

        image_file = open('/media/data/MyFolder/saved images/123.jpg', 'rb').read()
        self.new_image = Images()
        self.new_image.ad = Ad.objects.get(pk=1)
        self.new_image.image = SimpleUploadedFile(
            name='123.jpg',
            content=image_file,
            content_type='image/jpeg'
        )
        self.new_image.save()

        self.factory = RequestFactory()

    def test_models(self):
        ad = Ad.objects.get(pk=1)
        city = City.objects.get(pk=1)
        image = Images.objects.get(ad=ad.id)
        self.assertEqual(ad.title, "Some title")
        self.assertEqual(city.title, "ANKARA")
        self.assertEqual(image.ad.pk, ad.id)

    def test_form_valid(self):
        form_data = {
            'title': "title",
            'content': "content",
            'city': self.city.id,
            'date': datetime.date.today(),
            'contact': "contact"
        }
        form = AdForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        data = {
            'title': '',
            'content': '',
            'date': '',
            'contact': '',
            'city': ''
        }
        form = AdForm(data=data)
        self.assertFalse(form.is_valid())

    def test_image_form_valid(self):
        form_data = {
            'image': self.new_image.image,
            'ad': Ad.objects.get(pk=1)
        }
        form = ImageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_city_form_valid(self):
        form_data = {'title': 'London'}
        form = CityForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_city_form_invalid(self):
        form_data = {'title': ''}
        form = CityForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_home(self):
        request = self.factory.get(reverse('home'))
        response = HomePage.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'home.html')
        self.assertEqual(response.context_data['cities'][0], self.city)

    def test_addcity(self):
        request = self.factory.get(reverse('addcity'))
        response = AddCity.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'addcity.html')

    def test_advert(self):
        request = self.factory.get(reverse('advert', kwargs={'pk': self.ad.id}))
        response = Advert.as_view()(request, pk=self.ad.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'ad.html')

    def test_city_ads(self):
        request = self.factory.get(reverse('adverts', kwargs={'pk': self.city.id}))
        response = AdsCityList.as_view()(request, pk=self.city.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'ads.html')

    # test for addition ads
    def test_addition_get(self):
        response = self.client.get('/addition/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'addition.html')

    def test_addition_post(self):
        data = {
            'form-TOTAL_FORMS': u'1',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
        }
        response = self.client.post('/addition/', data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'addition.html')

        ad_form = response.context['ad_form']
        self.assertIsInstance(ad_form, AdForm)

    def test_addition_html(self):
        response = self.client.get('/addition/')
        self.assertContains(response, '<form')
        self.assertContains(response, 'type="text"', 3)
        self.assertContains(response, 'type="hidden"', 5)
        self.assertContains(response, 'textarea')
        self.assertContains(response, 'type="submit"', 1)

    def test_csrf(self):
        response = self.client.get('/addition/')
        self.assertContains(response, 'csrfmiddlewaretoken')
