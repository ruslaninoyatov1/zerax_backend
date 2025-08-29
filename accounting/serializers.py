from rest_framework import serializers
from .models import Account, JournalEntry


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class JournalEntrySerializer(serializers.ModelSerializer):
    account_detail = AccountSerializer(source="account", read_only=True)

    class Meta:
        model = JournalEntry
        fields = "__all__"
        read_only_fields = ("id", "created_at")
