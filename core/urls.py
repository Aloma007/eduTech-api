from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView  # <--- Import these!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('exams.urls')),
    path('api-auth/', include('rest_framework.urls')),

    # --- SWAGGER DOCUMENTATION URLS ---
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # The hidden JSON blueprint
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # The beautiful UI!
]