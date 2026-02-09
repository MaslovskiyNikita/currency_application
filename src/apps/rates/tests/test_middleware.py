import zlib
import pytest
from django.http import HttpResponse
from django.test import RequestFactory
from src.apps.common.middleware import SignatureCRC32Middleware


@pytest.fixture
def rf():
    return RequestFactory()


def _get_response_mock(content=b'{"ok": true}', status=200):
    
    def handler(request):
        return HttpResponse(
            content=content, 
            status=status, 
            content_type="application/json"
        )
    return handler


def test_adds_header_for_api_path(rf):

    request = rf.get("/api/v1/rates/rate/")
    
    middleware = SignatureCRC32Middleware(_get_response_mock())

    response = middleware(request)

    assert "X-Response-Signature" in response

    expected_hash = zlib.crc32(response.content) & 0xFFFFFFFF
    assert response["X-Response-Signature"] == f"{expected_hash:08x}"


def test_no_header_for_non_api_path(rf):

    request = rf.get("/admin/")
    
    middleware = SignatureCRC32Middleware(_get_response_mock())
    response = middleware(request)

    assert "X-Response-Signature" not in response


def test_no_header_for_empty_content(rf):

    request = rf.get("/api/v1/rates/rate/")

    middleware = SignatureCRC32Middleware(_get_response_mock(content=b""))
    response = middleware(request)

    assert "X-Response-Signature" not in response


def test_checksum_is_deterministic(rf):

    content = b'{"data": "hello world"}'

    mock_response = _get_response_mock(content=content)
    
    middleware = SignatureCRC32Middleware(mock_response)

    response1 = middleware(rf.get("/api/v1/test/"))
    response2 = middleware(rf.get("/api/v1/test/"))

    assert response1["X-Response-Signature"] == response2["X-Response-Signature"]