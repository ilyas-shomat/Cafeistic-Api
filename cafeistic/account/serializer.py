from rest_framework import serializers
from . import models


# --------------- USER -------------------------------------------------------------

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = "__all__"
        extra_kwargs = {
            # 'password': {'write_only':True},
            'is_admin': {'write_only': True},
            'is_active': {'write_only': True},
            'is_staff': {'write_only': True},
            'is_superuser': {'write_only': True},
        }

    def save(self):
        account = models.Account(full_name=self.validated_data['full_name'],
                                 username=self.validated_data["username"],
                                 email=self.validated_data["email"],
                                 user_type=self.validated_data["user_type"],
                                )
        if "establishment" in self.validated_data:
            account.establishment = self.validated_data["establishment"]
        password = self.validated_data['password']
        account.set_password(password)
        account.save()
        return account


class ReadableAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ('id','username','full_name','email','user_type')


# --------------- ESTABLISHMENT -------------------------------------------------------------

class EstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Establishment
        fields = "__all__"

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Schedule
        fields = "__all__"