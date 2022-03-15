from django.urls import path

from api.views import GraphQLView

urlpatterns = [
    path("gql/<uuid:request_slug>/", GraphQLView.as_view(), name="GQLView-apollo"),
]
