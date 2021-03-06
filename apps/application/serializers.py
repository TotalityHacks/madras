from rest_framework import serializers

from .models import Application, Resume, Submission
from .validators import validate_resume


class ApplicationSerializer(serializers.ModelSerializer):
    resumes = serializers.SerializerMethodField(read_only=True)
    submitted = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Application
        fields = (
            'id', 'user', 'first_name', 'last_name', 'phone_number', 'devpost',
            'github', 'linkedin', 'personal_website', 'school', 'essay_helped',
            'essay_project', 'age', 'college_grad_year', 'gender', 'major',
            'current_study_level', 'race_ethnicity', 'created_at',
            'updated_at', 'resumes', 'submitted',
        )
        read_only_fields = (
            'id', 'user', 'created_at', 'updated_at', 'resumes', 'submitted',)

    def get_resumes(self, instance):
        return ResumeSerializer(
            instance.user.resumes.all().order_by("-created_at"),
            many=True,
        ).data

    def get_submitted(self, instance):
        return instance.user.submissions.exists()


class ResumeSerializer(serializers.ModelSerializer):

    file = serializers.FileField(write_only=True, validators=[validate_resume])

    class Meta:
        model = Resume
        fields = ('created_at', 'file', 'filename', 'id',)
        read_only_fields = ('created_at', 'id',)
        ordering = ('created_at',)

    def create(self, validated_data):
        validated_data.pop('file')
        return Resume.objects.create(**validated_data)


class SubmissionSerializer(serializers.ModelSerializer):

    resumes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Submission
        fields = (
            'id', 'user', 'first_name', 'last_name', 'phone_number', 'devpost',
            'github', 'linkedin', 'personal_website', 'school', 'essay_helped',
            'essay_project', 'age', 'college_grad_year', 'gender', 'major',
            'current_study_level', 'race_ethnicity', 'created_at', 'resumes',
            'application_id',
        )
        read_only_fields = (
            'id', 'user', 'created_at', 'resumes', 'application_id',
        )

    def get_resumes(self, instance):
        return (
            instance.user.resumes.all()
            .order_by("-created_at")
            .values_list("id", flat=True)
        )
