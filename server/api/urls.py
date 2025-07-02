from rest_framework.routers import DefaultRouter
from .views import MenuItemViewSet, OrderViewSet, RegisterUserView, LoginView
from django.urls import path

router = DefaultRouter()
router.register(r'menu', MenuItemViewSet, basename='menu')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = router.urls
urlpatterns += [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
