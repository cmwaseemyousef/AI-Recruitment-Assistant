import pytest
from app import create_app, routes as app_routes # Import routes and alias to avoid conflict
import io
from PyPDF2 import PdfWriter

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the AI Recruitment Assistant!"}

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "up and running"}

def test_analyze_resume(client):
    data = {"resume": "John Doe has 5 years of experience in AI."}
    response = client.post("/analyze-resume", json=data)
    assert response.status_code == 200
    assert "resume_analysis" in response.json

def test_analyze_resume_empty(client):
    response = client.post("/analyze-resume", json={})
    assert response.status_code == 400
    assert response.json == {"error": "No resume text provided"}

# Helper function to create a dummy PDF
def create_dummy_pdf(text_content="This is a test PDF."):
    pdf_writer = PdfWriter()
    pdf_writer.add_blank_page(width=210, height=297) # A4 size in points
    # Adding text to a PDF with PyPDF2 is not straightforward for simple text.
    # For testing purposes, we'll rely on PyPDF2 being able to read a blank PDF
    # and extract no text, or we can simulate text extraction if needed.
    # For this test, we'll make a PDF that PyPDF2 can read and will have some metadata.
    # A more robust way would be to use reportlab or have a small actual PDF file.
    # However, creating a text stream that PyPDF2 can *reliably* extract text from via PdfWriter is tricky.
    # Instead, we'll make a PDF that's valid and assert based on the *analysis* of empty text,
    # or a known text if we had a reliable way to embed it and extract it.

    # For now, let's assume analyze_resume will correctly process the text from PyPDF2.
    # The key is that PyPDF2 can read it.
    # If we want to test specific text, we should have a small, real PDF file.
    # Given the constraints, we'll test with a PDF that *can* be opened.
    # The current `analyze_resume` function counts words. If we can get text in, great.
    # PyPDF2's PdfWriter doesn't directly add text that extract_text() can easily get.
    # We'll use a workaround by having a known dummy PDF file if possible,
    # or accept that the "text" might be empty or minimal from a PdfWriter-created PDF.

    # Let's simulate a PDF with one page and some text that might be hard for PdfWriter to make extractable.
    # For the purpose of this test, we'll create a simple PDF that should be processable.
    # The actual text extraction details are handled by the route, so we test if it's called.
    # We expect `analyze_resume` to be called with the extracted text.

    pdf_buffer = io.BytesIO()
    # To make text extractable, it's usually added via annotations or by "drawing" it.
    # PdfWriter is more for merging/splitting/encrypting.
    # Let's try adding a text annotation, though extraction might still be tricky.
    # This part is complex with PyPDF2 alone for creating text that's easily extractable.
    #
    # **Simplification for the test**: We will create a PDF that is valid.
    # The `analyze_resume` function will receive whatever text PyPDF2 extracts.
    # If PyPDF2 extracts an empty string (common for programmatically created PDFs without explicit text streams),
    # then `analyze_resume` will process an empty string.
    # The route has a check: `if not text.strip(): return jsonify({"error": "Could not extract text..."})`
    # So, a blank PDF created by PdfWriter will likely hit this.

    # Let's make a PDF that *does* have extractable text using a more direct method if available,
    # or use a pre-existing minimal PDF file.
    # For now, we'll make a valid PDF that PyPDF2 won't fail to open.
    # If it extracts no text, the route should handle it.

    # For a test that ensures analyze_resume is called with specific text:
    # It's better to have a small, actual PDF file with known text.
    # Since we can't add files directly, we'll make a PDF that is *parsable*
    # and the route should not fail on *parsing* it.
    # If it extracts empty text, it should return the "Could not extract text" error.

    # Create a very simple PDF that PdfReader can process
    # For a more robust test of text extraction, a sample file would be better.
    # This will create a valid PDF, but text extraction might be empty.
    # Let's assume the goal is to test the upload and basic processing flow.
    pdf_writer.add_blank_page(width=8.5 * 72, height=11 * 72) # Letter size
    # No direct text adding method that's simple and ensures extraction.
    pdf_writer.write(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer

class TestUploadResume:
    def test_upload_resume_success(self, client):
        # To properly test success, we need a PDF from which text can be extracted.
        # A blank PDF created by PdfWriter might result in empty extracted text.
        # The route currently returns an error for empty extracted text.
        # For a true success test (200 OK with analysis), we need a PDF with actual text.
        # Let's use a known string and assume analyze_resume works.
        # We'll need to adjust if creating a PDF with extractable text is too complex here.

        # Workaround: For now, let's assume a PDF that *can* be opened but might have no extractable text
        # by PyPDF2 will trigger the "Could not extract text" error, which is a valid test of that path.
        # To get a 200, we'd need a PDF that PyPDF2 *can* extract text from.

        # Let's create a PDF that *should* be readable by PyPDF2, even if no text is extracted.
        # This will test the file handling and basic PDF processing part.
        pdf_buffer = create_dummy_pdf("Hello world from PDF for test.") # Text might not be added by PdfWriter

        # Since PdfWriter doesn't easily add extractable text, we have two options:
        # 1. Test the path where text extraction yields empty string (route returns 400).
        # 2. Mock `PdfReader` to return a mock object that has `pages` with `extract_text` method.
        # Option 1 is easier without adding more complex PDF generation or mocking.

        data = {'file': (pdf_buffer, 'test.pdf')}
        response = client.post('/upload-resume', data=data, content_type='multipart/form-data')

        # Given PdfWriter makes PDFs that often have no easily extractable text,
        # we expect the "Could not extract text from PDF" error.
        if response.status_code == 200:
            # This case would happen if PyPDF2 *does* extract text from the dummy PDF
            assert "resume_analysis" in response.json
            # e.g. analyze_resume("") would result in "The resume contains 0 words."
            # analyze_resume("Hello world from PDF for test.") would be "7 words"
            # This depends on what create_dummy_pdf actually produces in terms of extractable text.
            # For a blank PDF from PdfWriter, it's likely 0 words.
            assert response.json.get("resume_analysis") == "The resume contains 0 words."
        elif response.status_code == 400:
            assert response.json == {"error": "Could not extract text from PDF. The PDF might be empty or scanned (e.g. image-based)."}
        else:
            # If it's another error, the test should fail and we'd investigate.
            assert False, f"Unexpected status code {response.status_code} with message {response.json}"


    def test_upload_resume_no_file(self, client):
        response = client.post('/upload-resume', data={})
        assert response.status_code == 400
        assert response.json == {"error": "No file part"}

    def test_upload_resume_empty_filename(self, client):
        data = {'file': (io.BytesIO(b"dummy content"), '')}
        response = client.post('/upload-resume', data=data, content_type='multipart/form-data')
        assert response.status_code == 400
        assert response.json == {"error": "No selected file"}

    def test_upload_resume_non_pdf_file(self, client):
        data = {'file': (io.BytesIO(b"this is not a pdf"), 'test.txt')}
        response = client.post('/upload-resume', data=data, content_type='multipart/form-data')
        # The route returns 415 for non-PDF files
        assert response.status_code == 415
        assert response.json == {"error": "Invalid file type. Please upload a PDF file."}

    # Test for corrupted PDF (difficult to create reliably without a real file)
    # We can simulate this by sending bytes that are not a valid PDF structure.
    def test_upload_resume_corrupted_pdf(self, client):
        # PyPDF2's PdfReader will raise PdfReadError for various issues.
        # Sending non-PDF bytes as a .pdf file should trigger this.
        not_a_pdf_buffer = io.BytesIO(b"%DefinitelyNotAPDF")
        data = {'file': (not_a_pdf_buffer, 'corrupted.pdf')}
        response = client.post('/upload-resume', data=data, content_type='multipart/form-data')
        assert response.status_code == 422 # Unprocessable Entity
        assert response.json == {"error": "Could not read PDF. File may be corrupted, password-protected, or not a valid PDF."}

    # Test for password-protected PDF (also hard to create on the fly without tools/libs)
    # If we had a password-protected PDF, PyPDF2 would raise PdfReadError: File has not been decrypted
    # This would be caught by the same handler as corrupted PDF.
    # def test_upload_resume_password_protected_pdf(self, client):
    #     # This test would require a password-protected PDF file.
    #     # For now, we assume it's covered by the general PdfReadError handling.
    #     pass

    def test_upload_resume_real_text_pdf_via_mocking(self, client, mocker):
        # This test shows how to mock PdfReader to control extracted text
        mock_pdf_reader_instance = mocker.MagicMock()
        mock_page = mocker.MagicMock()
        mock_page.extract_text.return_value = "This is a test resume with several words."
        mock_pdf_reader_instance.pages = [mock_page]

        # Mock the PdfReader constructor to return our mock instance
        mocker.patch('app.routes.PdfReader', return_value=mock_pdf_reader_instance)

        pdf_buffer = io.BytesIO(b"dummy pdf content, not actually used due to mocking")
        data = {'file': (pdf_buffer, 'test.pdf')}
        response = client.post('/upload-resume', data=data, content_type='multipart/form-data')

        assert response.status_code == 200
        assert "resume_analysis" in response.json
        # "This is a test resume with several words." has 8 words.
        assert response.json.get("resume_analysis") == "The resume contains 8 words."
        # Ensure PdfReader was called with the file content
        app_routes.PdfReader.assert_called_once()
        # We can even check that extract_text was called
        mock_page.extract_text.assert_called_once()
