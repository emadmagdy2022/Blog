from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_object_permission(self,request,view,obj):
        return request.user and request.user.is_staff

class IsOwner(BasePermission):
    def has_object_permission(self,request,view,obj):
        owner = getattr(obj, "author", None) or getattr(obj, "user", None)
        return owner == request.user

class IsAdminOrOwner(BasePermission):
    def has_object_permission(self,request,view,obj):
        is_admin = request.user and request.user.is_staff
        owner = getattr(obj, "author", None) or getattr(obj, "user", None)
        is_owner = owner == request.user
        return is_admin or is_owner