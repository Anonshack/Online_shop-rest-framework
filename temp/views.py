from rest_framework import generics
from users.views import checkUserToken
from .models import Clothing, AboutPage
from .serializers import ClothingSerializer, AboutPageSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework.decorators import api_view
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ClothingCreateView(generics.CreateAPIView):
    queryset = Clothing.objects.all()
    serializer_class = ClothingSerializer
    def update(self, request, *args, **kwargs):
        try:
            token = request.META['HTTP_TOKE']
        except:
            raise AuthenticationFailed('Iltomos, avval tizimga kiring')

        user = checkUserToken(token)
        if not user:
            raise AuthenticationFailed('Iltimos, avval tizimga kiring')


class ClothingDeleteView(generics.DestroyAPIView):
    queryset = Clothing.objects.all()
    serializer_class = ClothingSerializer
    def update(self, request, *args, **kwargs):
        try:
            token = request.META['HTTP_TOKE']
        except:
            raise AuthenticationFailed('Iltomos, avval tizimga kiring')

        user = checkUserToken(token)
        if not user:
            raise AuthenticationFailed('Iltimos, avval tizimga kiring')

@api_view(['GET'])
def clothing_detail(request, id):
    try:
        clothing = Clothing.objects.get(pk=id)
    except Clothing.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ClothingSerializer(clothing)
        return Response(serializer.data)

class ClothingFilterView(generics.ListAPIView):
    queryset = Clothing.objects.all()
    serializer_class = ClothingSerializer
    def update(self, request, *args, **kwargs):
        try:
            token = request.META['HTTP_TOKE']
        except:
            raise AuthenticationFailed('Iltomos, avval tizimga kiring')

        user = checkUserToken(token)
        if not user:
            raise AuthenticationFailed('Iltimos, avval tizimga kiring')

    def get_queryset(self):
        queryset = Clothing.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset


class AboutCreateView(generics.CreateAPIView):
    queryset = AboutPage.objects.all()
    serializer_class = AboutPageSerializer



# web-site uchun search qismi
class ShoesSearchListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ClothingSerializer

    def get_queryset(self):
        text = self.kwargs["text"]
        queryset = Clothing.objects.filter(
            name__icontains=text
        ) | Clothing.objects.filter(name__icontains=text)
        return queryset