from app import app
from kenzie import image

test_client = app.test_client()

def test_upload_using_form_accepts_post_request():
    assert 'POST' in (test_client.options('/upload').headers['Allow']), "Não possui médoto POST"


def test_upload_using_form_does_not_accepts_get_request():
    assert 'GET' not in (test_client.options('/upload').headers['Allow']), "Possui o método GET"
   

def test_json_response_route_files():
    response = test_client.get('/files')
    assert type(response.get_json()) == list, "Não retornou Lista"


def test_files_does_not_accepts_post_request():
    assert 'POST' not in (test_client.options('/files').headers['Allow']), "Possui médoto POST"


def test_filetype_accepts_get_request():
    assert 'GET' in (test_client.options('/files/<string:type_file>').headers['Allow']) , "Não possui médoto GET"


def test_json_response_route_filetype():
    response = test_client.get('/files/<string:type_file>')
    assert type(response.get_json()) == list, "Não retornou Lista"


def test_download_filename_accepts_get_request():
    assert 'GET' in (test_client.options('/download/<string:file_name>').headers['Allow']) , "Não possui médoto GET"


def test_status_code_route_download_filename():
    response = test_client.get('/download/kenzie.jpg')
    assert response.status_code == 200, "Status incorreto"


def test_downloadzip_does_not_accepts_post_request():
    assert 'POST' not in (test_client.options('/download-zip').headers['Allow']), "Possui médoto POST"


def test_downloadzip_accepts_get_request():
    assert 'GET' in (test_client.options('/download-zip').headers['Allow']), "Não possui médoto GET"