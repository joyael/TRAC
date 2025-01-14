from rest_framework import serializers
from .models import Role, RUser , Product, Permission, Favourite
from django.contrib.auth.hashers import make_password, check_password

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'  # or specify the fields you want to include

class RUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RUser 
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'


class RUserRegistrationSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(slug_field='name', queryset=Role.objects.all())
    class Meta:
        model = RUser 
        fields = ['username', 'hashed_password', 'role']  # Include role_id if needed

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['hashed_password'] = make_password(validated_data['hashed_password'])
        return super().create(validated_data)

class RUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)  # Ensure password is not returned in responses

class RUserResponseSerializer(serializers.ModelSerializer):
    role_id = serializers.IntegerField(source='role.id')  # Assuming role is a ForeignKey

    class Meta:
        model = RUser 
        fields = ['username', 'role_id']