"""
URL configuration for GloriousProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static


from accounts.views import home_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('administration/', include('administration.urls')),
    path('staff/', include('staff.urls')),
    path('students/', include('students.urls')),
    path('superuser/', include('superuser.urls')),
    # path('parent/', include('parent.urls')),
    path('schoolevents/', include('schoolevents.urls')),
    # path('notification/', include('notification.urls')),
    path('fees/', include('fees.urls')),
    # path('online_payments/', include('online_payments.urls')),
    path('birthdays/', include('birthdays.urls')),
    path('chat/', include('chat.urls')),
    path('reportcard/', include('reportcard.urls')),

    
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
