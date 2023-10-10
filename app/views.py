import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from app.models import Client, User
from app.db_manager import DBManager
from app.ms_manager import MSManager
from app.notifier import send_notification
from app.serializers import UserSerializer
from app.serializers import ClientSerializer
from app.serializers import RefreshSerializer
from app.serializers import NotificationSerializer
from djangoTest.authentication import MSAuthView


logger = logging.getLogger(__name__)


class CallbackAPI(APIView):
    authentication_classes = []

    def get(self, request):
        ms_manager = MSManager(code=request.query_params['code'])
        credentials_dict = ms_manager.exchange_code()
        db_manager = DBManager()
        user = db_manager.create_user(ms_manager.get_user())

        # logger.debug("User %s created" % user.username, extra={"": user.is_staff})

        db_manager.create_token(credentials_dict | {"user_id": user.id})
        return Response({
            'access_token': credentials_dict["access_token"],
            'refresh_token': credentials_dict["refresh_token"],
        })


class RefreshTokenAPI(MSAuthView):

    def post(self, request):
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        credentials_dict = MSManager().refresh(serializer.validated_data['refresh_token'])
        db_manager = DBManager()
        db_manager.create_token(credentials_dict | {"user_id": request.user.id})
        return Response({
            'access_token': credentials_dict["access_token"],
            'refresh_token': credentials_dict["refresh_token"],
        })


class NotificationAPI(MSAuthView):
    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        logger.info(
            "Send messages from - %s, to - %s, by - %s" %
            (validated_data['from_email'], validated_data['recipient_list'], validated_data['notification_type']),
            extra={"is_staff": request.user.is_staff}
        )
        send_notification(validated_data.pop('notification_type'), validated_data, request.access_token)
        return Response()


class HistoryMassagesAPI(MSAuthView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('client', openapi.IN_QUERY, description="Клієнт", type=openapi.TYPE_STRING),
        ],
        responses={200: 'OK'},
    )
    def get(self, request):
        client = request.query_params['client']
        ms_manager = MSManager(token=request.access_token)
        logger.info(
            "Get massages %s with %s" % (request.user.username, client),
            extra={"is_staff": request.user.is_staff}
        )
        return Response(ms_manager.get_messages(client))


class ClientAPI(ModelViewSet, MSAuthView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class UserAPI(ModelViewSet, MSAuthView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
