from django.urls import path
from User import views as user

urlpatterns = [
    path('login/', user.user_login, name='login'),
    path('logout/', user.user_logout, name='logout'),
    path('signup/', user.user_signup, name='signup'),
]
