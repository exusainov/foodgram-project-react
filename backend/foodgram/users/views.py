from djoser.views import UserViewSet


from .models import User
from .serializers import CustomUserSerializer

User = User()



class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer