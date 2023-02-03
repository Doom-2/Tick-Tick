from rest_framework.generics import UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import TgUser
from .serializers import BotUpdateSerializer


class BotUpdateView(UpdateAPIView):
    queryset = TgUser.objects.all()
    serializer_class = BotUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        data = self.request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        obj = get_object_or_404(queryset, verification_code=self.request.data['verification_code'])
        return obj
