from lxml import etree
from pathlib import Path
from typing import Dict
from ..models.arrangement import Arrangement
from ..models.clip import Clip

class XMLGenerator:
    def __init__(self, arrangement: Arrangement, clip_paths: Dict[Clip, Path]) -> None:
        """
        Initialize XMLGenerator with arrangement and clip paths.

        Args:
            arrangement: Arrangement object containing clips and metadata.
            clip_paths: Dictionary mapping Clip objects to their processed audio file paths.
        """
        self.arrangement = arrangement
        self.clip_paths = clip_paths

    def generate_xml(self, output_path: str) -> None:
        """
        Generate an XML representation of the arrangement.

        Args:
            output_path: Path where the XML file will be saved.
        """
        root = etree.Element("arrangement", name=self.arrangement.name)
        for clip in self.arrangement.clips:
            clip_element = etree.SubElement(root, "clip", name=clip.name)
            clip_element.set("position", str(clip.position))
            clip_element.set("duration", str(clip.duration))
            clip_element.set("color", clip.color)
            clip_element.set("volume", str(clip.volume))
            clip_element.set("muted", str(clip.muted).lower())

            if clip in self.clip_paths:
                clip_element.set("source_path", str(self.clip_paths[clip]))

        tree = etree.ElementTree(root)
        with open(output_path, "wb") as f:
            tree.write(f, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    def generate_debug_info(self, debug_dir: str) -> None:
        """
        Generate debug information related to the XML generation.

        Args:
            debug_dir: Directory where debug information will be saved.
        """
        debug_path = Path(debug_dir) / "debug_info.txt"
        with open(debug_path, "w") as f:
            f.write(f"Arrangement: {self.arrangement.name}\n")
            f.write(f"Number of Clips: {len(self.arrangement.clips)}\n")
            for clip in self.arrangement.clips:
                f.write(f"Clip: {clip.name}\n")
                f.write(f"  Position: {clip.position}\n")
                f.write(f"  Duration: {clip.duration}\n")
                f.write(f"  Color: {clip.color}\n")
                f.write(f"  Volume: {clip.volume}\n")
                f.write(f"  Muted: {clip.muted}\n")
                if clip in self.clip_paths:
                    f.write(f"  Source Path: {self.clip_paths[clip]}\n")
