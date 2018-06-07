from rest_framework import serializers, status
from django.db import transaction
from rest_framework.exceptions import ValidationError

from rest_framework.response import Response

from apps.reader.models import Rating, RatingField, RatingResponse


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        exclude = tuple()
        read_only_fields = ("id", "reader", "rating")

    def __init__(self, *args, **kwargs):
        super(RatingSerializer, self).__init__(*args, **kwargs)
        self.fields["rating"] = serializers.IntegerField(
            help_text="A weighted combination of all available rating fields.",
            read_only=True,
        )
        for field in RatingField.objects.all():
            name = field.name
            help_text = "{} ({}% of final score)".format(
                name.title(), field.weight)
            self.fields["field_{}".format(name)] = serializers.IntegerField(
                help_text=help_text)

    def create(self, data):
        request = self.context['request']
        if dict(request.data) == {}:
            return Response(
                {"error": "Invalid Rating Submitted!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data['reader'] = request.user
        with transaction.atomic():
            Rating.objects.filter(
                application=data['application'],
                reader=data['reader'],
            ).delete()
            response = super(RatingSerializer, self).create(
                {k: v for k, v in data.items() if not k.startswith("field_")})
            for field in data:
                if field.startswith("field_"):
                    setattr(response, field, data[field])
            fields_processed = RatingResponse.objects.filter(
                rating=response).count()
            field_count = RatingField.objects.count()
            if fields_processed < field_count:
                field_names = RatingField.objects.all().values_list(
                    "name", flat=True)
                list_of_fields = ["field_{}".format(x) for x in field_names]
                raise ValidationError(
                    'Missing required fields! Please pass the following '
                    'parameters to the API: {}'.format(list_of_fields)
                )
        return response
