import pytest
from rest_framework import status

from home.views import HomeView
from tests.variants import Variant


variants = [
    (
        "Home view",
        Variant(
            name="home",
            view=HomeView.as_view(),
            expected={"status": "OK"},
            status_code=status.HTTP_200_OK,
        ),
    ),
]



@pytest.mark.parametrize("test_name, variant", variants)
def test_home(api_request, test_name, variant):
    response = variant.view(
        api_request(
            variant.name,
            method_name=variant.method_name,
        )
    )

    assert response.data == variant.expected
    assert response.status_code == variant.status_code
