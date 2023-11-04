from typing import Type
from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, permissions, views, generics
from rest_framework.parsers import MultiPartParser
from .models import UserImage
from .serializers import ImageDetailOutputSerializer, ImageDetailInputSerializer, ImageOutputSerializer, \
    BasicImageOutputSerializer
from .services.basic_services import get_user_images, get_image_details, delete_image, create_image_obj
from .services.expiring_link_services import generate_image_temporary_link


class ImagesView(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['upload_date']

    def get_serializer_class(self) -> Type[ImageOutputSerializer] | Type[BasicImageOutputSerializer]:
        user_profile = self.request.user.userprofile
        account_tier = user_profile.account_tier

        if account_tier and (account_tier.name in ['Premium', 'Enterprise'] or account_tier.original_image_link):
            return ImageOutputSerializer
        else:
            return BasicImageOutputSerializer

    def get_queryset(self) -> QuerySet[UserImage]:
        return get_user_images(user=self.request.user.id)

    def create(self, request: Request, *args, **kwargs) -> Response:
        image = request.FILES.get('image')
        create_image_obj(user=request.user, image=image)
        return Response({'message': 'Image uploaded successfully.'}, status=status.HTTP_201_CREATED)


class ImageDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, image_id: int) -> Response:
        image_obj = get_image_details(image_id=image_id, user=request.user.id)
        serializer = ImageDetailOutputSerializer(image_obj)
        return Response(serializer.data)

    def post(self, request: Request, image_id: int) -> Response:
        user_profile = request.user.userprofile
        is_enterprise = user_profile.account_tier == 'enterprise'
        has_expiring_link = user_profile.account_tier.original_image_link

        if is_enterprise or has_expiring_link:
            serializer = ImageDetailInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            time = serializer.validated_data['image_link_time']
            temporary_link = generate_image_temporary_link(image_id=image_id, time=time)
            return Response({'temporary_link': temporary_link}, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request: Request, image_id: int) -> Response:
        delete_image(image_id=image_id, user=request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)
