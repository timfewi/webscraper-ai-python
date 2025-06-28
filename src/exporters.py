"""
Data export implementation.

This module handles exporting scraped data to various formats,
following the Single Responsibility Principle.
"""

import csv
from datetime import datetime
import json
from pathlib import Path
from typing import Callable, Dict, List
import xml.etree.ElementTree as ET

from .interfaces import IDataExporter
from .models import ScrapedData


class CSVExporter(IDataExporter):
    """Exports scraped data to CSV format."""

    def export(self, data: List[ScrapedData], filename: str) -> str:
        """
        Export scraped data to CSV file.

        Args:
            data: List of scraped data
            filename: Output filename

        Returns:
            Path to exported file
        """
        if not filename.endswith(".csv"):
            filename += ".csv"

        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        if not data:
            # Create empty file with headers
            with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["url", "title", "content", "category", "timestamp"])
            return str(filepath.absolute())

        with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            # Write header
            writer.writerow(["url", "title", "content", "category", "timestamp"])

            # Write data
            for item in data:
                writer.writerow(
                    [
                        item.url,
                        item.title,
                        (
                            item.content[:1000] if item.content else ""
                        ),  # Limit content length
                        item.category,
                        item.timestamp.isoformat() if item.timestamp else "",
                    ]
                )

        return str(filepath.absolute())


class JSONExporter(IDataExporter):
    """Exports scraped data to JSON format."""

    def export(self, data: List[ScrapedData], filename: str) -> str:
        """
        Export scraped data to JSON file.

        Args:
            data: List of scraped data
            filename: Output filename

        Returns:
            Path to exported file
        """
        if not filename.endswith(".json"):
            filename += ".json"

        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Convert data to dictionaries
        export_data = []
        for item in data:
            item_dict = {
                "url": item.url,
                "title": item.title,
                "content": item.content,
                "category": item.category,
                "timestamp": item.timestamp.isoformat() if item.timestamp else None,
                "metadata": item.metadata,
            }
            export_data.append(item_dict)

        # Add export metadata
        output = {
            "export_timestamp": datetime.now().isoformat(),
            "total_items": len(export_data),
            "data": export_data,
        }

        with open(filepath, "w", encoding="utf-8") as jsonfile:
            json.dump(output, jsonfile, indent=2, ensure_ascii=False)

        return str(filepath.absolute())


class XMLExporter(IDataExporter):
    """Exports scraped data to XML format."""

    def export(self, data: List[ScrapedData], filename: str) -> str:
        """Export data to XML file."""
        # Ensure XML extension
        if not filename.endswith(".xml"):
            filename += ".xml"

        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Create root element
        root = ET.Element("scraped_data")

        for item in data:
            item_elem = ET.SubElement(root, "item")

            # Add child elements
            ET.SubElement(item_elem, "url").text = item.url
            ET.SubElement(item_elem, "title").text = item.title or ""

            # Truncate content for XML
            content_text = item.content or ""
            if len(content_text) > 2000:
                content_text = content_text[:2000] + "..."
            ET.SubElement(item_elem, "content").text = content_text

            ET.SubElement(item_elem, "category").text = item.category
            ET.SubElement(item_elem, "timestamp").text = (
                item.timestamp.isoformat() if item.timestamp else ""
            )

            # Add metadata
            if item.metadata:
                metadata_elem = ET.SubElement(item_elem, "metadata")
                for key, value in item.metadata.items():
                    ET.SubElement(metadata_elem, key).text = str(value)

        # Write to file
        tree = ET.ElementTree(root)
        # Pretty print (Python 3.9+), fallback for older versions
        if hasattr(ET, "indent"):
            ET.indent(tree, space="  ", level=0)
        tree.write(filepath, encoding="utf-8", xml_declaration=True)

        return str(filepath)


class DataExporterFactory:
    """Factory for creating appropriate data exporters."""

    _exporters: Dict[str, Callable[[], IDataExporter]] = {
        "csv": CSVExporter,
        "json": JSONExporter,
        "xml": XMLExporter,
    }

    @classmethod
    def create_exporter(cls, format_type: str) -> IDataExporter:
        """
        Create an exporter for the specified format.

        Args:
            format_type: Export format ('csv', 'json', 'xml')

        Returns:
            Appropriate exporter instance

        Raises:
            ValueError: If format is not supported
        """
        format_type = format_type.lower()
        if format_type not in cls._exporters:
            supported_formats = ", ".join(cls._exporters.keys())
            raise ValueError(
                f"Unsupported format '{format_type}'. Supported formats: {supported_formats}"
            )

        return cls._exporters[format_type]()

    @classmethod
    def get_supported_formats(cls) -> List[str]:
        """
        Get list of supported export formats.

        Returns:
            List of supported format strings
        """
        return list(cls._exporters.keys())
