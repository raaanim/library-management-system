import pytest


@pytest.fixture
def logged_client(request):
    client_obj = request.getfixturevalue("client")
    member_obj = request.getfixturevalue("member")
    with client_obj.session_transaction() as sess:
        sess["member_id"] = member_obj.id
    return client_obj
