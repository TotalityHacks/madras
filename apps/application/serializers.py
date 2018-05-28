from rest_framework import serializers

from .models import Application, Resume, Submission


class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = (
            'id', 'user', 'first_name', 'last_name', 'phone_number', 'devpost',
            'github', 'linkedin', 'personal_website', 'school', 'essay_helped',
            'essay_project', 'age', 'college_grad_year', 'gender', 'major',
            'current_study_level', 'race_ethnicity', 'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')


class ResumeSerializer(serializers.ModelSerializer):

    file = serializers.FileField(write_only=True)

    class Meta:
        model = Resume
        fields = ('created_at', 'file', 'filename', 'id',)
        read_only_fields = ('created_at', 'id',)
        ordering = ('created_at',)

    def create(self, validated_data):
        validated_data.pop('file')
        return Resume.objects.create(**validated_data)


class SubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submission
        fields = ApplicationSerializer.Meta.fields
        read_only_fields = ApplicationSerializer.Meta.read_only_fields
