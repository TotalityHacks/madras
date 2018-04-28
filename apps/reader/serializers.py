from rest_framework import serializers

from apps.reader.models import Rating


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ("application", "reader", "rating_number", "comments")
        read_only_fields = ("reader",)

    def create(self, data):
        data['reader'] = self.context['request'].user
        return super(RatingSerializer, self).create(data)
