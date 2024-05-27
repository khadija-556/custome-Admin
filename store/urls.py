"""
URL configuration for storefront project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from rest_framework_nested import routers
from store.views import *
from pprint import pprint


admin.site.site_header="StoreFront Administration"
admin.site.index_title="Admin"

router  = routers.DefaultRouter()
router.register('product',ProductViewSet , basename="Product-details")
router.register('collection',CollectionViewset)

product_router = routers.NestedDefaultRouter(router, 'product', lookup='product')
product_router.register('reviews', ReviewViewSet, basename='product-review')
pprint(router.urls)

urlpatterns = router.urls + product_router.urls

# urlpatterns = [
    # path('product/', ProductList.as_view(), name="product"),
    # path('product/<int:pk>', ProductDetails.as_view(), name="product"),
    # path('collection/', CollectionList.as_view(), name="collection"),
    # path('collection/<int:pk>', CollectionDetails.as_view(), name="collection"),
    
    
    
    # path('hellow/', hellow, name="hellow"),
    #path('product/<int:pk>', product_details, name="product_details"),
    # path('product/', product, name="product"),
    # path('collection/<int:pk>',collection_details, name="collection_details"),
    # path('collection/', collection, name="collection"),

##]
