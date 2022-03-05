"""wdpy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from websocket import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('faker_data_nga_truemoni', views.faker_data_nga_truemoni ),
    path('faker_data_nga_nairaforever', views.faker_data_nga_nairaforever ),
    path('faker_data_nga_aceloan', views.faker_data_nga_aceloan),
    path('faker_data_nga_moneyaccess', views.faker_data_nga_moneyaccess),
    path('faker_data_ke_kencash', views.faker_data_ke_kencash)
]