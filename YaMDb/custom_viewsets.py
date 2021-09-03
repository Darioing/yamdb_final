from rest_framework import mixins, viewsets


class BaseModelViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    pass


class TitleModelViewSet(BaseModelViewSet,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,):
    pass
