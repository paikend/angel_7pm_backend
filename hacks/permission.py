from rest_framework.permissions import IsAuthenticated


class IsAuthenticatedOnlyNotGet(IsAuthenticated):
    def has_permission(self, request, view):
      if request.method != "GET":
        return request.user.is_authenticated and request.user.type == 'i'
      return True
        # return request.user.is_authenticated and request.user.type == 'i'
    # def has_permission(self, request, view):
    #     return request.user.is_authenticated and request.user.type == 'i'