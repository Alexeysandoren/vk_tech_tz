from rest_framework.mixins import (CreateModelMixin,
                                   DestroyModelMixin,
                                   ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.viewsets import GenericViewSet


class CreateListRetrieveViewSet(CreateModelMixin, GenericViewSet, 
                                ListModelMixin, RetrieveModelMixin):
    pass


class ListDestroyViewSet(DestroyModelMixin, GenericViewSet,
                         ListModelMixin):
    pass
