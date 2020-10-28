from django.urls import path, include 
from profiles_api import views # file containing view
from rest_framework.routers import DefaultRouter #for Viewset


router = DefaultRouter() #assign default router to variable
router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset') #register our specific viewset with router at address hello-viewset, since router is going to assign urls we dont need to specify the forward slash, base name is used for url retrieving , base_name deprecated use basename
router.register('profile', views.UserProfileViewSet) # we dont have to specify base name since in our viewset in the views.py we have a queryset , it is derived from here, using basename would override this behavior
router.register('feed', views.UserProfileFeedViewSet)

urlpatterns = [
    path('hello-view/', views.HelloAPIView.as_view()), #call as_view() on our APIView class, which gets mapped to the get function
    path('login/',views.UserLoginApiView.as_view()), #enable login in drf
    path('', include(router.urls)) #as you register new routes with router it generates a list of urls associated for our viewset, it figures out urls for all of the functions we add to our viewset and returns it as a list in routers.urls. '' means we dont want to add any prefix
]