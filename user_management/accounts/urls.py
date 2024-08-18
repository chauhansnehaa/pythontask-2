from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import  articleDetailView, addPostView,updatePostView, deletePostView, addCategoryView,CategoryView

urlpatterns = [
  
   
    path('', views.home, name='home'), 
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('doctor_dashboard/',views.doctor_dashboard,name='doctor_dashboard'),
    path('patient_dashboard/',views.patient_dashboard,name='patient_dashboard'),
    path('article/<int:pk>', articleDetailView.as_view(), name='article-detail'),
    path('add_post/',addPostView.as_view(), name='addpost'),
    path('article/edit/<int:pk>',updatePostView.as_view(), name='update-post'),
    path('article/<int:pk>/remove',deletePostView.as_view(), name='delete-post'),
    path('addcategory/',addCategoryView.as_view(), name='add-category'),
    path('category/<str:cats>',CategoryView,name='category'),
    path('draft_posts/', views.draft_posts, name='draft-posts'),
    
    # path('media/<path:path>/', views.media, name='media'),  

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
