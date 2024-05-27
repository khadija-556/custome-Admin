from rest_framework import serializers
from .models import *
from store.views import *

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ["id","date","discribtion","name"]
    
    
    
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Reviews.objects.create(product_id = product_id , **validated_data)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id","title","product_count"]
        
    product_count=serializers.IntegerField(read_only=True)
 
 
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = '__all__'
        fields = ["id","title","slug","price","inventory","collection","description"]
    
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # unit_price = serializers.DecimalField(
    #     max_digits=6,
    #     decimal_places=2,
    #     source="price") # how we want to show name in api page
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset = Collection.objects.all()
    # )
    # collection = serializers.StringRelatedField()
    # collection=CollectionSerializer()
    # collection=serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name="collection_details"
     
    # )
    
    

# class ProductSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = Product
    #     fields = "__all__"
        # fields = ['id', 'title', 'slug' ]
    
    



        