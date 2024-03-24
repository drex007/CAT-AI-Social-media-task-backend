from django.urls import path
from .views import( GenerateTwitterOAUTH,GetAccountTwitterDetails, AccountLogin, AccountSignup, AllAccount, 
                   GetUserTwitterOauthForLogin, TelegramBotWebHook, GetSignedUpUser, RedeemReferralCode, UpdateAccountTelegram
)
urlpatterns = [
    path("x-oauth", GenerateTwitterOAUTH.as_view()),
    path("get-x-details", GetAccountTwitterDetails.as_view()),
    path("login", AccountLogin.as_view()),
    path("signup", AccountSignup.as_view()),
    path("all", AllAccount.as_view()),
    path("login-x-oauth", GetUserTwitterOauthForLogin.as_view()),
    path("telegram-bot", TelegramBotWebHook.as_view()),
    path("user", GetSignedUpUser.as_view()),  
    path("redeem-code", RedeemReferralCode.as_view()),  
    path("update-telegram", UpdateAccountTelegram.as_view()),   
]
