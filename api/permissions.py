from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        role = getattr(user.userprofile, "role", "").lower().strip()

        # SAFE METHODS (GET, HEAD, OPTIONS) 
        if request.method in ("GET",'HEAD',"OPTIONS"):
            return True

        # DELETE: admin can delete anything, employee can delete own
        if request.method == "DELETE":
            if role in ("admin", "superadmin"):
                return True
            return obj.employee == user

        if request.method in ("PUT", "PATCH"):
            return obj.employee == user

        return False
