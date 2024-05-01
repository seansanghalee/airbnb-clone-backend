from django.db import transaction
from rest_framework.exceptions import (
    NotAuthenticated,
    NotFound,
    ParseError,
    PermissionDenied,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from categories.models import Category

from .models import Amenity, Room
from .serializers import AmenitySerializer, RoomDetailSerializer, RoomListSerializer


class Rooms(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomListSerializer(
            rooms,
            context={
                "request": request,
            },
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required.")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("Category kind must be rooms.")
                except Category.DoesNotExist:
                    raise NotFound("Category not found.")
                try:
                    with transaction.atomic():
                        room = serializer.save(owner=request.user, category=category)
                        amenities = request.data.get("amenities")
                        # if amenities:
                        for amenity_pk in amenities:
                            # try:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                            # except Amenity.DoesNotExist:
                            # pass
                            # raise ParseError(f"Amenity with id {amenity_pk} not found.")
                        serializer = RoomDetailSerializer(room)
                        return Response(serializer.data)
                except Exception:
                    raise ParseError("Amenity not found.")
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(
            room,
            context={
                "request": request,
            },
        )
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        # update

    def delete(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Amenities(APIView):
    def get(self, request):
        amenities = Amenity.objects.all()
        serializer = AmenitySerializer(
            amenities,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        return Response(
            AmenitySerializer(
                self.get_object(pk),
            ).data
        )

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)
