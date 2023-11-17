"""Test the main module"""

import pytest
from fastapi.testclient import TestClient

from app.main import app, get_template

client = TestClient(app)


async def mock_get_template():
    """Mock the get_template function"""
    return "<html><body><h1>Hello {{ message }}</h1></body></html>"


app.dependency_overrides[get_template] = mock_get_template


@pytest.mark.parametrize(
    "input_data, expected",
    [
        (
            {
                "name": "test",
                "templateUrl": "https://mock-template/example1/",
                "data": {"message": "World"},
            },
            {"statusCode": 200, "mediaType": "application/pdf"},
        ),
        (
            {
                "name": "test",
                "templateUrl": "https://mock-template/example2/",
            },
            {"statusCode": 200, "mediaType": "application/pdf"},
        ),
    ],
)
def test_create_pdf_report_ok(input_data, expected):
    """Test the creation of a pdf report with success"""

    response = client.post("/v1/report", json=input_data)
    assert response.status_code == expected["statusCode"]
    assert response.headers["content-type"] == expected["mediaType"]


@pytest.mark.parametrize(
    "input_data, expected",
    [
        (
            {
                "templateUrl": "https://mock-template/example/",
                "data": {"message": "World"},
            },
            {
                "detail": [
                    {
                        "type": "missing",
                        "loc": ["body", "name"],
                        "msg": "Field required",
                        "input": {
                            "templateUrl": "https://mock-template/example/",
                            "data": {"message": "World"},
                        },
                        "url": "https://errors.pydantic.dev/2.5/v/missing",
                    }
                ]
            },
        ),
        (
            {
                "name": "test",
                "data": {"message": "World"},
            },
            {
                "detail": [
                    {
                        "type": "missing",
                        "loc": ["body", "templateUrl"],
                        "msg": "Field required",
                        "input": {
                            "name": "test",
                            "data": {"message": "World"},
                        },
                        "url": "https://errors.pydantic.dev/2.5/v/missing",
                    }
                ]
            },
        ),
        (
            {"data": {"message": "World"}},
            {
                "detail": [
                    {
                        "type": "missing",
                        "loc": ["body", "name"],
                        "msg": "Field required",
                        "input": {
                            "data": {"message": "World"},
                        },
                        "url": "https://errors.pydantic.dev/2.5/v/missing",
                    },
                    {
                        "type": "missing",
                        "loc": ["body", "templateUrl"],
                        "msg": "Field required",
                        "input": {
                            "data": {"message": "World"},
                        },
                        "url": "https://errors.pydantic.dev/2.5/v/missing",
                    },
                ]
            },
        ),
        # (
        #     None,
        #     {
        #         "detail": [
        #             {
        #                 "type": "missing",
        #                 "loc": [
        #                     "body"
        #                 ],
        #                 "msg": "Field required",
        #                 "input": "null",
        #                 "url": "https://errors.pydantic.dev/2.4/v/missing"
        #             },
        #             {
        #                 "type": "missing",
        #                 "loc": [
        #                     "body"
        #                 ],
        #                 "msg": "Field required",
        #                 "input": "null",
        #                 "url": "https://errors.pydantic.dev/2.4/v/missing"
        #             }
        #         ]
        #     }
        # ),
    ],
)
def test_create_report_error(input_data, expected):
    """Test the creation of a pdf report with error"""

    response = client.post("/v1/report", json=input_data)
    assert response.status_code == 422
    assert response.json() == expected
