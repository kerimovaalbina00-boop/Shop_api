from rest_framework import serializers
from .models import Category, Product, Review
from django.db.models import Avg
from rest_framework.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = 'id name products_count'.split()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'




class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id title price rating reviews'.split()

    def get_rating(self, product):
        return product.reviews.aggregate(Avg('stars'))['stars__avg']
    


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=2, max_length=100)


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=2, max_length=100)
    description = serializers.CharField(required=True, min_length=5)
    price = serializers.FloatField(min_value=1)
    category = serializers.IntegerField()

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category does not exist!'
)

        return category_id


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, min_length=5)
    stars = serializers.IntegerField(min_value=1, max_value=10)
    product = serializers.IntegerField()

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Product does not exist!')

        return product_id