from rest_framework import serializers
from .models import TgUser
from .tg.client import TgClient
import environ

env = environ.Env()
token = env('TG_CLIENT_TOKEN')


class BotUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TgUser
        fields = '__all__'
        read_only_fields = ('id', 'tg_chat_id', 'tg_user_name',)

    def validate_verification_code(self, value: str):
        try:
            TgUser.objects.get(verification_code=value)
        except TgUser.DoesNotExist:
            raise serializers.ValidationError('Verification code is incorrect')
        return value

    def update(self, instance: TgUser, validated_data: dict) -> TgUser:

        instance.user_id = self.context['request'].user.id
        instance.save(update_fields=('verification_code',))
        cl = TgClient(token)
        cl.send_message(instance.tg_chat_id, f'{instance.user.username.title()}, '
                                             f'you have successfully authorized via Telegram! 🙏\n'
                                             f'I\'ll help you see your list of active goals, '
                                             f'as well as create new ones.\n\n'
                                             f'Enter /goals to view all your goals.\n\n'
                                             f'Enter /create to create a new goal.')

        return super().update(instance, validated_data)
