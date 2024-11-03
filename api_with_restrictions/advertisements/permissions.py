from django.template.context_processors import request
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == ['GET']: # Ограничение кроме ГЕТ
            return True
        return obj.creator == request.user