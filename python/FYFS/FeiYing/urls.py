"""FeiYing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls
from FeiYing.settings import DEBUG
from FeiYing.index import Index, rest_static
from diskview.views import DiskManageView, RaidManageView
from gfsview.views import GfsStateView, GfsVolumeView
from logview.views import UserLogView
api = [
    url('disk', DiskManageView.as_view(), name='disk'),
    url('raid', RaidManageView.as_view(), name='raid'),
    url('gfs$', GfsStateView.as_view(), name='gfs'),
    url('gfs/volume', GfsVolumeView.as_view(), name='volume'),
    url('log', UserLogView.as_view(), name='log')

]
urlpatterns = [
    url('admin/', admin.site.urls),
    url("^docs/", include_docs_urls(title="LDFS API VIEW")),
    url('^ldfs$', Index.as_view(), name='index'),
    #url(r'ldfs/static/rest_framework/(?P<filename>.*)$', rest_static, name='rest_static'),
    url('^ldfs/api/v1/', include(api))
]
if DEBUG:
    urldebug = [
        url(r'ldfs/static/rest_framework/(?P<filename>.*)$', rest_static, name='rest_static'),
    ]
    urlpatterns += urldebug
