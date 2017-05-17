import os
import sys

from django.conf import settings

DEBUG = os.environ.get('DEBUG','on') == 'on'

SECRET_KEY = os.environ.get('SECRET_KEY','nmu5jz=jg^_z(jn+zj3_m)qbo*-go=5!em%nb%x*d6$j#tb(#3')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS','127.0.0.1').split(',')


settings.configure(
    DEBUG = DEBUG,
    SECRET_KEY = SECRET_KEY,
    ALLOWED_HOSTS = ALLOWED_HOSTS,
    ROOT_URLCONF = __name__,
    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)

from django import forms
from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from io import BytesIO
from PIL import Image

class ImageForm(forms.Form):
    """Form to validate requested placeholder image."""

    height = forms.IntegerField(min_value=1, max_value = 2000)
    width = forms.IntegerField(min_value=1, max_value = 2000)

    def generate (self,image_format='PNG'):
        """Generate an image of the given type and return as raw bytes."""
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        image = Image.new('RGB',(width,height))
        content = BytesIO()
        image.save(content,image_format)
        content.seek(0)
        return content


def placeholder(request,width,height):
    form = ImageForm({'height':height,'width':width})
    if form.is_valid():
        image = form.generate()
        return HttpResponse(image,content_type='image/png')
    else:
        return HttpResponseBadRequest('Invalid Image Request')

def index (request):
    return HttpResponse('Hello world')

urlpatterns = (
    url(r'^$ image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', placeholder, name='placeholder'),
    url(r'^$', index, name='homepage'),
)


application = get_wsgi_application()

if __name__ == '__main__':
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
