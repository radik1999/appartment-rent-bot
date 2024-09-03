from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class HomeView(APIView):
    @extend_schema(
        request=None,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Successful response",
                response=inline_serializer(name="HomeViewSuccessResponse", fields={"status": serializers.CharField()}),
            )
        },
    )
    def get(self, request: Request) -> Response:
        return Response({"status": "OK"}, status.HTTP_200_OK)
