"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from library_service.views.catalog import *
from library_service.views.basket import *
from library_service.views.profile import *
from library_service.views.order import *

router = DefaultRouter()
router.register("book", BookViewset, basename="book")
router.register("library", LibraryViewset, basename="library")
router.register("scenario", ScenarioViewset, basename="scenario")
router.register("basket", BasketViewset, basename="basket")
router.register("profile", ProfileViewset, basename="profile")
router.register("order", OrderViewset, basename="order")
router.register("borrowed", BorrowedViewset, basename="borrowed")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', TokenObtainPairView.as_view()),
    path('api/auth/refresh/', TokenRefreshView.as_view()),
    path('api/auth/logout/', TokenBlacklistView.as_view()),
    path("api/", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
