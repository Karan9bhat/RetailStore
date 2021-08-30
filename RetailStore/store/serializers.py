from rest_framework import serializers

from .models import Store, Staff, Customer, Order, Contains, Inventory


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"

class StaffSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Staff
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["store"] = StoreSerializer(instance.store_id).data
        return response

class CustomerSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Customer
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Order
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["store"] = StoreSerializer(instance.store_id).data
        return response

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["staff"] = StaffSerializer(instance.staff_id).data
        return response

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["customer"] = CustomerSerializer(instance.cust_id).data
        return response

class InventorySerializer(serializers.ModelSerializer) :
    class Meta:
        model = Inventory
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["store"] = StoreSerializer(instance.store_id).data
        return response

