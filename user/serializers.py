from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer, TokenSerializer

class UserSerializer(UserDetailsSerializer):

    company_name = serializers.CharField(source="userprofile.company_name")

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('company_name',)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', {})
        company_name = profile_data.get('company_name')

        instance = super(UserSerializer, self).update(instance, validated_data)

        # get and update user profile
        profile = instance.userprofile
        if profile_data and company_name:
            profile.company_name = company_name
            profile.save()
        return instance

class tokenSerializer1(TokenSerializer):
    userId = serializers.UUIDField(source="user.userprofile.id")
    username = serializers.CharField(source="user.username")
    name = serializers.CharField(source="user.userprofile.name")
    lastLogin = serializers.CharField(source="user.last_login")
    email = serializers.CharField(source="user.email")

    """
    Serializer for Token model.
    """

    class Meta(TokenSerializer.Meta):
        fields = TokenSerializer.Meta.fields + ('userId','username','name','lastLogin','email')
