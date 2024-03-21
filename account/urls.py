from django.urls import path
from .views import GenerateTwitterOAUTH,GetAccountTwitterDetails, AccountLogin, AccountSignup, AllAccount, GetUserAccount, TelegramBotWebHook

urlpatterns = [
    path("x-oauth", GenerateTwitterOAUTH.as_view()),
    path("get-x-details", GetAccountTwitterDetails.as_view()),
    path("login", AccountLogin.as_view()),
    path("signup", AccountSignup.as_view()),
    path("all", AllAccount.as_view()),
    path("user", GetUserAccount.as_view()),
    path("telegram-bot", TelegramBotWebHook.as_view()),   
]
