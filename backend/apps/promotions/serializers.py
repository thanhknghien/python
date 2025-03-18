from rest_framework import serializers
from .models import Promotion
from apps.books.models import Category
from apps.books.serializers import CategorySerializer

class PromotionSerializer(serializers.ModelSerializer):
    CategoryID = CategorySerializer(read_only=True)

    class Meta:
        model = Promotion
        fields = ['PromotionID', 'Name', 'DiscountPercent', 'StartDate', 'EndDate', 'CategoryID']

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='CategoryID', write_only=True, required=False
    )

    def validate(self, data):
        # Kiểm tra ngày hợp lệ
        if data['StartDate'] > data['EndDate']:
            raise serializers.ValidationError("EndDate must be after StartDate.")
        return data