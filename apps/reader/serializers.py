from rest_framework import serializers

from apps.reader.models import Rating, RatingField, RatingResponse


class RatingFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = RatingField
        fields = ("prompt", "min_number", "max_number", "options")
        read_only_fields = fields


class RatingSchemaSerializer(serializers.ModelSerializer):
    fields = RatingFieldSerializer(many=True)

    class Meta:
        model = Rating
        fields = ("application", "fields")
        read_only_fields = fields


class RatingResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = RatingResponse
        fields = ("application", "reader", "rating_number", "comments")
        read_only_fields = ("reader",)

    def create(self, data):
        data['reader'] = self.context['request'].user
        return super(RatingResponseSerializer, self).create(data)
