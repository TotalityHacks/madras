from rest_framework import serializers
from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.reader.models import Rating, RatingField, RatingResponse


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        exclude = tuple()
        read_only_fields = ("id", "reader", "rating")

    def __init__(self, *args, **kwargs):
        super(RatingSerializer, self).__init__(*args, **kwargs)
        self.fields["rating"] = serializers.IntegerField(help_text="A weighted combination of all available rating fields.")
        for field in RatingField.objects.all():
            name = field.name
            self.fields["field_{}".format(name)] = serializers.IntegerField(help_text="{} ({}% of final score)".format(name.title(), field.weight))

    def create(self, data):
        request = self.context['request']
        data['reader'] = request.user
        with transaction.atomic():
            Rating.objects.filter(application=data['application'], reader=data['reader']).delete()
            response = super(RatingSerializer, self).create({k: v for k, v in data.items() if not k.startswith("field_")})
            for field in data:
                if field.startswith("field_"):
                    setattr(response, field, data[field])
            fields_processed = RatingResponse.objects.filter(rating=response).count()
            field_count = RatingField.objects.count()
            if fields_processed < field_count:
                raise ValidationError('Missing required fields! Please pass the following parameters to the API: {}'.format(["field_{}".format(x) for x in RatingField.objects.all().values_list("name", flat=True)]))
        return response
