from rest_framework import serializers
from .models import Message, User, Conversation
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'password']
        read_only_fields = ['user_id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        try:
            # Validate the password using Django's built-in validators
            validate_password(value)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'sender_username', 'message_body', 'sent_at', 'created_at']
        read_only_fields = ['message_id', 'sent_at', 'created_at']
    
    def create(self, validated_data):
        return Message.objects.create(**validated_data)
    
    def get_sender_username(self, obj):
        return obj.sender.username if obj.sender else None
    
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']
    
    def create(self, validated_data):
        conversation = Conversation.objects.create()
        conversation.participants.set(validated_data.get('participants', []))
        return conversation
    


