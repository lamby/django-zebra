from django.conf.urls.defaults import url
from marty import views

urlpatterns = (
    url(r'update$',     views.update,          name='update'),
)
