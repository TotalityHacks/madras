from rest_framework import serializers

class SummarySerializer(serializers.BaseSerializer):
    def to_representation(self):
        return {
            "num_applicants": 123,
            "num_total_reads": 220,
            "average_application_rating": 3.4,
        }
