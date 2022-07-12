from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import CreateUserView, LoginView, UpdatePasswordView, MeView


router = DefaultRouter(trailing_slash=False)
router.register("create-user", CreateUserView, "create user")
router.register("login", LoginView, "login")
router.register("update-password", UpdatePasswordView, "update password")
router.register("me", MeView, "me")
router.register("activities", views.UserActivitiesView, "activities log")
router.register("users", views.UsersView, "users")

urlpatterns = [path("", include(router.urls))]
