from rest_framework.filters import BaseFilterBackend
import coreapi


class ShopFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        fields = [
            coreapi.Field(
                name='name',
                location='queryset',
                required=True,
                type='str',
                description='Filter by user name',
            )
        ]
        return fields

    def filter_queryset(self, request, queryset, view):
        name = request.query_params.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
