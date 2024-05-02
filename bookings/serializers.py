from django.utils import timezone
from rest_framework.serializers import DateField, ModelSerializer, ValidationError

from .models import Booking


class CreateRoomBookingSerializer(ModelSerializer):
    check_in = DateField()
    check_out = DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise ValidationError("Can't book for the past date.")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise ValidationError("Can't book for the past date.")
        return value

    def validate(self, data):
        if data["check_out"] <= data["check_in"]:
            raise ValidationError("Check in date must be before check out date.")
        if Booking.objects.filter(
            check_in__lt=data["check_out"],
            check_out__gt=data["check_in"],
        ).exists():
            raise ValidationError("Booking during the date already exists.")
        return data


class PublicBookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience",
            "guests",
        )
