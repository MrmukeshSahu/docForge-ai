import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import time

class CoverPageGenerator:
    @staticmethod
    def insert_cover_page(doc, title: str = "Document Title", author: str = "Author Name", preset_id: str = "classic_book"):
        first_p = doc.paragraphs[0] if doc.paragraphs else doc.add_paragraph()
        
        # We insert cover elements before the first paragraph
        p_title = first_p.insert_paragraph_before()
        p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_title.paragraph_format.space_before = Pt(72)
        p_title.paragraph_format.space_after = Pt(18)
        run_title = p_title.add_run(title.upper())
        run_title.font.name = 'Times New Roman' if preset_id != 'modern_corporate' else 'Arial'
        run_title.font.size = Pt(28)
        run_title.font.bold = True
        if preset_id == "modern_corporate":
            run_title.font.color.rgb = RGBColor(37, 99, 235)
        else:
            run_title.font.color.rgb = RGBColor(15, 23, 42)

        # Subtitle / Type
        p_sub = first_p.insert_paragraph_before()
        p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_sub.paragraph_format.space_after = Pt(120)
        run_sub = p_sub.add_run("OFFICIAL PUBLICATION MANUSCRIPT")
        run_sub.font.size = Pt(11)
        run_sub.font.bold = True
        run_sub.font.color.rgb = RGBColor(100, 116, 139)

        # Author & Date
        p_author = first_p.insert_paragraph_before()
        p_author.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_author.paragraph_format.space_after = Pt(6)
        run_auth = p_author.add_run(f"Prepared by: {author}")
        run_auth.font.size = Pt(14)
        run_auth.font.bold = True

        p_date = first_p.insert_paragraph_before()
        p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_date.paragraph_format.space_after = Pt(24)
        run_date = p_date.add_run(time.strftime("%B %Y"))
        run_date.font.size = Pt(11)
        run_date.font.italic = True
        run_date.font.color.rgb = RGBColor(100, 116, 139)

        # Page Break after cover page
        p_break = first_p.insert_paragraph_before()
        p_break.add_run().add_break(docx.enum.text.WD_BREAK.PAGE)
