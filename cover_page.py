import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import time

class CoverPageGenerator:
    @staticmethod
    def insert_cover_page(doc, title: str = "Document Title", author: str = "docForge Publication Engine", preset_id: str = "classic_book"):
        first_p = doc.paragraphs[0] if doc.paragraphs else doc.add_paragraph()
        
        # Clean title string
        formatted_title = title.replace('_', ' ').replace('-', ' ').title()

        if preset_id == "modern_corporate":
            # Corporate Header Banner Line
            p_top = first_p.insert_paragraph_before()
            p_top.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p_top.paragraph_format.space_before = Pt(36)
            p_top.paragraph_format.space_after = Pt(48)
            r_top = p_top.add_run("EXECUTIVE REPORT  |  CONFIDENTIAL")
            r_top.font.name = 'Arial'
            r_top.font.size = Pt(10)
            r_top.font.bold = True
            r_top.font.color.rgb = RGBColor(37, 99, 235)

            # Main Title
            p_title = first_p.insert_paragraph_before()
            p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p_title.paragraph_format.space_after = Pt(12)
            run_title = p_title.add_run(formatted_title)
            run_title.font.name = 'Arial'
            run_title.font.size = Pt(32)
            run_title.font.bold = True
            run_title.font.color.rgb = RGBColor(15, 23, 42)

            # Horizontal Accent Divider Rule
            p_rule = first_p.insert_paragraph_before()
            p_rule.paragraph_format.space_after = Pt(24)
            pBdr = parse_xml(r'<w:pBdr %s><w:bottom w:val="single" w:sz="18" w:space="1" w:color="2563EB"/></w:pBdr>' % nsdecls('w'))
            p_rule._p.get_or_add_pPr().append(pBdr)

            # Subtitle Badge
            p_sub = first_p.insert_paragraph_before()
            p_sub.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p_sub.paragraph_format.space_after = Pt(120)
            run_sub = p_sub.add_run("OFFICIAL BUSINESS PUBLICATION")
            run_sub.font.name = 'Arial'
            run_sub.font.size = Pt(11)
            run_sub.font.bold = True
            run_sub.font.color.rgb = RGBColor(100, 116, 139)

            # Metadata Footer
            p_meta = first_p.insert_paragraph_before()
            p_meta.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p_meta.paragraph_format.space_after = Pt(4)
            r_auth = p_meta.add_run(f"Author: {author}\nDate: {time.strftime('%B %d, %Y')}\nStatus: Verified Final Output")
            r_auth.font.name = 'Arial'
            r_auth.font.size = Pt(10.5)
            r_auth.font.color.rgb = RGBColor(71, 85, 105)

        elif preset_id == "ieee_paper" or preset_id == "apa_7th":
            # Academic Title Block
            p_title = first_p.insert_paragraph_before()
            p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_title.paragraph_format.space_before = Pt(72)
            p_title.paragraph_format.space_after = Pt(14)
            run_title = p_title.add_run(formatted_title)
            run_title.font.name = 'Times New Roman'
            run_title.font.size = Pt(24)
            run_title.font.bold = True
            run_title.font.color.rgb = RGBColor(15, 23, 42)

            # Subtitle
            p_sub = first_p.insert_paragraph_before()
            p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_sub.paragraph_format.space_after = Pt(60)
            run_sub = p_sub.add_run("IEEE Academic Research Publication Manuscript")
            run_sub.font.name = 'Times New Roman'
            run_sub.font.size = Pt(12)
            run_sub.font.italic = True
            run_sub.font.color.rgb = RGBColor(100, 116, 139)

            # Author Affiliations Box
            p_auth = first_p.insert_paragraph_before()
            p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_auth.paragraph_format.space_after = Pt(6)
            r_auth = p_auth.add_run(f"{author}\nDepartment of Computer Science & Engineering\n{time.strftime('%B %Y')}")
            r_auth.font.name = 'Times New Roman'
            r_auth.font.size = Pt(11)
            r_auth.font.color.rgb = RGBColor(51, 65, 85)

        else:
            # Classic Book / Novel Cover
            p_title = first_p.insert_paragraph_before()
            p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_title.paragraph_format.space_before = Pt(90)
            p_title.paragraph_format.space_after = Pt(18)
            run_title = p_title.add_run(formatted_title.upper())
            run_title.font.name = 'Georgia'
            run_title.font.size = Pt(30)
            run_title.font.bold = True
            run_title.font.color.rgb = RGBColor(15, 23, 42)

            # Decorative Rule
            p_rule = first_p.insert_paragraph_before()
            p_rule.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_rule.paragraph_format.space_after = Pt(24)
            r_star = p_rule.add_run("♦   ♦   ♦")
            r_star.font.name = 'Georgia'
            r_star.font.size = Pt(14)
            r_star.font.color.rgb = RGBColor(148, 163, 184)

            # Subtitle
            p_sub = first_p.insert_paragraph_before()
            p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_sub.paragraph_format.space_after = Pt(90)
            run_sub = p_sub.add_run("A NOVEL & PUBLICATION MANUSCRIPT")
            run_sub.font.name = 'Georgia'
            run_sub.font.size = Pt(11)
            run_sub.font.bold = True
            run_sub.font.color.rgb = RGBColor(100, 116, 139)

            # Author
            p_auth = first_p.insert_paragraph_before()
            p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_auth.paragraph_format.space_after = Pt(12)
            r_auth = p_auth.add_run(author)
            r_auth.font.name = 'Georgia'
            r_auth.font.size = Pt(14)
            r_auth.font.bold = True
            r_auth.font.color.rgb = RGBColor(15, 23, 42)

        # Page Break after cover page
        p_break = first_p.insert_paragraph_before()
        p_break.paragraph_format.space_before = Pt(0)
        p_break.paragraph_format.space_after = Pt(0)
        p_break.add_run().add_break(docx.enum.text.WD_BREAK.PAGE)
