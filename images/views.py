from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, permissions, views, generics
from rest_framework.parsers import MultiPartParser
from .serializers import ImageDetailOutputSerializer, ImageDetailInputSerializer, ImageOutputSerializer, \
    BasicImageOutputSerializer
from .services.basic_services import get_user_images, get_image_details, delete_image, create_image_obj
from .services.expiring_link_services import generate_image_temporary_link


class ImagesView(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ImageOutputSerializer

    def get_serializer_class(self):
        user_profile = self.request.user.userprofile

        if user_profile.account_tier in ['premium', 'enterprise']:
            return ImageOutputSerializer
        elif user_profile.custom_tier and user_profile.custom_tier.original_image_link:
            return ImageOutputSerializer
        else:
            return BasicImageOutputSerializer

    def get_queryset(self):
        return get_user_images(user=self.request.user.id)

    def perform_create(self, serializer):
        image = self.request.FILES.get('image')
        create_image_obj(user=self.request.user, image=image)


class ImageDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, image_id: int) -> Response:
        image_obj = get_image_details(image_id=image_id, user=request.user.id)
        serializer = ImageDetailOutputSerializer(image_obj)
        return Response(serializer.data)

    def post(self, request: Request, image_id: int) -> Response:
        if request.user.userprofile.account_tier == 'enterprise' or request.user.userprofile.custom_tier.expiring_link:
            serializer = ImageDetailInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            time = serializer.validated_data['image_link_time']
            temporary_link = generate_image_temporary_link(image_id=image_id, time=time)
            return Response({'temporary_link':temporary_link}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request: Request, image_id: int) -> Response:
        delete_image(image_id=image_id, user=request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)
