from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # api
    path('api/', include(('virtualclass.api.urls', 'virtualclass'), namespace='api')),
    path('api/payment/', include(('payment.urls', 'payment'), namespace='payment_api')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
