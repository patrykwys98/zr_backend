from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.urls import path, include
from . import views
from .views import MyTokenObtainPairView, ChangePasswordView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


schema_view = get_schema_view(
    openapi.Info(
        title="ZR",
        default_version='v1',
        description="Test description",
        contact=openapi.Contact(email="patrykwys98test@snippets.local"),
        license=openapi.License(name="Text License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("email-verify/", views.VerifyEmail.as_view(), name="verify_email"),
    path('change-password/', ChangePasswordView.as_view(),
         name='change-password'),
    path("profiles/", include("profiles.urls")),


    path('', schema_view.with_ui('swagger',
                                 cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),
]
