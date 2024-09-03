
import urllib
from django.urls import reverse
import pytest

from rest_framework.test import APIRequestFactory

from django.core.handlers.wsgi import WSGIRequest

from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_request():
    def get_view_by_name(
        view_name: str,
        method_name: str = "get",
        url_args: list | None = None,
        url_kwargs: dict | None = None,
        request_body: dict | list | None = None,
        request_format: str = "json",
        query_params: dict | None = None,
    ) -> WSGIRequest:
        factory = APIRequestFactory()
        url = reverse(view_name, args=url_args, kwargs=url_kwargs)
        if query_params:
            url += "?" + urllib.parse.urlencode(query_params)
        factory_method = getattr(factory, method_name)
        request = factory_method(url, data=request_body, format=request_format)

        return request

    return get_view_by_name
