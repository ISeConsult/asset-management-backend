from rest_framework import serializers
from apps.userActivities.models import UserActivity


class UserActivitiesSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        if obj.user:
            return {
                "id": obj.user.id,
                "uid": obj.user.uid,
                "full_name": f"{obj.user.first_name} {obj.user.last_name}",
            }
        else:
            return None

    class Meta:
        model = UserActivity
        fields = "__all__"  # or specify fields you want to include
