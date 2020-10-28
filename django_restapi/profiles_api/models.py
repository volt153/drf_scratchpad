from django.db import models
from django.contrib.auth.models import AbstractBaseUser #standard base classes that need to be imported when overriding the default django user model
from django.contrib.auth.models import PermissionsMixin #standard base classes that need to be imported when overriding the default django user model
from django.contrib.auth.models import BaseUserManager
from django.conf import settings #import settings.py from our django project (specifically auth model)
# Create your models here. 


class UserProfileManager(BaseUserManager):
    '''Manager for class UserProfile - by default when django creates new user it creates one with username and password fields, but we have replaced username with email field, so custom user manager handles creating user with email field instead of username. the way managers is used is that we specify functions which can be used to manipulate the objects for which the manager is for, UserProfile class in our case'''

    def create_user(self, email, name, password=None):
        '''create a new user profile - this function is used by django cli when creating user'''
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email) #normalize to all lower case
        user = self.model(email=email, name=name) #creates new model that the model manager is representing , self.model is set to the model UserProfile here, and it sets the email and name for that model

        user.set_password(password) # so that password is encrypted as hash and not stored as plain text, done by set_password function
        user.save(using=self._db) #django supports several db types

        return user #return the custom user object

    def create_superuser(self, email, name, password): #password cannot be null for superuser
        '''Create and save a new superuser with given details'''
        user = self.create_user(email, name, password) #calls create_user method, here self is not specified as arg since it is passed automatically when function/method (create_user in this case) is called

        user.is_superuser = True #is_superuser is automatically created by PermissionsMixin base class
        user.is_staff = True #is_staff is specified in the UserProfile class
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    '''Database model for users in the system'''
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email' # since we are overriding username with email field
    REQUIRED_FIELDS = ['name'] #addition to email we also specify name as required field

    def get_full_name(self): #function inside class must have self as first argument , these functions are required for django to interact with our custom class
        '''Retrieve full name of user'''
        return self.name

    def get_short_name(self):
        '''Retrieve short name of user'''
        return self.name

    def __str__(self): #this is recommended for all django models to make sure input is being interpreted correctly as a feedback output, you will see this in action in the django admin where all users are listed by their email id
        '''return string representation of user'''
        return self.email

class ProfileFeedItem(models.Model):
    '''Profile status update - model to store status update in system, so every time they create a new update its going to create a new profilefeeditem object and associate it with the user '''        
    #the way you link models with other models in django is  with foreign key, when foreign key field is used it sets up a foreign key relationship in the db to a remote model
    #this allows to make sure the integrity of the db is maintained, so you can never create a profile feed item for a user profile that does not exist

    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL, #normally first argument is the foriegn model that ProfileFeedItem is linked to, here we are using a reference to keep it dynamic, this retrieves the auth_user_model from settings.py file, if a different model needs to be used it can be changed here
        on_delete=models.CASCADE # what to do if remote entry in linked model is deleted, if user profile is delete what should happen to the profile feed item associated with it, cascade tells cascade the changes the down the models, so remove the profile feed, or other option is to set null       
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateField(auto_now_add=True) # automatically add datetime the item was created

    def __str__ (self): #add string representation of model, to tell python what to do when we convert a model instance into a string 
        '''Return the model as a string'''
        return self.status_text # return status text
