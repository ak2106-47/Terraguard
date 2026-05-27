import json
import pytest
from unittest.mock import patch, MagicMock, mock_open
from analyzer.ai_suggester import analyze_with_gpt4


class TestAISuggester:
    """Test AI-powered analysis functionality (Google Gemini backend)."""

    @patch('analyzer.ai_suggester._get_client')
    def test_analyze_success(self, mock_client):
        """Test a successful Gemini analysis."""
        # Mock the Gemini API response (response.text holds the content).
        mock_response = MagicMock()
        mock_response.text = '''
        [
            {
                "type": "Security Risk",
                "line": 8,
                "message": "S3 bucket has public-read ACL which can expose sensitive data to the public."
            },
            {
                "type": "Best Practice",
                "line": 17,
                "message": "Hardcoded AMI ID can lead to issues if the AMI is deregistered or deleted."
            }
        ]
        '''
        mock_client.return_value.models.generate_content.return_value = mock_response

        test_content = '''
        resource "aws_s3_bucket" "test" {
          bucket = "test-bucket"
          acl    = "public-read"
        }
        '''

        with patch("builtins.open", mock_open(read_data=test_content)):
            result = analyze_with_gpt4("test.tf")

            assert len(result) == 2
            assert result[0]["type"] == "Security Risk"
            assert result[1]["type"] == "Best Practice"
            assert "public-read" in result[0]["message"]

    @patch('analyzer.ai_suggester._get_client')
    def test_analyze_handles_markdown_fences(self, mock_client):
        """Gemini often wraps JSON in ```json fences; these should be stripped."""
        mock_response = MagicMock()
        mock_response.text = '```json\n[{"type": "Warning", "line": 1, "message": "Test"}]\n```'
        mock_client.return_value.models.generate_content.return_value = mock_response

        with patch("builtins.open", mock_open(read_data="test content")):
            result = analyze_with_gpt4("test.tf")

            assert len(result) == 1
            assert result[0]["type"] == "Warning"

    @patch('analyzer.ai_suggester._get_client')
    def test_analyze_api_error(self, mock_client):
        """An API error should be caught and return an empty list."""
        mock_client.return_value.models.generate_content.side_effect = Exception("API Error")

        with patch("builtins.open", mock_open(read_data="test content")):
            result = analyze_with_gpt4("test.tf")

            # Should return an empty list on error.
            assert result == []

    @patch('analyzer.ai_suggester._get_client')
    def test_analyze_invalid_json(self, mock_client):
        """Invalid JSON in the response is caught and yields an empty list."""
        mock_response = MagicMock()
        mock_response.text = "Invalid JSON response"
        mock_client.return_value.models.generate_content.return_value = mock_response

        with patch("builtins.open", mock_open(read_data="test content")):
            # The broad except in analyze_with_gpt4 swallows the JSON error.
            result = analyze_with_gpt4("test.tf")
            assert result == []

    def test_analyze_file_not_found(self):
        """A non-existent file is caught and yields an empty list."""
        result = analyze_with_gpt4("nonexistent.tf")
        assert result == []


class TestCodeBERTAnalyzer:
    """Test CodeBERT analysis functionality."""

    def test_codebert_analyzer_initialization(self):
        """Test CodeBERT analyzer initialization."""
        from analyzer.codebert_analyzer import CodeBERTAnalyzer

        # Mock the transformers imports to avoid downloading models in tests.
        with patch('analyzer.codebert_analyzer.RobertaTokenizer'):
            with patch('analyzer.codebert_analyzer.RobertaForSequenceClassification'):
                with patch('analyzer.codebert_analyzer.torch') as mock_torch:
                    mock_torch.argmax.return_value.item.return_value = 1

                    analyzer = CodeBERTAnalyzer()

                    # Verify initialization.
                    assert analyzer.label_map[0] == "None"
                    assert analyzer.label_map[1] == "Best Practice"
                    assert analyzer.label_map[2] == "Security Risk"

    def test_codebert_analyze(self):
        """Test CodeBERT analysis."""
        from analyzer.codebert_analyzer import CodeBERTAnalyzer

        test_code = '''
        resource "aws_s3_bucket" "test" {
          bucket = "test-bucket"
          acl    = "private"
        }
        '''

        with patch('analyzer.codebert_analyzer.RobertaTokenizer') as mock_tokenizer:
            with patch('analyzer.codebert_analyzer.RobertaForSequenceClassification') as mock_model:
                with patch('analyzer.codebert_analyzer.torch') as mock_torch:
                    # Mock tokenizer.
                    mock_tokenizer.from_pretrained.return_value = MagicMock()
                    mock_tokenizer.from_pretrained.return_value.return_tensors = MagicMock()
                    mock_tokenizer.from_pretrained.return_value.truncation = MagicMock()
                    mock_tokenizer.from_pretrained.return_value.padding = MagicMock()

                    # Mock model.
                    mock_model.from_pretrained.return_value = MagicMock()
                    mock_model.from_pretrained.return_value.return_value.logits = MagicMock()

                    # Mock torch.
                    mock_torch.argmax.return_value.item.return_value = 2  # Security Risk

                    analyzer = CodeBERTAnalyzer()
                    result = analyzer.analyze(test_code)

                    assert result == "Security Risk"


if __name__ == "__main__":
    pytest.main([__file__])
