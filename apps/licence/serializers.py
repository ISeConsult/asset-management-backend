from rest_framework import serializers
from apps.assets.serializers import AssetManufacturerSerializer
from apps.licence.models import (
  LicenseCategoryTypes,
  LicenseCategory,
  License,
  LicenseCheckOut
)


class LicenseCategoryTypesSerializer(serializers.ModelSerializer):
    class Meta:
        models = LicenseCategoryTypes
        fields = '__all__'


class LicenseCategoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        models = LicenseCategory
        fields = '__all__'



class LicenseCategoryListSerializer(serializers.ModelSerializer):
    category_type = serializers.SerializerMethodField()

    def get_category_type(self,obj):
        if obj.category_type:
            return {
                'id':obj.category_type.id,
                'uid':obj.category_type.uid,
                'name':obj.category_type.name
            }
        else:
            return None

    class Meta:
        models = LicenseCategory
        fields = '__all__'



class LicenseCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        models = License
        fields = "__all__"


class LicenseListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    manufacturer = serializers.SerializerMethodField()
    licensed_to = serializers.SerializerMethodField()

    def get_category(self,obj):
        if obj.category:
            return {
                'id':obj.category.id,
                'uid':obj.category.uid,
                'name':obj.category.name,
                'category_type':obj.category.category_type.name
            }
        else:
            return None
        
    def get_manufacturer(self, obj):
        if obj.manufacturer:
            return AssetManufacturerSerializer(obj.manufacturer).data
        return None
    
    def get_licensed_to(self,obj):
        if obj.licensed_to:
            return {
                'id':obj.licensed_to.id,
                'uid':obj.licensed_to.uid,
                'full_name': f"{obj.licensed_to.first_name} {obj.licensed_to.last_name}"
            }


    class Meta:
        models = License
        fields = "__all__" 



class LicenseCheckOutCreateUpdateSerializer(serializers.ModelSerializer):
   class Meta:
        models = LicenseCheckOut
        fields = '__all__'


class LicenseCheckOutListSerializer(serializers.ModelSerializer):
    license = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    checkout_by = serializers.SerializerMethodField()

    def get_license(self,obj):
        if obj.license:
            return LicenseListSerializer(obj.license).data
        else:
            return None
        
    def get_user(self, obj):
        if obj.user:
            return {
                "id": obj.user.id,
                "uid": obj.user.uid,
                "full_name": f"{obj.user.first_name} {obj.user.last_name}",
            }
        else:
            return None
        
    def get_checkout_by(self, obj):
        if obj.checkout_by:
            return {
                "id": obj.checkout_by.id,
                "uid": obj.checkout_by.uid,
                "full_name": f"{obj.checkout_by.first_name} {obj.checkout_by.last_name}",
            }
        else:
            return None


    class Meta:
        models = LicenseCheckOut
        fields = '__all__'