from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import LoginSerializer, LogoutSerializer


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        tokens = user.get_tokens()

        return Response({
            "success": True,
            "status_code": 200,
            "message": "Login muvaffaqiyatli bajarildi",
            "data": {
                "user_id": str(user.id),
                "full_name": user.full_name,
                "role": user.role,
                "tokens": tokens
            }
        }, status=status.HTTP_200_OK)


class LogOutAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)