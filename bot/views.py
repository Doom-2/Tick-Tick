from rest_framework.generics import UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import TgUser
from .serializers import BotUpdateSerializer


class BotUpdateView(UpdateAPIView):
    """
    Handles PATCH to /bot/verify.
    """
    queryset = TgUser.objects.all()
    serializer_class = BotUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Gets data from request and passes it to serializer for validation after that update user fk field.
        :return: updated TGUser object where 'user' field is filled with 'id' value of current authenticated user.
        """
        queryset = self.filter_queryset(self.get_queryset())
        data = self.request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        obj = get_object_or_404(queryset, verification_code=self.request.data['verification_code'])
        return obj
