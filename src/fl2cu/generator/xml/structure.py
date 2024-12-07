# src/fl2cu/generator/xml/structure.py
from xml.etree import ElementTree as ET
from ...models.project import Project
from ...models.timing import ProjectTiming

class BaseStructureGenerator:
    """Handles creation of basic DAWproject XML structure."""
    
    def create_root(self) -> ET.Element:
        return ET.Element("Project", version="1.0")
        
    def create_application_info(self) -> ET.Element:
        return ET.Element("Application", 
            name="Cubase",
            version="14.0.5"
        )
        
    def create_transport(self, timing: ProjectTiming) -> ET.Element:
        """Create Transport element from timing model."""
        transport = ET.Element("Transport")
        
        ET.SubElement(transport, "Tempo",
            unit="bpm",
            value=str(int(timing.tempo))
        )
        
        ET.SubElement(transport, "TimeSignature",
            numerator=str(timing.time_signature_numerator),
            denominator=str(timing.time_signature_denominator)
        )
        
        return transport