from django.urls import path
from .views import AuthenticationView, VerifyCodeView, ProfileView, ReferralInputView

urlpatterns = [
    path('auth/', AuthenticationView.as_view(), name='auth'),
    path('verify/', VerifyCodeView.as_view(), name='verify'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/referral/', ReferralInputView.as_view(), name='referral'),
]