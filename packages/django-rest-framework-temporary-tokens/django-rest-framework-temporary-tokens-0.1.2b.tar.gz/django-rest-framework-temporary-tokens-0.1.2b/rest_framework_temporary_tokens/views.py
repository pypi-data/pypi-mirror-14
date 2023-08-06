"""Utility views for Temporary Tokens.
Classes:
    ObtainTemporaryAuthToken: View to provide tokens to clients.
    
( Inspired by 
https://github.com/JamesRitchie/django-rest-framework-expiring-tokens,
https://github.com/JamesRitchie/django-rest-framework-expiring-tokens/blob/master/LICENSE )
"""
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from models import TemporaryToken


class ObtainTemporaryAuthToken(ObtainAuthToken):
    """Enables username/password exchange for expiring token."""
    model = TemporaryToken

    def post(self, request):
        """Respond to POSTed username/password with token."""
        serializer = AuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            token, _ = TemporaryToken.objects.get_or_create(
                user=serializer.validated_data['user']
            )

            if token.expired:
                # If the token is expired, generate a new one.
                token.delete()
                token = TemporaryToken.objects.create(
                    user=serializer.validated_data['user']
                )

            data = {'token': token.key}
            return Response(data)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

obtain_temporary_auth_token = ObtainTemporaryAuthToken.as_view()

