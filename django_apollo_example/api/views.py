import json

from ariadne import make_executable_schema, ObjectType, graphql, format_error
from ariadne.constants import PLAYGROUND_HTML
from asgiref.sync import async_to_sync
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views import View

from api.queries import list_posts_resolver

type_defs = """
type Post {
    id: ID!
    slug: String!
    title: String!
    description: String!
    c_on: String!
}

type PostsResult {
    success: Boolean!
    errors: [String]
    post: [Post]
}

type Query {
    listPosts: PostsResult!
    hello: String!
}
"""


def resolve_hello(_, info):
    request = info.context["environ"]
    user_agent = request.get("HTTP_USER_AGENT", "guest")
    return "Hello, %s!" % user_agent


query = ObjectType("Query")
# query.set_field("listPosts", list_posts_resolver)
query.set_field("hello", resolve_hello)

# Create executable schema instance
schema = make_executable_schema(type_defs, query)


# Create GraphQL view
class GraphQLView(View):
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # bet keep on mind this will nor prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    def get(self, *args, **kwargs):
        return HttpResponse(PLAYGROUND_HTML)

    # GraphQL queries are always sent as POSTd
    @async_to_sync
    async def post(self, request, *args, **kwargs):
        # Reject requests that aren't JSON
        if request.content_type != "application/json":
            return HttpResponseBadRequest()

        # Naively read data from JSON request
        _d = dict(
            variables=dict(),
            query="",
            operationName="hello"
        )
        try:
            data = json.loads(json.dumps(_d))
        except ValueError:
            return HttpResponseBadRequest()

        # Check if instance data is not empty and dict
        if not data or not isinstance(data, dict):
            return HttpResponseBadRequest()

        # Check if variables are dict:
        variables = data.get("variables")
        if variables and not isinstance(variables, dict):
            return HttpResponseBadRequest()

        # Execute the query
        success, result = await graphql(
            schema,
            data.get("query"),
            context=request,  # expose request as info.context
            variables=data.get("variables"),
            operation_name=data.get("operationName"),
        )

        # Build valid GraphQL API response
        status = 200
        response = {}
        print(result)
        # if result.errors:
        #     response["errors"] = list(map(format_error, result.errors))

        # if result.invalid:
        #     status = 400
        # else:

        # response["data"] = result.data

        # Send response to client
        return JsonResponse(result, status=status)

# from ariadne import (
#     graphql_sync,
#     ObjectType,
#     snake_case_fallback_resolvers,
#     make_executable_schema,
#     load_schema_from_path,
# )
# from ariadne.constants import PLAYGROUND_HTML
# from django.conf import settings
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.views.generic.base import View
#
# from api.queries import list_posts_resolver
#
# # from utils.api_utils import render_api_response
#
# # GRAPHQL SCHEMA DEFINE
# query = ObjectType("Query")
# query.set_field("listPosts", list_posts_resolver)
#
# SCHEMA_PATH = settings.BASE_DIR / "schema.graphql"
# TYPE_DEFS = load_schema_from_path(SCHEMA_PATH.__str__())
# SCHEMA = make_executable_schema(TYPE_DEFS, snake_case_fallback_resolvers)
#
#
# class GQLView(View):
#     def get(self, *args, **kwargs):
#         return HttpResponse(PLAYGROUND_HTML)
#
#     @csrf_exempt
#     def post(self, *args, **kwargs):
#         data = self.request.POST
#         success, result = graphql_sync(
#             SCHEMA, data, context_value=self.request.POST, debug=settings.DEBUG
#         )
#
#         return JsonResponse(result)
#         # return render_api_response([result], success=success, code="ANS02")
