from rest_framework import serializers

from apps.reader.models import RatingResponse


class RatingResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = RatingResponse
        fields = ("application", "reader", "rating_number", "comments")
        read_only_fields = ("reader",)

    def create(self, data):
        data['reader'] = self.context['request'].user
        return super(RatingResponseSerializer, self).create(data)
