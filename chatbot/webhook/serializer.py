from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TextSerializer(serializers.Serializer):
    body = serializers.CharField()

class ContextSerializer(serializers.Serializer):
    from_ = serializers.CharField()
    id = serializers.CharField()

    def to_internal_value(self, data):
        data["from_"] = data.pop("from", None)
        return super().to_internal_value(data)

class MessageSerializer(serializers.Serializer):
    context = ContextSerializer(required=False)
    from_ = serializers.CharField()
    id = serializers.CharField()
    timestamp = serializers.CharField()
    type_ = serializers.CharField()
    text = TextSerializer()

    def to_internal_value(self, data):
        data["from_"] = data.pop("from", None)
        data["type_"] = data.pop("type", None)
        return super().to_internal_value(data)

class ProfileSerializer(serializers.Serializer):
    name = serializers.CharField()

class ContactSerializer(serializers.Serializer):
    wa_id = serializers.CharField()
    profile = ProfileSerializer()

class MetaDataSerializer(serializers.Serializer):
    display_phone_number = serializers.CharField()
    phone_number_id = serializers.CharField()

class ValueSerializer(serializers.Serializer):
    messaging_product = serializers.CharField()
    metadata = MetaDataSerializer()
    contacts = ContactSerializer(many=True)
    messages = MessageSerializer(many=True)

class ChangesSerializer(serializers.Serializer):
    field = serializers.CharField()
    value = ValueSerializer()

class EntrySerializer(serializers.Serializer):
    id = serializers.CharField()
    changes = ChangesSerializer(many=True)

class RequestSerializer(serializers.Serializer):
    object = serializers.CharField()
    entry = EntrySerializer(many=True)