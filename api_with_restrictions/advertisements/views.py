from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement

from advertisements.serializers import AdvertisementSerializer

from advertisements.permissions import IsOwnerOrReadOnly

from advertisements.filters import AdvertisementFilter


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()    # Запрос
    serializer_class = AdvertisementSerializer
    authentication_classes = [TokenAuthentication]  # для приема Токена
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['created_at', 'status']

    def perform_create(self, serializer):
        if Advertisement.objects.filter(creator=self.request.user).count() >= 10:
            raise ValidationError('Вы разместили максимально возможное количество объявлений')
        serializer.save(creator=self.request.user)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update"]:
            return [IsOwnerOrReadOnly()]
        return []

    def list(self, request):
        list = Advertisement.objects.all()
        queryset = AdvertisementFilter(data=request.GET, queryset=list, request=request).qs
        serializer = AdvertisementSerializer(queryset, many=True)
        return Response(serializer.data)