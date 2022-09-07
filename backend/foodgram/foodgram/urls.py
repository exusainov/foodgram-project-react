from api.views import IngredientViewSet, RecipeViewSet, TagViewSet
from users.views import CustomUserViewSet

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
#from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet) 
router.register('tags', TagViewSet)
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('api/', include('djoser.urls')),
    #path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')), # auth/token/login/
    path("admin/", admin.site.urls),
    path('', include(router.urls)),
]
#urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
