from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path(r"api/v1/account/", include('api_account.urls')),
                  path(r"api/v1/task/", include('api_task.urls')),
                  path(r"api/v1/user/", include('api_user.urls')),
                  path(r'api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path(r'api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
