from rest_framework.permissions import IsAuthenticated


class IsAuthenticatedOrViewing(IsAuthenticated):

    def has_permission(self, request, view):
        return view.action == 'retrieve' or super(IsAuthenticatedOrViewing, self).has_permission(request, view)
