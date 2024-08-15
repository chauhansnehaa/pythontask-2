from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
  
   
    path('', views.home, name='home'), 
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('doctor_dashboard/',views.doctor_dashboard,name='doctor_dashboard'),
    path('patient_dashboard/',views.patient_dashboard,name='patient_dashboard')
    # path('media/<path:path>/', views.media, name='media'),  

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
