from rest_framework import serializers


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField(
        style={
            'template': 'email_field.html'
        }
    )
