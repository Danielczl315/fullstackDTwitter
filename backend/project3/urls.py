"""project3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic.base import TemplateView

from rest_framework.routers import DefaultRouter

# apps 
from users import views as user_views
from posts import views as post_views
from social import views as social_views

router = DefaultRouter()

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("users/", include("django.contrib.auth.urls")),
    path('', include(router.urls)),
    # testing purpose only 
    path('api/signin/', user_views.SignInView.as_view()),
    # user endpoints  
    path('api/signout/', user_views.SignOutView.as_view()),
    path('api/nonce/', user_views.NonceView.as_view()),
    path('api/dashboard/', user_views.DashboardView.as_view()), 
    path('api/onboard/', user_views.OnboardingView.as_view()),
    path('api/userInfo/', user_views.UserInfoView.as_view()), 
    # post endpoints
    path('api/post/', post_views.PostView.as_view()), 
    path('api/likePost/', post_views.LikeView.as_view()),
    path('api/postStats/', post_views.PostStatsView.as_view()),
    path('api/postStatsWithUser/', post_views.PostStatsUserView.as_view()),    
    path('api/reply/', post_views.ReplyView.as_view()),
    path('api/allPost/', post_views.PostView.as_view()),
    path('api/likeReply/', post_views.ReplyLikeView.as_view()),
    path('api/replyStats/', post_views.ReplyStatsView.as_view()),
    path('api/replyStatsWithUser/', post_views.ReplyStatsUserView.as_view()),   
    path('api/postFrom/', post_views.PostFromUserView.as_view()),
    path('api/follow/', social_views.UserFollowingView.as_view()), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
