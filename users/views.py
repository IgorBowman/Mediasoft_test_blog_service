from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import CreateCustomUserSerializer
from .models import CustomUser


class RegistrationAPI(GenericAPIView):
    serializer_class = CreateCustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": CreateCustomUserSerializer(
                user,
                context=self.get_serializer_context()
            ).data
        })
