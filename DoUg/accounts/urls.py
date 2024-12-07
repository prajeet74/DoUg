from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from accounts import views

urlpatterns = [
path('token/', views.MyTokenObtainPairView.as_view()),
path('token/refresh/', TokenRefreshView.as_view()),
path('resigter/', views.RegisterView.as_view()),  
path('dashboard/', views.dashboard),
]