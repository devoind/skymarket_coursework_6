from django.contrib.auth import get_user_model
# from django.shortcuts import get_object_or_404
from rest_framework import pagination, viewsets
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Ad, Comment
from .filters import AdFilter
from .permissions import IsOwner, IsAdmin
from .serializers import AdSerializer, CommentSerializer

#
# class AdPagination(pagination.PageNumberPagination):
#     page_size = 4
#
#
# class CRUDPermission(permissions.BasePermission):
#
#     def has_permission(self, request, view):
#         pass
#
#
# class AdViewSet(viewsets.ModelViewSet):
#     queryset = Ad.objects.all()
#     pagination_class = AdPagination
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = AdFilter
#     serializer_class = AdSerializer
#
#     def get_queryset(self):
#         if self.action == 'me':
#             return Ad.objects.filter(author=self.request.user).all()
#         return Ad.objects.all()
#
#     def get_permissions(self):
#         if self.action in ['list', 'retrieve', 'create', 'me']:
#             self.permission_classes = [permissions.IsAuthenticated]
#         else:
#             self.permission_classes = [permissions.IsAdminUser]
#
#         return super().get_permissions()
#
#     def get_serializer_class(self):
#         if self.action == 'retrieve':
#             return AdDetailSerializer
#         return AdSerializer
#
#     @action(detail=False, methods=['get'])
#     def me(self, request, *args, **kwargs):
#         return super().list(self, request, *args, **kwargs)
#
#
# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#
#     def get_queryset(self):
#         ad_instance = get_object_or_404(Ad, id=self.kwargs['ad_pk'])
#         return ad_instance.comment_set.all()
#
#     def perform_create(self, serializer):
#         ad_instance = get_object_or_404(Ad, id=self.kwargs['ad_pk'])
#         user = self.request.user
#         serializer.save(author=user, ad=ad_instance)

User = get_user_model()


class AdPagination(pagination.PageNumberPagination):
    page_size = 4


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    pagination_class = AdPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action in ("me", "list"):
            self.serializer_class = AdSerializer
        else:
            self.serializer_class = AdSerializer

        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [AllowAny]
        elif self.action == "update":
            self.permission_classes = [IsAuthenticated & IsOwner | IsAdmin]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated & IsOwner | IsAdmin]
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.pk)

    @action(detail=False)
    def me(self, request, *args, **kwargs):
        self.queryset = self.get_queryset().filter(author_id=self.request.user.pk)
        return self.list(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        """
        Выдача всех комментарий указанного объявления
        """
        self.queryset = self.queryset.filter(ad_id=self.kwargs.get('ad_id'))
        return super().get_queryset()

    def get_permissions(self):
        if self.action == "update":
            self.permission_classes = [IsAuthenticated & IsOwner | IsAdmin]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated & IsOwner | IsAdmin]
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(ad_id=self.kwargs.get("ad_id"), author_id=self.request.user.pk)
