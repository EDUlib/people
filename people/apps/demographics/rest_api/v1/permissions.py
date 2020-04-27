from rest_framework import permissions

# TODO: Do more research on this. Code snippet based on Coaching plugin that looks like
#       it should help implement ability for a user to only access their own data
class CanAccessDemographics(permissions.BasePermission):
    """
    Permission class to check that a user can update their own resource only
    """
    def has_permission(self, request, view):
        if request.method == "POST":
            modified_user = request.POST.get("user")
            if modified_user:
                return request.user.id == int(modified_user)
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.user.id
