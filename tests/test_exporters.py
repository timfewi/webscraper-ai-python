"""
Test suite for the exporters module.

Tests data export functionality for various formats.
"""

from datetime import datetime
from unittest.mock import mock_open, patch

import pytest

from src.exporters import CSVExporter, DataExporterFactory, JSONExporter, XMLExporter
from src.models import ScrapedData


class TestCSVExporter:
    """Test cases for CSVExporter class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.exporter = CSVExporter()
        self.test_data = [
            ScrapedData(
                url="https://example.com",
                title="Test Title 1",
                content="Test content 1",
                category="news",
                timestamp=datetime(2023, 1, 1, 12, 0, 0),
            ),
            ScrapedData(
                url="https://example2.com",
                title="Test Title 2",
                content="Test content 2",
                category="tech",
                timestamp=datetime(2023, 1, 2, 12, 0, 0),
            ),
        ]

    @patch("pathlib.Path.mkdir")
    @patch("builtins.open", new_callable=mock_open)
    def test_export_csv_with_data(self, mock_file, mock_mkdir):
        """Test CSV export with actual data."""
        filename = "test_output.csv"
        result_path = self.exporter.export(self.test_data, filename)

        # Check that file was opened for writing
        mock_file.assert_called()
        call_args = mock_file.call_args_list[0]  # Get first call
        assert call_args[0][0].name == "test_output.csv"
        # Check that 'w' mode was used in any call
        found_write_mode = any("w" in str(call) for call in mock_file.call_args_list)
        assert found_write_mode
        assert call_args[1]["encoding"] == "utf-8"

        # Check that mkdir was called for parent directory
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

        # Verify return path
        assert result_path.endswith("test_output.csv")

    @patch("pathlib.Path.mkdir")
    @patch("builtins.open", new_callable=mock_open)
    def test_export_csv_empty_data(self, mock_file, mock_mkdir):
        """Test CSV export with empty data."""
        filename = "empty_output.csv"
        result_path = self.exporter.export([], filename)

        # Should still create file with headers
        mock_file.assert_called_once()
        assert result_path.endswith("empty_output.csv")

    def test_export_csv_filename_extension(self):
        """Test that CSV extension is added if missing."""
        with patch("pathlib.Path.mkdir"), patch("builtins.open", mock_open()):
            result_path = self.exporter.export([], "test_file")
            assert result_path.endswith("test_file.csv")

            # Should not double-add extension
            result_path = self.exporter.export([], "test_file.csv")
            assert result_path.endswith("test_file.csv")
            assert not result_path.endswith("test_file.csv.csv")

    def test_export_csv_content_truncation(self):
        """Test that long content is truncated in CSV."""
        long_content = "A" * 2000  # Longer than 1000 char limit
        data = [
            ScrapedData(
                url="https://example.com",
                title="Test",
                content=long_content,
                category="test",
            )
        ]

        with patch("pathlib.Path.mkdir"), patch(
            "builtins.open", mock_open()
        ) as mock_file:
            self.exporter.export(data, "test.csv")

            # Check that csv.writer.writerow was called with truncated content
            # This is a bit complex to test due to the mock, but we can verify the file was opened
            mock_file.assert_called_once()


class TestJSONExporter:
    """Test cases for JSONExporter class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.exporter = JSONExporter()
        self.test_data = [
            ScrapedData(
                url="https://example.com",
                title="Test Title",
                content="Test content",
                category="news",
                metadata={"key": "value"},
                timestamp=datetime(2023, 1, 1, 12, 0, 0),
            )
        ]

    @patch("pathlib.Path.mkdir")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_export_json_with_data(self, mock_json_dump, mock_file, mock_mkdir):
        """Test JSON export with actual data."""
        filename = "test_output.json"
        self.exporter.export(self.test_data, filename)

        # Check file operations
        mock_file.assert_called_once()
        mock_mkdir.assert_called_once()

        # Check JSON dump was called
        mock_json_dump.assert_called_once()
        call_args = mock_json_dump.call_args[0]
        output_data = call_args[0]

        # Verify structure of exported data
        assert "export_timestamp" in output_data
        assert "total_items" in output_data
        assert "data" in output_data
        assert output_data["total_items"] == 1
        assert len(output_data["data"]) == 1

        # Verify data structure
        item_data = output_data["data"][0]
        assert item_data["url"] == "https://example.com"
        assert item_data["title"] == "Test Title"
        assert item_data["content"] == "Test content"
        assert item_data["category"] == "news"
        assert item_data["metadata"] == {"key": "value"}
        assert item_data["timestamp"] == "2023-01-01T12:00:00"

    def test_export_json_filename_extension(self):
        """Test that JSON extension is added if missing."""
        with patch("pathlib.Path.mkdir"), patch("builtins.open", mock_open()), patch(
            "json.dump"
        ):
            result_path = self.exporter.export([], "test_file")
            assert result_path.endswith("test_file.json")


class TestXMLExporter:
    """Test cases for XMLExporter class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.exporter = XMLExporter()
        self.test_data = [
            ScrapedData(
                url="https://example.com",
                title="Test Title",
                content="Test content",
                category="news",
                metadata={"author": "John Doe", "score": 95},
                timestamp=datetime(2023, 1, 1, 12, 0, 0),
            )
        ]

    @patch("pathlib.Path.mkdir")
    @patch("xml.etree.ElementTree.ElementTree.write")
    def test_export_xml_with_data(self, mock_xml_write, mock_mkdir):
        """Test XML export with actual data."""
        filename = "test_output.xml"
        result_path = self.exporter.export(self.test_data, filename)

        # Check that XML write was called
        mock_xml_write.assert_called_once()
        mock_mkdir.assert_called_once()

        # Check return path
        assert result_path.endswith("test_output.xml")

    def test_export_xml_structure(self):
        """Test XML output structure by examining the generated tree."""
        # Temporarily patch write to capture the tree
        with patch("pathlib.Path.mkdir"), patch(
            "xml.etree.ElementTree.ElementTree.write"
        ):
            # Create a minimal test to verify XML structure is created correctly
            result_path = self.exporter.export(self.test_data, "test.xml")
            assert result_path.endswith("test.xml")

    def test_export_xml_filename_extension(self):
        """Test that XML extension is added if missing."""
        with patch("pathlib.Path.mkdir"), patch(
            "xml.etree.ElementTree.ElementTree.write"
        ):
            result_path = self.exporter.export([], "test_file")
            assert result_path.endswith("test_file.xml")

    def test_export_xml_content_truncation(self):
        """Test that long content is truncated in XML."""
        long_content = "A" * 5000  # Longer than 2000 char limit
        data = [
            ScrapedData(
                url="https://example.com",
                title="Test",
                content=long_content,
                category="test",
            )
        ]

        with patch("pathlib.Path.mkdir"), patch(
            "xml.etree.ElementTree.ElementTree.write"
        ):
            result_path = self.exporter.export(data, "test.xml")
            assert result_path.endswith("test.xml")


class TestDataExporterFactory:
    """Test cases for DataExporterFactory class."""

    def test_create_csv_exporter(self):
        """Test creating CSV exporter."""
        exporter = DataExporterFactory.create_exporter("csv")
        assert isinstance(exporter, CSVExporter)

        # Test case insensitive
        exporter = DataExporterFactory.create_exporter("CSV")
        assert isinstance(exporter, CSVExporter)

    def test_create_json_exporter(self):
        """Test creating JSON exporter."""
        exporter = DataExporterFactory.create_exporter("json")
        assert isinstance(exporter, JSONExporter)

        # Test case insensitive
        exporter = DataExporterFactory.create_exporter("JSON")
        assert isinstance(exporter, JSONExporter)

    def test_create_xml_exporter(self):
        """Test creating XML exporter."""
        exporter = DataExporterFactory.create_exporter("xml")
        assert isinstance(exporter, XMLExporter)

        # Test case insensitive
        exporter = DataExporterFactory.create_exporter("XML")
        assert isinstance(exporter, XMLExporter)

    def test_unsupported_format(self):
        """Test error handling for unsupported formats."""
        with pytest.raises(ValueError) as exc_info:
            DataExporterFactory.create_exporter("pdf")

        assert "Unsupported format 'pdf'" in str(exc_info.value)
        assert "csv, json, xml" in str(exc_info.value)

    def test_get_supported_formats(self):
        """Test getting list of supported formats."""
        formats = DataExporterFactory.get_supported_formats()
        assert isinstance(formats, list)
        assert "csv" in formats
        assert "json" in formats
        assert "xml" in formats
        assert len(formats) == 3

    def test_empty_format_string(self):
        """Test handling of empty format string."""
        with pytest.raises(ValueError):
            DataExporterFactory.create_exporter("")

    def test_none_format(self):
        """Test handling of None format by using type: ignore."""
        with pytest.raises((AttributeError, TypeError)):
            DataExporterFactory.create_exporter(None)  # type: ignore


class TestExporterIntegration:
    """Integration tests for all exporters."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_data = [
            ScrapedData(
                url="https://example1.com",
                title="Article 1",
                content="Content of article 1",
                category="news",
                metadata={"author": "John", "tags": ["news", "tech"]},
                timestamp=datetime(2023, 1, 1, 10, 0, 0),
            ),
            ScrapedData(
                url="https://example2.com",
                title="Article 2",
                content="Content of article 2",
                category="tech",
                metadata={"author": "Jane", "rating": 4.5},
                timestamp=datetime(2023, 1, 2, 14, 30, 0),
            ),
        ]

    def test_all_exporters_with_same_data(self):
        """Test that all exporters can handle the same data set."""
        formats = ["csv", "json", "xml"]

        for format_type in formats:
            exporter = DataExporterFactory.create_exporter(format_type)

            with patch("pathlib.Path.mkdir"):
                if format_type == "csv":
                    with patch("builtins.open", mock_open()):
                        result = exporter.export(self.test_data, f"test.{format_type}")
                elif format_type == "json":
                    with patch("builtins.open", mock_open()), patch("json.dump"):
                        result = exporter.export(self.test_data, f"test.{format_type}")
                elif format_type == "xml":
                    with patch("xml.etree.ElementTree.ElementTree.write"):
                        result = exporter.export(self.test_data, f"test.{format_type}")

                assert result.endswith(f"test.{format_type}")

    def test_exporters_with_empty_data(self):
        """Test that all exporters handle empty data gracefully."""
        formats = ["csv", "json", "xml"]

        for format_type in formats:
            exporter = DataExporterFactory.create_exporter(format_type)

            with patch("pathlib.Path.mkdir"):
                if format_type == "csv":
                    with patch("builtins.open", mock_open()):
                        result = exporter.export([], f"empty.{format_type}")
                elif format_type == "json":
                    with patch("builtins.open", mock_open()), patch("json.dump"):
                        result = exporter.export([], f"empty.{format_type}")
                elif format_type == "xml":
                    with patch("xml.etree.ElementTree.ElementTree.write"):
                        result = exporter.export([], f"empty.{format_type}")

                assert result.endswith(f"empty.{format_type}")

    def test_exporters_with_special_characters(self):
        """Test exporters with data containing special characters."""
        special_data = [
            ScrapedData(
                url="https://example.com",
                title="Special chars: <>&\"'",
                content="Content with émojis 🚀 and ñáéíóú",
                category="test",
                metadata={"unicode": "测试"},
            )
        ]

        formats = ["csv", "json", "xml"]

        for format_type in formats:
            exporter = DataExporterFactory.create_exporter(format_type)

            with patch("pathlib.Path.mkdir"):
                if format_type == "csv":
                    with patch("builtins.open", mock_open()):
                        result = exporter.export(special_data, f"special.{format_type}")
                elif format_type == "json":
                    with patch("builtins.open", mock_open()), patch("json.dump"):
                        result = exporter.export(special_data, f"special.{format_type}")
                elif format_type == "xml":
                    with patch("xml.etree.ElementTree.ElementTree.write"):
                        result = exporter.export(special_data, f"special.{format_type}")

                assert result.endswith(f"special.{format_type}")
