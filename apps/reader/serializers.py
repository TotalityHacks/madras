from rest_framework import serializers

from apps.reader.models import Rating, RatingField


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
