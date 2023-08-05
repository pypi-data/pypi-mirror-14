import django

if django.get_version() >= '1.9':

	from django.conf.urls import url
	from cajax.views import cajax_view

	urlpatterns = [
		url(r'^cajax/', cajax_view, name='cajax-url'),
	]

else:

	from django.conf.urls import patterns, url

	urlpatterns= patterns('cajax.views',
		url(r'^cajax/', 'cajax_view', name='cajax-url'),
	)
