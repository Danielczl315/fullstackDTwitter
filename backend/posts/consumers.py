from .models import Post

from .serializers import GetPostSerializer

from djangochannelsrestframework.generics import GenericAsyncAPIConsumer 
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework import permissions

class PostConsumer(ListModelMixin, GenericAsyncAPIConsumer):

    queryset = Post.objects.all() 
    permission_classes = (permissions.AllowAny, )

    async def connect(self, **kwargs):
        await self.model_change.subscribe()
        await super().connect(**kwargs)

    @model_observer(Post) 
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serialize(self, instance, action, **kwargs):
        return dict(data=GetPostSerializer(instance=instance).data, action=action.value)