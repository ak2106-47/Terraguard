import pytest
import json
import os
from unittest.mock import patch, MagicMock, mock_open
from analyzer.terraform_parser import parse_terraform_file, extract_blocks
from analyzer.rule_engine import check_s3_bucket_acl, check_ec2_name_tag, run_all_checks
from analyzer.output_writer import write_json_output, write_markdown_report


class TestTerraformParser:
    """Test Terraform parsing functionality."""
    
    def test_parse_terraform_file_success(self):
        """Test successful parsing of a valid Terraform file."""
        # Create a temporary test file
        test_content = '''
        provider "aws" {
          region = "us-east-1"
        }
        
        resource "aws_s3_bucket" "test" {
          bucket = "test-bucket"
          acl    = "private"
        }
        '''
        
        with patch("builtins.open", mock_open(read_data=test_content)):
            with patch("hcl2.load") as mock_hcl2:
                mock_hcl2.return_value = {
                    "provider": [{"aws": {"region": "us-east-1"}}],
                    "resource": [{"aws_s3_bucket": {"test": {"bucket": "test-bucket", "acl": "private"}}}]
                }
                
                result = parse_terraform_file("test.tf")
                assert "provider" in result
                assert "resource" in result
    
    def test_parse_terraform_file_not_found(self):
        """Test handling of non-existent file."""
        with pytest.raises(FileNotFoundError):
            parse_terraform_file("nonexistent.tf")
    
    def test_extract_blocks(self):
        """Test extraction of Terraform blocks."""
        parsed_data = {
            "resource": [{"aws_s3_bucket": {"test": {}}}],
            "variable": [{"region": {"type": "string"}}],
            "provider": [{"aws": {"region": "us-east-1"}}],
            "output": [{"bucket_name": {"value": "test"}}],
            "module": [{"vpc": {"source": "./vpc"}}],
            "data": [{"aws_ami": {"ubuntu": {"most_recent": True}}}]
        }
        
        blocks = extract_blocks(parsed_data)
        
        assert "resource" in blocks
        assert "variable" in blocks
        assert "provider" in blocks
        assert "output" in blocks
        assert "module" in blocks
        assert "data" in blocks


class TestRuleEngine:
    """Test rule-based analysis functionality."""
    
    def test_check_s3_bucket_acl_secure(self):
        """Test S3 bucket ACL check with secure configuration."""
        resources = [
            {"aws_s3_bucket": {"secure_bucket": {"acl": "private"}}}
        ]
        
        issues = check_s3_bucket_acl(resources)
        assert len(issues) == 0
    
    def test_check_s3_bucket_acl_insecure(self):
        """Test S3 bucket ACL check with insecure configuration."""
        resources = [
            {"aws_s3_bucket": {"insecure_bucket": {"acl": "public-read"}}}
        ]
        
        issues = check_s3_bucket_acl(resources)
        assert len(issues) == 1
        assert "insecure ACL" in issues[0]
    
    def test_check_ec2_name_tag_present(self):
        """Test EC2 instance with Name tag."""
        resources = [
            {"aws_instance": {"web": {"tags": {"Name": "WebServer"}}}}
        ]
        
        issues = check_ec2_name_tag(resources)
        assert len(issues) == 0
    
    def test_check_ec2_name_tag_missing(self):
        """Test EC2 instance without Name tag."""
        resources = [
            {"aws_instance": {"web": {"instance_type": "t2.micro"}}}
        ]
        
        issues = check_ec2_name_tag(resources)
        assert len(issues) == 1
        assert "missing a 'Name' tag" in issues[0]
    
    def test_run_all_checks(self):
        """Test running all rule checks."""
        blocks = {
            "resource": [
                {"aws_s3_bucket": {"test": {"acl": "public-read"}}},
                {"aws_instance": {"web": {"instance_type": "t2.micro"}}}
            ]
        }
        
        issues = run_all_checks(blocks)
        assert len(issues) >= 1  # At least the S3 ACL issue


class TestOutputWriter:
    """Test output writing functionality."""
    
    def test_write_json_output(self):
        """Test JSON output writing."""
        issues = [
            {"type": "Security Risk", "line": 1, "message": "Test issue"}
        ]
        metadata = {"source": "test", "num_issues": 1}
        
        with patch("builtins.open", mock_open()) as mock_file:
            with patch("os.makedirs"):
                result = write_json_output("test", "test.tf", issues, metadata)
                
                # Verify file was opened for writing
                mock_file.assert_called_once()
                
                # Verify JSON content was written
                written_content = mock_file().write.call_args[0][0]
                json_data = json.loads(written_content)
                
                assert json_data["model"] == "test"
                assert json_data["file_analyzed"] == "test.tf"
                assert len(json_data["issues_detected"]) == 1
    
    def test_write_markdown_report(self):
        """Test Markdown report writing."""
        model_outputs = [
            {
                "model": "GPT-4",
                "file_analyzed": "test.tf",
                "issues_detected": [
                    {"type": "Security Risk", "line": 1, "message": "Test issue"}
                ]
            }
        ]
        
        with patch("builtins.open", mock_open()) as mock_file:
            with patch("os.makedirs"):
                result = write_markdown_report(model_outputs)
                
                # Verify file was opened for writing
                mock_file.assert_called_once()
                
                # Verify Markdown content was written
                written_content = mock_file().write.call_args[0][0]
                assert "# TerraGuard AI Model Comparison Report" in written_content
                assert "GPT-4" in written_content
                assert "Security Risk" in written_content


class TestIntegration:
    """Integration tests for the complete workflow."""
    
    def test_end_to_end_analysis(self):
        """Test complete analysis workflow."""
        # This would test the full pipeline from file parsing to report generation
        # For now, we'll test the components work together
        
        test_content = '''
        resource "aws_s3_bucket" "test" {
          bucket = "test-bucket"
          acl    = "public-read"
        }
        '''
        
        with patch("builtins.open", mock_open(read_data=test_content)):
            with patch("hcl2.load") as mock_hcl2:
                mock_hcl2.return_value = {
                    "resource": [{"aws_s3_bucket": {"test": {"bucket": "test-bucket", "acl": "public-read"}}}]
                }
                
                # Parse the file
                parsed = parse_terraform_file("test.tf")
                blocks = extract_blocks(parsed)
                
                # Run rule checks
                issues = run_all_checks(blocks)
                
                # Should find the S3 ACL issue
                assert len(issues) > 0
                assert any("public-read" in issue for issue in issues)


if __name__ == "__main__":
    pytest.main([__file__])
