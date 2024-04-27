from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Token
from .serializers import TokenSerializer
import datetime
import secrets

COUNT_GEN = {}
TIME_GENERATE_TOKEN_IN_HOUR = [12, 15, 20]
for i in TIME_GENERATE_TOKEN_IN_HOUR:
    COUNT_GEN[i] = True


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
        global COUNT_GEN
        try:
            latest_token = Token.objects.latest('id')
            if latest_token.created_at.day != now.day:
                for key, val in COUNT_GEN.items():
                    COUNT_GEN[key] = True

            if now.hour in TIME_GENERATE_TOKEN_IN_HOUR and COUNT_GEN[now.hour]:
                # Генерация нового токена
                COUNT_GEN[now.hour] = False
                token_value = secrets.token_hex(32)
                token = Token.objects.create(value=token_value)
                token.save()
            latest_token = Token.objects.latest('id')
            serializer = TokenSerializer(latest_token)

            return serializer.data

        except Token.DoesNotExist:
            # Генерация нового токена
            if now.hour in TIME_GENERATE_TOKEN_IN_HOUR:
                token_value = secrets.token_hex(32)
                token = Token.objects.create(value=token_value)
                token.save()
                serializer = TokenSerializer(token)
                COUNT_GEN += 1
                return serializer.data
            return 0
