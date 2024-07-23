import unittest
from unittest.mock import patch, MagicMock
#from tutorials.tutorial_llms.hopenai import get_completion
import hopenai


class TestGetCompletion(unittest.TestCase):
    #@patch('tutorials.tutorial_llms.hopenai.OpenAI')
    @patch('hopenai.OpenAI')
    def test_get_completion_mock1(self, mock_openai):
        # Arrange
        mock_openai().chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Test content"))])
        user = "Test user"
        system = "Test system"
        model = "Test model"
        # Act
        result = hopenai.get_completion(user, system=system, model=model)
        # Assert
        self.assertEqual(result, "Test content")
        mock_openai().chat.completions.create.assert_called_once_with(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ]
        )

    def test_get_completion1(self):
        user = "Test user"
        system = "Test system"
        model = "gpt-4o-mini"
        # Act.
        result = hopenai.get_completion(user, system=system, model=model)
        print(result)
        # Assert.
        self.assertEqual(result, "Hello! How can I assist you today?")

if __name__ == '__main__':
    unittest.main()
