from rest_framework import serializers
from . import models


# --------------- AUTH -------------------------------------------------------------

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
                                )
        password = self.validated_data['password']
        account.set_password(password)
        account.save()
        return account