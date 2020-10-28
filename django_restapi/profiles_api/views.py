# from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response #used to return response from APIview when app calls APIVIew
from rest_framework import status #http status codes
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication # is the type of authentication we use for users to authenticate themselves with our API , it works by generating a random token string  when user logs in and every request we make to the api that we need to authenticate, we add this token string to the request 
from rest_framework import filters #drf comes with some modules for filtering 
from rest_framework.authtoken.views import ObtainAuthToken#view that comes with drf that we can use  to generate auth token
from rest_framework.settings import api_settings 
# from rest_framework.permissions import IsAuthenticatedOrReadOnly #make sure viewset is read only if user is not authenticated
from rest_framework.permissions import IsAuthenticated #using this blocks endpoint access except if authenticated user
from profiles_api import serializers #import serializers in the api subdir contained in the serializers.py
from profiles_api import models # import models modules 
from profiles_api import permissions


class HelloAPIView(APIView):
    '''Test API View. This is the APIview class derived from APIView class'''

    serializer_class = serializers.HelloSerialzer #this configures our apiview to have our serializer class defined in serializers.py , i.e whenever making a post,put or get expect a field 'name' with max length 10 

    def get(self, request, format=None):
        '''Returns a list of APIView features'''
        an_apiview = [
            'Uses HTTP methods as functions get, post, patch, put, delete',
            'is similar to a traditional Django view',
            'gives you the most control over your application logic',
            'is mapped manually to urls',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview}) #response object is converted to json, hence response must be dict or list
        
    def post(self, request):
        '''Create a hello message with our name. this also creates a name field on the api since we have defined it here '''
        serializer = self.serializer_class(data = request.data) #first we retrieve the serializer and pass in the data that we get, self.serializer_class is a class that come with apiview and it retrieves the serializer class for our view , the second part assigns the data, when we make a post request, data gets passed in as request.data, we pass this data to the serializer class and define a new variable called serializer

        if serializer.is_valid():#drf serializer provide a way to validate the input as per the specification of our serializers fields, in our case our name is no longer than 10, we validate by calling the is_valid() class
            name = serializer.validated_data.get('name') # this retrieves  the name field that has been validated by serializer
            message = f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
                ) #serializer.errors is a dict of all errors based on validation rules applied by serializer

    def put(self, request, pk=None): #http put is to a specific url primary key/id, but if we do not want to support that we can set it to none with pk 
        '''Handle updating an object'''
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        '''Handle a partial update of an object'''
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        '''Delete an object'''
        return Response({'method':'DELETE'})

class HelloViewSet(viewsets.ViewSet): # based on standard viewset that django provides
    '''Test API ViewSet'''

    serializer_class = serializers.HelloSerialzer #this configures our apiview to have our serializer class defined in serializers.py , i.e whenever making a post,put or get expect a field 'name' with max length 10 

    def list(self, request): # normally like http get, returns ViewSet objects in a list, i.e when a call is made to the root url of api 
        '''Return a hello message'''        

        a_viewset =  [
            "Uses actions (list,create,retrieve,update, partial_update)",
            'Automatically maps URLs using Routers',
            'Provides more functionality with less code',
        ]

        return (Response({'message': 'Hello', 'a_viewset' : a_viewset}))

    def create(self, request):
        '''Create a new hello message'''
        serializer = self.serializer_class(data=request.data) # we pass in the data made in the request and retrieve it with serializer class
        if serializer.is_valid():#drf serializer provide a way to validate the input as per the specification of our serializers fields, in our case our name is no longer than 10, we validate by calling the is_valid() class
            name = serializer.validated_data.get('name') # this retrieves  the name field that has been validated by serializer
            message = f'Hello {name}!'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
                ) #serializer.errors is a dict of all errors based on validation rules applied by serializer

    def retrieve(self, request, pk=None): #retieve an object with primary key
        '''Handle getting an object by its id'''
        return Response({'http_method':'GET'}) # maps/equivalent to http get

    def update(self, request, pk=None):
        '''Handle updating an object'''
        return Response({'http_method':'PUT'})

    def partial_update(self, request, pk=None):
            '''Handle updating part of an object'''
            return Response({'http_method':'PATCH'})                            

    def destroy(self, request, pk=None):
            '''Handle removing an object'''
            return Response({'http_method':'DELETE'})            

class UserProfileViewSet(viewsets.ModelViewSet):
    '''Handle creating and updating profiles. Modelviewset is very similar to a standard viewset except 
    it is specifically designed to manage m odel through our api''' 
    #the way to use a modelviewset is to connect it upto a serializer class just like you would a regular viewset and provide a queryset to modelview set so it knows which objects in db is managed through this viewset

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all() # django has standard operations available once we assign the serializer class and class set to the modelview set            
    authentication_classes = (TokenAuthentication,) # make sure our viewset uses the correct authentication, the comma at the end creates a tuple instead of a single item. we can configure one or more authentication types with a viewset 
    permission_classes = (permissions.UpdateOwnProfile,)# authentication class how the user is authenticated, permission says how the user gets permission to do certain things, so every action in this api viewset is checked against UpdateOwnProfile in permissions.py
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',) # add a filter backend for the search filter which comes with drf and we are going to serach fields name and email 

class UserLoginApiView(ObtainAuthToken): #ObtaiinAuthTOken files can be directly added to urls in urls.py, however it does enable itself in the browsable django site, so we need override this class and make it visible in api making it easier to test
    '''Handle creating user authentication tokens'''     
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES  # default renderer class from api settings (which we imported earlier), it assings renderer class to our obtainauthtoken, we need to add this manually to make it visible 

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    '''Handles creating,reading and updating profile feed items'''
    authentication_classes = (TokenAuthentication,) # token authentication used to authenticate to our end point, comma at end means it get passed as tuple
    serializer_class = serializers.ProfileFeedItemSerializer #this sets serializer class on our viewset to the profilefeed item serializer
    queryset = models.ProfileFeedItem.objects.all() # manage all our profile feed items from our model in our viewset
    permission_classes=(
        permissions.UpdateOwnStatus, #authenticated users can modify only own feed
        # IsAuthenticatedOrReadOnly #user has to be authenticated on viewsets that are not read only
        IsAuthenticated
    )
    def perform_create(self, serializer): #perform_create function allows us to customise behavior for creating objects through model viewset, so when a request gets made to our viewset it gets passed in to our serialzier class and its validate and serializer.save is called, if we need to customise  we use perform_crreate function, this gets called everytime we call a http post
        '''Sets user profile to the logged in user'''
        serializer.save(user_profile=self.request.user) #when a new object is created drf calls perform_Create and it passes in serialzer tht we used to create. the serializer is a modelserialzer which has a save associated with it, which saves the model in the db , in addition to other parameters we also pass in self.request.user, request is passed in every time a request is made to the viewset , this contains all request information including the authenticated user 
         