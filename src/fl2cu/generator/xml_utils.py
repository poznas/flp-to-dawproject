from xml.etree import ElementTree as ET
from typing import Optional
import logging
from pathlib import Path

class XMLWriter:
    """Handles XML file writing with proper formatting."""
    
    @staticmethod
    def format_xml(elem: ET.Element, level: int = 0, indent: str = "  ") -> None:
        """Format XML element with proper indentation."""
        i = "\n" + level * indent
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + indent
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for subelem in elem:
                XMLWriter.format_xml(subelem, level + 1, indent)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    @staticmethod
    def write_xml(
        root: ET.Element,
        output_path: Path,
        encoding: str = 'UTF-8',
        xml_declaration: bool = True
    ) -> bool:
        """Write formatted XML to file."""
        logger = logging.getLogger(__name__)
        try:
            # Format the XML
            XMLWriter.format_xml(root)
            
            # Convert to string
            xml_str = ET.tostring(root, encoding='unicode')
            
            # Write to file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding=encoding) as f:
                if xml_declaration:
                    f.write(f'<?xml version="1.0" encoding="{encoding}"?>\n')
                f.write(xml_str)
                
            logger.debug(f"Successfully wrote XML to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to write XML to {output_path}: {e}")
            return False