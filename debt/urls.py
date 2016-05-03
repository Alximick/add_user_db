from django.conf.urls import url, include, patterns
import debt.views

urlpatterns = [
    url(r'^debt/$', debt.views.mydebt, name='mydebt'),
    url(r'^debt/(?P<year>\w+)/$', debt.views.mydebt, name='mydebt'),
    # url(r'^$', loginsys.views.login),
]

