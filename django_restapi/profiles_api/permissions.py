from rest_framework import permissions #provides base class to create permissions

class UpdateOwnProfile(permissions.BasePermission): # it is base permission that drf provides for making custom permission classes 
    '''Allow users to edit their own profile'''

    #add has_object_permission function to the class which gets called every time a request is made to the api to which we assign the permissions to , this function would return a true or a false to determine whether user has righ to make changes
    def has_object_permission(self, request, view, obj): #everytime a request is made the drf will call this fn and will pass in the request object, the view and the actual object we are checking the permission against 
        '''Check user is trying to edit own profile'''
        if request.method in permissions.SAFE_METHODS:# we are going to check the current http method and see if it is in the safe methods list  (safe method does not make changes to object), so viewing other users profile is ok
            return True
    
        return obj.id == request.user.id #whether the obj they are updating matches their authenticated user profile that is added to the authentication request, so when we authenticate a request in drf it will assign the authenticated user profile to the request and we can use this to compare  it to the object being updated and make sure it is same id

class UpdateOwnStatus(permissions.BasePermission):
    '''Allow user to update only their own status'''

    def has_object_permission(self, request, view, obj):
        '''Check the user is trying to update their own status'''
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id #if not safe method check if user is making changes to own profile