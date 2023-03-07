from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from buildings.models import Premise, Office, OtherBuilding, Cottage, OfficeInApartament
from buildings.services.client.view_counter import add_viewer
from utils.choices import ClientGroupChoices
from utils.services.request_counter import counter
from rest_framework.response import Response
from rest_framework import generics


class ListMixin(generics.ListAPIView):

    model = None

    def get_count_qs(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        return Response({"count": queryset.count()})

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        counter.delay(self.model.__name__)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class QuerysetMixin(generics.GenericAPIView):
    model = None
    action = None

    def get_queryset(self):
        if self.action == 'delete' or self.action == 'patch':
            return self.model.objects.filter(advertisement__user=self.request.user)
        else:
            return self.queryset


class RetrieveMixin(generics.RetrieveAPIView):

    model = None

    def check_permission(self, instance):
        if not self.request.user.is_authenticated or (self.request.user.is_authenticated and self.request.user.client_group == ClientGroupChoices.PARTIAL):
            if self.model == Premise:
                if instance.business_center.recommendation.all().exists():
                    return True
                else:
                    raise PermissionDenied()

    def retrieve(self, request, *args, **kwargs):
        counter.delay(self.model.__name__)
        instance = self.get_object()
        self.check_permission(instance)
        add_viewer(self.request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ViewSerializerMixin(generics.GenericAPIView):
    serializers = None
    action = None

    def get_serializer_class(self):
        return self.serializers

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        locale = self.request.GET.get('locale', 'ru')

        if self.action == 'list' or self.action == 'get':
            serializer_class = self.serializers['list'][locale]
        elif self.action == 'retrieve' or self.action == 'get':
            serializer_class = self.serializers['retrieve'][locale]
        elif self.action == 'create' or self.action == 'post':
            serializer_class = self.serializers['create'][locale]
        elif self.action == 'put' or self.action == 'patch' or self.action == 'update':
            serializer_class = self.serializers['update'][locale]
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)
