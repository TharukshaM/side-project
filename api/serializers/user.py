from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'address']  # Replace 'name' with 'username'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create a new user and hash password securely."""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            address=validated_data.get('address', "")
        )
        return user
