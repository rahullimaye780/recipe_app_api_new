"""
  Sirializers for API view
"""
from django.contrib.auth import (get_user_model,authenticate,)
from django.utils.translation import gettext as _
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """ Serializer for user objects """

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}} # Password should be write only and have a minimum length of 5

    def create(self, validated_data):
        """ Create a new user with encrypted password and return it """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """ Update a user, setting the password correctly and return it """
        password = validated_data.pop('password', None) # Pop the password from the validated data
        user = super().update(instance, validated_data) # Update the user with the remaining validated data

        if password:
            user.set_password(password) # Set the password using the set_password method to ensure it's encrypted
            user.save() # Save the user after setting the password

        return user

class AuthTokenSerializer(serializers.Serializer):
    """ Serializer for the user authentication token """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):                  #attrs is the short form of attributes and its use for data that is passed to the serializer
        """ Validate and authenticate the user """
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs