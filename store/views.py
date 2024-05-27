from itertools import product
from django.shortcuts import render,get_object_or_404
from .models import *
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics  
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.db.models import Count
from .serializers import CollectionSerializer , ProductSerializer ,ReviewSerializer
from rest_framework.generics import ListCreateAPIView ,RetrieveDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .filter import ProductFilter
from rest_framework.filters import SearchFilter , OrderingFilter

from .pagination import *

class ReviewViewSet(ModelViewSet):
    
    serializer_class=ReviewSerializer
    
    def get_queryset(self):
        return Reviews.objects.filter(product_id = self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}




### ModelViewset ###

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend , SearchFilter , OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title']
    ordering_fields = ['last_update','inventory']
    
    pagination_class = DefultPagination
    
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id') ##filtering
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id = collection_id)
    #     return queryset
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    
    
    
class CollectionViewset(ModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count("product")).all()
    serializer_class = CollectionSerializer
    
    ## dosen't work
    def destroy(self, request, *args, **kwargs):
        if Collection.objects.filter(id = kwargs['pk']).count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
  
    
    # def delete(self, request, pk):
    #     collection=get_object_or_404(Collection,pk=pk)
    #     if collection.product.count() > 0:
    #         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
        
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
    

########Generic,Mixin
# class ProductList(ListCreateAPIView):
#     queryset= Product.objects.select_related("collection").all()
#     serializer_class=ProductSerializer

#     def get_serializer_context(self):
#         return {'request': self.request}
    
# class ProductDetails(RetrieveDestroyAPIView):
#     queryset=Product.objects.all()
#     serializer_class=ProductSerializer
    
#     def delete(self,request,pk):
#         product=get_object_or_404(Product,pk=pk)
#         if product.orderitems.count() > 0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
###Collection class GET,POST
# class CollectionList(ListCreateAPIView):
#         queryset=Collection.objects.annotate(product_count=Count("product")).all()
#         serializer_class=CollectionSerializer

# class CollectionDetails(RetrieveDestroyAPIView):
#     queryset=Collection.objects.annotate(product_count=Count("product"))
#     serializer_class=CollectionSerializer
    
#     def delete(self, request, pk):
#         collection=get_object_or_404(Collection,pk=pk)
#         if collection.product.count() > 0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
        
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
        
    
   
    
         
    
   


##### Class-base function class #######
# class ProductList(APIView):
#     def get(self,request):
#         queryset=Product.objects.select_related("collection").all()
#         serializer=ProductSerializer(queryset,many=True,context={'request': request})
#         return Response(serializer.data)
    
#     def post(self,request):
#         serializer=ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

# class ProductDetails(APIView):
#     def get(self,request,pk):
#         object = Product.objects.get(pk=pk)
#         serializer=ProductSerializer(object,context={'request': request})
#         return Response(serializer.data)
    
#     def put(self,request,pk):
#         object = Product.objects.get(pk=pk)
#         serializer=ProductSerializer(object,data=request.data,context={'request': request} )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     def delete(self,request,pk):
#         product=get_object_or_404(Product,pk=pk)
#         if product.orderitems.count() > 0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
       
    
    
        
    
    

# class collection_details(APIView):
#     def get(self,request,pk):
#         if request.method == "GET":
#             object=Collection.objects.get(pk=pk)
#             serializer=CollectionSerializer(object)#Serializer
#             return Response(serializer.data)
    
#     def put(self,request,pk):
#         if request.method == "PUT":
#             object = Collection.objects.get(pk=pk)
#             serializer = CollectionSerializer(object,data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
            
#         return Response(serializer.data)
    
#     def delete(self,request,pk):
#         if request.method == "DELETE":
        
        
        

    
 ##Function base API   
 #single object collection put ,get.delete  
# @api_view(['GET','PUT','DELETE'])   
# def collection_details(request,pk):
#     collection=get_object_or_404(Collection.objects.annotate(product_count=Count("product")),pk=pk)
#     if request.method == "GET":
#         serializer=CollectionSerializer(collection)#Serializer
#         return Response(serializer.data)
    
#     elif request.method == "PUT":
#         serializer = CollectionSerializer(collection,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
    
#     elif request.method == "DELETE":
#         if collection.product.count() > 0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
        
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
        

#List of collection here we have to use get and post method
# @api_view(['GET','POST'])   
# def collection(request):
#     if request.method == "GET":
#         queryset=Collection.objects.annotate(product_count=Count("product")).all()
#         serializer=CollectionSerializer(queryset,many=True)
#         return Response(serializer.data)
       
    # elif request.method == "POST":
    #     serializer=CollectionSerializer(data=request.data)#Desirilizer
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data,status=status.HTTP_201_CREATED)



# #Product list
# @api_view(['GET','POST']) 
# def product(request):
#     if request.method == "GET":
#         queryset=Product.objects.all()
#         serializer=ProductSerializer(queryset,many=True,context={'request': request})
#         return Response(serializer.data)
    
#     elif request.method == "POST":
        
#         serializer=ProductSerializer(data=request.data,context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
# @api_view(['GET','PUT','DELETE'])     
# def product_details(request,pk):
#     product=get_object_or_404(Product,pk=pk)
#     if request.method == "GET":
#         object = Product.objects.get(pk=pk)
#         serializer=ProductSerializer(object,context={'request': request})
#         return Response(serializer.data)
    
#     elif request.method == "PUT":
#         object = Product.objects.get(pk=pk)
#         serializer=ProductSerializer(object,data=request.data,context={'request': request} )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     elif request.method == "DELETE":
#         if product.orderitems.count() > 0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        
    
    
        