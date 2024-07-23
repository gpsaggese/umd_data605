import unittest
from unittest.mock import patch, MagicMock
import hopenai


class TestGetCompletion(unittest.TestCase):

    @patch('hopenai.OpenAI')
    def test_get_completion_mock1(self, mock_openai: MagicMock) -> None:
        # Prepare inputs.
        mock_openai().chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Test content"))])
        user = "Test user"
        system = "Test system"
        model = "Test model"
        # Test.
        result = hopenai.get_completion(user, system=system, model=model)
        # Check.
        self.assertEqual(result, "Test content")
        mock_openai().chat.completions.create.assert_called_once_with(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ]
        )

    def test_get_completion1(self) -> None:
        # Prepare inputs.
        user = "Test user"
        system = "Test system"
        model = "gpt-4o-mini"
        # Test.
        result = hopenai.get_completion(user, system=system, model=model)
        print(result)
        # Check.
        exp_result = "Hello! How can I assist you today?"
        self.assertEqual(result, exp_result)

    def test_get_completion2(self) -> None:
        # Prepare inputs.
        user = "She no went to the market."
        system = "You will be provided with statements, and your task is to convert them to standard English."
        model = "gpt-4o-mini"
        create_kwargs = {
            "temperature": 0.0,
            "max_tokens": 64,
            "top_p": 1
        }
        # Test.
        result = hopenai.get_completion(user, system=system, model=model,
                                        **create_kwargs)
        print(result)
        # Check.
        exp_result = "She didn't go to the market."
        self.assertEqual(result, exp_result)


if __name__ == '__main__':
    unittest.main()
