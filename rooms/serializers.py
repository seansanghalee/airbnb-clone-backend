from rest_framework.serializers import ModelSerializer, SerializerMethodField

from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from users.serializers import TinyUserSerializer

from wishlists.models import Wishlist

from .models import Amenity, Room


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomListSerializer(ModelSerializer):
    photos = PhotoSerializer(
        read_only=True,
        many=True,
    )

    rating = SerializerMethodField()
    is_owner = SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user


class RoomDetailSerializer(ModelSerializer):
    owner = TinyUserSerializer(
        read_only=True,
    )
    amenities = AmenitySerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(
        read_only=True,
    )

    photos = PhotoSerializer(
        read_only=True,
        many=True,
    )

    rating = SerializerMethodField()
    is_liked = SerializerMethodField()
    is_owner = SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()

    def get_is_liked(self, room):
        request = self.context["request"]
        return Wishlist.objects.filter(owner=request.user, rooms__pk=room.pk).exists()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user
