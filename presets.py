import json
import os
from typing import Dict, Any

class StylePreset:
    def __init__(
        self,
        name: str,
        description: str,
        font_family: str = "Times New Roman",
        title_size: int = 24,
        heading1_size: int = 16,
        heading2_size: int = 14,
        heading3_size: int = 12,
        body_size: int = 12,
        caption_size: int = 10,
        line_spacing: float = 1.5,
        first_line_indent_cm: float = 1.27,
        top_margin_cm: float = 1.52,
        bottom_margin_cm: float = 1.52,
        left_margin_cm: float = 1.97,
        right_margin_cm: float = 1.96,
        primary_color_rgb: tuple = (0, 0, 0),
        heading_color_rgb: tuple = (0, 0, 0),
        table_style: str = "Grid Table 4 Accent 1",
        add_toc: bool = True,
        add_page_numbers: bool = True,
        add_chapter_header: bool = True,
        body_alignment: str = "JUSTIFY",
        two_column_layout: bool = False,
        insert_cover_page: bool = False
    ):
        self.name = name
        self.description = description
        self.font_family = font_family
        self.title_size = title_size
        self.heading1_size = heading1_size
        self.heading2_size = heading2_size
        self.heading3_size = heading3_size
        self.body_size = body_size
        self.caption_size = caption_size
        self.line_spacing = line_spacing
        self.first_line_indent_cm = first_line_indent_cm
        self.top_margin_cm = top_margin_cm
        self.bottom_margin_cm = bottom_margin_cm
        self.left_margin_cm = left_margin_cm
        self.right_margin_cm = right_margin_cm
        self.primary_color_rgb = primary_color_rgb
        self.heading_color_rgb = heading_color_rgb
        self.table_style = table_style
        self.add_toc = add_toc
        self.add_page_numbers = add_page_numbers
        self.add_chapter_header = add_chapter_header
        self.body_alignment = body_alignment
        self.two_column_layout = two_column_layout
        self.insert_cover_page = insert_cover_page


    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "font_family": self.font_family,
            "title_size": self.title_size,
            "heading1_size": self.heading1_size,
            "heading2_size": self.heading2_size,
            "heading3_size": self.heading3_size,
            "body_size": self.body_size,
            "caption_size": self.caption_size,
            "line_spacing": self.line_spacing,
            "first_line_indent_cm": self.first_line_indent_cm,
            "top_margin_cm": self.top_margin_cm,
            "bottom_margin_cm": self.bottom_margin_cm,
            "left_margin_cm": self.left_margin_cm,
            "right_margin_cm": self.right_margin_cm,
            "primary_color_rgb": list(self.primary_color_rgb),
            "heading_color_rgb": list(self.heading_color_rgb),
            "table_style": self.table_style,
            "add_toc": self.add_toc,
            "add_page_numbers": self.add_page_numbers,
            "add_chapter_header": self.add_chapter_header,
            "body_alignment": self.body_alignment
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StylePreset':
        data_copy = data.copy()
        if "primary_color_rgb" in data_copy and isinstance(data_copy["primary_color_rgb"], list):
            data_copy["primary_color_rgb"] = tuple(data_copy["primary_color_rgb"])
        if "heading_color_rgb" in data_copy and isinstance(data_copy["heading_color_rgb"], list):
            data_copy["heading_color_rgb"] = tuple(data_copy["heading_color_rgb"])
        return cls(**data_copy)

# Built-in Presets Definition
BUILTIN_PRESETS = {
    "classic_book": StylePreset(
        name="Classic Publication Book",
        description="Traditional book layout with Times New Roman, indented body paragraphs, and header chapter titles.",
        font_family="Times New Roman",
        title_size=24,
        heading1_size=16,
        heading2_size=14,
        heading3_size=12,
        body_size=12,
        caption_size=10,
        line_spacing=1.5,
        first_line_indent_cm=1.27,
        top_margin_cm=1.52,
        bottom_margin_cm=1.52,
        left_margin_cm=1.97,
        right_margin_cm=1.96,
        primary_color_rgb=(0, 0, 0),
        heading_color_rgb=(0, 0, 0),
        table_style="Grid Table 4 Accent 1",
        add_toc=True,
        add_page_numbers=True,
        add_chapter_header=True,
        body_alignment="JUSTIFY"
    ),
    "academic_ieee": StylePreset(
        name="Academic / IEEE Journal",
        description="Formal academic style with compact spacing, bold headers, 2-column layout, and structured tables.",
        font_family="Times New Roman",
        title_size=22,
        heading1_size=15,
        heading2_size=13,
        heading3_size=11,
        body_size=11,
        caption_size=9,
        line_spacing=1.15,
        first_line_indent_cm=0.63,
        top_margin_cm=2.54,
        bottom_margin_cm=2.54,
        left_margin_cm=2.54,
        right_margin_cm=2.54,
        primary_color_rgb=(20, 20, 20),
        heading_color_rgb=(15, 23, 42),
        table_style="Table Grid",
        add_toc=True,
        add_page_numbers=True,
        add_chapter_header=True,
        body_alignment="JUSTIFY",
        two_column_layout=True
    ),

    "modern_corporate": StylePreset(
        name="Modern Corporate Report",
        description="Sleek business report layout with Arial font, navy headers, clean left alignment, and accent tables.",
        font_family="Arial",
        title_size=26,
        heading1_size=18,
        heading2_size=14,
        heading3_size=12,
        body_size=11,
        caption_size=10,
        line_spacing=1.3,
        first_line_indent_cm=0.0,
        top_margin_cm=2.0,
        bottom_margin_cm=2.0,
        left_margin_cm=2.5,
        right_margin_cm=2.5,
        primary_color_rgb=(30, 41, 59),
        heading_color_rgb=(37, 99, 235), # Blue
        table_style="Light Shading Accent 1",
        add_toc=True,
        add_page_numbers=True,
        add_chapter_header=False,
        body_alignment="LEFT"
    ),
    "minimalist_ebook": StylePreset(
        name="Minimalist E-Book",
        description="Clean, highly readable digital layout with Georgia serif font, generous line spacing, and soft margins.",
        font_family="Georgia",
        title_size=28,
        heading1_size=18,
        heading2_size=14,
        heading3_size=12,
        body_size=12,
        caption_size=10,
        line_spacing=1.6,
        first_line_indent_cm=1.0,
        top_margin_cm=2.2,
        bottom_margin_cm=2.2,
        left_margin_cm=2.2,
        right_margin_cm=2.2,
        primary_color_rgb=(15, 23, 42),
        heading_color_rgb=(15, 23, 42),
        table_style="Table Grid",
        add_toc=True,
        add_page_numbers=True,
        add_chapter_header=True,
        body_alignment="JUSTIFY"
    ),
    "apa_7th": StylePreset(
        name="APA 7th Edition Paper",
        description="Official APA paper standard: Times New Roman 12pt, double spacing, 1-inch margins, left-aligned body.",
        font_family="Times New Roman",
        title_size=12,
        heading1_size=12,
        heading2_size=12,
        heading3_size=12,
        body_size=12,
        caption_size=12,
        line_spacing=2.0,
        first_line_indent_cm=1.27,
        top_margin_cm=2.54,
        bottom_margin_cm=2.54,
        left_margin_cm=2.54,
        right_margin_cm=2.54,
        primary_color_rgb=(0, 0, 0),
        heading_color_rgb=(0, 0, 0),
        table_style="Table Grid",
        add_toc=False,
        add_page_numbers=True,
        add_chapter_header=False,
        body_alignment="LEFT"
    )
}

class PresetManager:
    def __init__(self, custom_presets_dir: str = None):
        if custom_presets_dir is None:
            custom_presets_dir = os.path.join(os.path.dirname(__file__), "custom_presets")
        self.custom_presets_dir = custom_presets_dir
        os.makedirs(self.custom_presets_dir, exist_ok=True)

    def get_preset(self, preset_id: str) -> StylePreset:
        if preset_id in BUILTIN_PRESETS:
            return BUILTIN_PRESETS[preset_id]
        
        # Check custom presets folder
        custom_path = os.path.join(self.custom_presets_dir, f"{preset_id}.json")
        if os.path.exists(custom_path):
            with open(custom_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return StylePreset.from_dict(data)
                
        # Default fallback
        return BUILTIN_PRESETS["classic_book"]

    def list_all_presets(self) -> Dict[str, StylePreset]:
        presets = BUILTIN_PRESETS.copy()
        if os.path.exists(self.custom_presets_dir):
            for fname in os.listdir(self.custom_presets_dir):
                if fname.endswith(".json"):
                    pid = fname[:-5]
                    try:
                        with open(os.path.join(self.custom_presets_dir, fname), "r", encoding="utf-8") as f:
                            data = json.load(f)
                            presets[pid] = StylePreset.from_dict(data)
                    except Exception:
                        pass
        return presets

    def save_custom_preset(self, preset_id: str, preset: StylePreset):
        path = os.path.join(self.custom_presets_dir, f"{preset_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(preset.to_dict(), f, indent=4)
