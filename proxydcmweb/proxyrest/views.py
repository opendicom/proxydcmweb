from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import uuid
from proxyrest.models import SessionRest


@api_view(['POST'])
def rest_login(request, *args, **kwargs):
    if 'user' in request.query_params and 'password' in request.query_params:
        user = authenticate(username=request.query_params.get('user'), password=request.query_params.get('password'))
        if user:
            uid = create_session_rest(user)
            return Response({'session': uid}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'missing params'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def rest_logout(request, *args, **kwargs):
    if 'session' in kwargs:
        try:
            sessionrest = SessionRest.objects.get(sessionid=kwargs.get('session'))
            sessionrest.delete()
            return Response({'logout': 'ok'}, status=status.HTTP_200_OK)
        except SessionRest.DoesNotExist:
            return Response({'error': 'session not exist'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'missing parameter'}, status=status.HTTP_400_BAD_REQUEST)


def create_session_rest(user):
    uid = uuid.uuid4()
    sessionrest = SessionRest(sessionid=uid.hex,
                              start_date=timezone.now(),
                              expiration_date=timezone.now() + timezone.timedelta(minutes=5),
                              user=user)
    sessionrest.save()
    return uid.hex


def validate_session_expired(sessionrest):
    if sessionrest.expiration_date >= timezone.now():
        sessionrest.expiration_date = timezone.now() + timezone.timedelta(minutes=5)
        sessionrest.save()
        return True
    else:
        sessionrest.delete()
        return False
