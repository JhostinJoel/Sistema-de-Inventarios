from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock
from apps.chatbot.utils import get_chatbot_response

User = get_user_model()

class ChatbotTests(TestCase):
    def setUp(self):
        # Create a user for login required views
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.url = reverse('chatbot:api')

    def test_chat_api_login_required(self):
        """Test that the API requires login."""
        self.client.logout()
        response = self.client.post(self.url, {'message': 'Hello'}, content_type='application/json')
        self.assertNotEqual(response.status_code, 200) # Should be 302 redirect or 403

    def test_chat_api_invalid_method(self):
        """Test that only POST requests are allowed."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    @patch('apps.chatbot.views.get_chatbot_response')
    def test_chat_api_success(self, mock_get_response):
        """Test a successful chat request."""
        self.client.force_login(self.user)
        mock_get_response.return_value = "I am a bot."
        
        data = {'message': 'Hello'}
        response = self.client.post(self.url, data, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'response': 'I am a bot.'})
        mock_get_response.assert_called_with('Hello')

    @patch('apps.chatbot.utils.settings')
    @patch('apps.chatbot.utils.genai')
    def test_utils_success(self, mock_genai, mock_settings):
        """Test the utility function with mocked Gemini API."""
        mock_settings.GEMINI_API_KEY = 'fake-key'
        
        # Mock the model and response
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Gemini response"
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        response = get_chatbot_response("Hola")
        
        self.assertEqual(response, "Gemini response")
        mock_genai.configure.assert_called_with(api_key='fake-key')

    @patch('apps.chatbot.utils.settings')
    def test_utils_missing_key(self, mock_settings):
        """Test utility function when API key is missing."""
        mock_settings.GEMINI_API_KEY = ''
        
        response = get_chatbot_response("Hola")
        
        self.assertIn("Error: API Key de Gemini no configurada", response)

    @patch('apps.chatbot.utils.settings')
    @patch('apps.chatbot.utils.genai')
    def test_utils_api_error(self, mock_genai, mock_settings):
        """Test utility function when Gemini API throws an error."""
        mock_settings.GEMINI_API_KEY = 'fake-key'
        
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_genai.GenerativeModel.return_value = mock_model
        
        response = get_chatbot_response("Hola")
        
        self.assertIn("ocurrió un error", response)
