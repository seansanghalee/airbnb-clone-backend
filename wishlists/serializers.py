from rest_framework.serializers import ModelSerializer
from .models import Wishlist


class WishlistSerializer(ModelSerializer):
    from rooms.serializers import RoomListSerializer

    rooms = RoomListSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
            "rooms",
            # code challenge: experiences
        )
