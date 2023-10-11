from django.urls import path
from authentication.views.add_employee import AddEmployeeView
from authentication.views.login_authentication import LoginAuthenticationView, LogoutView
from authentication.views.login_user import LoginUsersView


urlpatterns = [
    path('add/employee/',AddEmployeeView.as_view()),
    path('add/login/user/',LoginUsersView.as_view()),
    path('login/',LoginAuthenticationView.as_view()),
    path('logout/',LogoutView.as_view()),
]