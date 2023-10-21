from django.urls import path
from .views import (ClothingCreateView,
                    ClothingDeleteView,
                    ClothingFilterView,
                    ShoesSearchListView,
                    clothing_detail,
                  )

urlpatterns = [
    path("get-shoes-list/<str:text>/", ShoesSearchListView.as_view()),
    path('shoes-create/', ClothingCreateView.as_view(), name='clothing-create'),
    path('shoes/delete/<int:pk>/', ClothingDeleteView.as_view(), name='clothing-delete'),
    path('all-shoes/', ClothingFilterView.as_view(), name='all-shoes'),
    path('clothing-detail/<int:id>/', clothing_detail, name='clothing-detail'),

    # web-site uchun search
]
