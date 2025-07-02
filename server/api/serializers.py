from rest_framework import serializers
from .models import MenuItem, Order, OrderItem

from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class MenuItemSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=False)
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'available', 'image', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request and request.method in ['POST', 'PUT', 'PATCH']:
            return None  # Hide in POST/PUT responses
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None


class OrderItemWriteSerializer(serializers.ModelSerializer):
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), source='menu_item'
    )

    class Meta:
        model = OrderItem
        fields = ['menu_item_id', 'quantity']

class OrderItemReadSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemWriteSerializer(many=True, write_only=True, required=False)

    order_items = OrderItemReadSerializer(source='orderitem_set', many=True, read_only=True)
    total_price = serializers.DecimalField(read_only=True, max_digits=8, decimal_places=2)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_price', 'created_at', 'items', 'order_items']
        read_only_fields = ['user', 'total_price', 'created_at']
    def validate_items(self, value):
        if self.context['request'].method == 'POST':
            if not value:
                raise serializers.ValidationError("Order must contain at least one item.")
            for item in value:
                if not item['menu_item'].available:
                    raise serializers.ValidationError(
                        f"Item '{item['menu_item'].name}' is currently unavailable."
                    )
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        user = self.context['request'].user

        order = Order.objects.create(user=user, total_price=0)
        total = 0

        for item_data in items_data:
            menu_item = item_data['menu_item']
            quantity = item_data['quantity']
            OrderItem.objects.create(order=order, menu_item=menu_item, quantity=quantity)
            total += menu_item.price * quantity

        order.total_price = total
        order.save()
        return order
  
    def update(self, instance, validated_data):
        user = self.context['request'].user

        if not user.is_staff and 'status' in validated_data:
            validated_data.pop('status')

        return super().update(instance, validated_data)

