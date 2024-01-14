
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog
from manage_users.views.login_views import LogoutView, UserLoginView

class IndexPage(TemplateView):
    template_name = 'dashboard.html'

urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('jsi18n', JavaScriptCatalog.as_view(), name='javascript-catalog'),    
    path("", include('manage_users.urls'), name="manage_users"),
    path("", include('pasien.urls'), name="manage_pasien"),
    path("", include('master_data.urls'), name="manage_layanan"),
    path("", include('surat.urls'), name="surat"),
    path("auth/", include([
        path("login/", UserLoginView.as_view(), name="login"),
        path("logout/", LogoutView.as_view(), name="logout"),
    ])),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)