from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, permissions, views
from .serializers import ImageInputSerializer, ImageDetailOutputSerializer, ImageDetailInputSerializer
from .services.basic_services import get_user_images, get_image_details, delete_image, \
    get_user_images_based_on_account_level, create_user_images_based_on_account_level, create_image_obj
from .services.expiring_link_services import generate_image_temporary_link


class ImagesView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        images = get_user_images(user=request.user.id)
        response_data = get_user_images_based_on_account_level(user=request.user, images=images, request=request)
        return Response(response_data)

    def post(self, request: Request) -> Response:
        serializer = ImageInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image_obj = create_image_obj(request=request, serializer=serializer)
        response_data = create_user_images_based_on_account_level(
            image_obj=image_obj, request=request, user=request.user)
        return Response(response_data)


class ImageDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, image_id: int) -> Response:
        image_obj = get_image_details(image_id=image_id, user=request.user.id)
        serializer = ImageDetailOutputSerializer(image_obj)
        return Response(serializer.data)

    def post(self, request, image_id):
        if request.user.userprofile.account_tier == 'enterprise':
            serializer = ImageDetailInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            time = serializer.validated_data['image_link_time']
            temporary_link = generate_image_temporary_link(image_id=image_id, time=time, request=request)
            return Response({'temporary_link': temporary_link}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request: Request, image_id: int) -> Response:
        delete_image(image_id=image_id, user=request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)
