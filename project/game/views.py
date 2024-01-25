from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Token
from .serializers import TokenSerializer
import datetime
import secrets


TIME_GENERATE_TOKEN_IN_HOUR = [12, 15, 20]


class CheckOnlineView(APIView):
    def get(self, request):
        # Возвращаем ответ с кодом 200 и сообщением "OK"
        return Response({"message": "OK"}, status=200)


class TokenGenerateView(APIView):
    def get(self, request):
        token = self.generate_token()
        return Response({'token': token})

    def generate_token(self):
        now = datetime.datetime.now()
        if now.hour in TIME_GENERATE_TOKEN_IN_HOUR:
            # Генерация нового токена
            token_value = secrets.token_hex(32)
            token = Token.objects.create(value=token_value)
            token.save()
        latest_token = Token.objects.latest('id')
        serializer = TokenSerializer(latest_token)
        print(serializer.data)
        return serializer.data
