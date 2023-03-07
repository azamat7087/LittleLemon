from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from utils.services.user_service import get_user_queryset


class ProfileViewSet(ViewSet):
    user_serializer_class = None
    client_serializer_class = None
    permission_classes = (IsAuthenticated,)
    queryset = get_user_queryset(**{})

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        """
        For getting user object with prefetched data
        """
        filter_kwargs = {'id': self.request.user.id, 'user_type': self.request.user.user_type}
        instance = get_object_or_404(self.get_queryset(), **filter_kwargs)
        return instance

    def get_serializer_class(self):
        """
        Check if serializer_class is not None
        """
        assert self.user_serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        assert self.client_serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        if self.request.user.is_authenticated and self.request.user.user_type == 'U':
            return self.user_serializer_class
        else:
            return self.client_serializer_class

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    @action(methods=["get"], detail=False,
            url_path="profile", url_name="profile")
    def profile(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }
