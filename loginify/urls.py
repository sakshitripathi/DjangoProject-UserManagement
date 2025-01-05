from django.urls import path
from .import views 
urlpatterns = [
    path("hello/",views.print_hello_world),
    path("template/",views.hello_from_template),
    path("signup/",views.signup,name="signup"),
    path("user_login/", views.user_login, name="login"),
    path("success/", views.success, name="success"),
    path("users/", views.get_all_users, name="get_all_users"),
    path("user/<str:email>/", views.get_user_by_email, name="get_user_by_email"),
    path("user/update/<str:email>/", views.update_user, name="update_user"),
    path("user/delete/<str:email>/", views.delete_user, name="delete_user"),
]