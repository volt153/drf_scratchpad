from rest_framework import serializers
from profiles_api import models #access user profile model we created


class HelloSerialzer(serializers.Serializer): #second Serializer is a class name hence it has a capital S in the beginning
    '''Serializes a name field for testing our api view'''
    name = serializers.CharField(max_length=10)
    

class UserProfileSerializer(serializers.ModelSerializer):
    '''Serializes a user profile object. model serializer is similar to normal serializer but this has extra functionalities
    which make it easier to work with existing django db'''

    class Meta: 
        model = models.UserProfile    # the way to work with ModelSerializer is to use a meta class to configure the serializer to point to a specific model in our project 
        fields = ('id', 'email', 'name', 'password')#list of fields in our model that we want to manage in our serializer 
        extra_kwargs = { # to make password write only 
            'password' : {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    # model serializer allows you to create simple objects in db (it uses default create function of object manager), so we need to override this (to use create_user function we defined instead of the default create function) since we do not want password to be recorded in clear text (since set_password in create_user treats it as password)
    def create(self, validated_data):
        '''Create and return a new user'''

        user = models.UserProfile.objects.create_user(
            emails = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password']
        )

        return

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    '''Serialized profile feed items'''           

    class Meta:
        model = models.ProfileFeedItem # this sets our serializer to our profile feed item created in our models.py this has 3 fields, first one is user profile associated with model, 2nd is status text and 3rd created on
        fields = ('id', 'user_profile', 'status_text', 'created_on') # make above fields available through serializer along with id, django adds primary key for all models created 
        extra_kwargs = {'user_profile':{'read_only':True}} # to make sure user_profile is read only we do this by specifying it in extra_kwargs