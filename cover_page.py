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
        formatted_title = title.replace('_', ' ').replace('-', ' ').strip()
        if not formatted_title or formatted_title.lower() in ["mock input", "input", "document", "chapter 1"]:
            formatted_title = "OFFICIAL PUBLICATION MANUSCRIPT"
        else:
            formatted_title = formatted_title.title()

        # Insert Graphic Banner Table before first_p
        tbl = doc.add_table(rows=1, cols=1)
        tbl.autofit = False
        
        # Move table before first paragraph
        first_p._p.addprevious(tbl._tbl)
        
        cell = tbl.cell(0, 0)
        cell.width = Cm(17.0)
        
        bg_color = "1E293B" if preset_id == "classic_book" else ("1D4ED8" if preset_id == "modern_corporate" else "0F172A")
        tcPr = cell._element.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>')
        tcPr.append(shd)

        # Inside Banner Cell Paragraph
        p_banner = cell.paragraphs[0]
        p_banner.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_banner.paragraph_format.space_before = Pt(16)
        p_banner.paragraph_format.space_after = Pt(16)
        
        r_banner = p_banner.add_run("❖   PUBLICATION & RESEARCH STUDIO EDITION   ❖")
        r_banner.font.name = 'Arial'
        r_banner.font.size = Pt(11)
        r_banner.font.bold = True
        r_banner.font.color.rgb = RGBColor(255, 255, 255)

        # Spacing Paragraph below banner
        p_sp1 = first_p.insert_paragraph_before()
        p_sp1.paragraph_format.space_before = Pt(40)
        p_sp1.paragraph_format.space_after = Pt(10)

        # Main Graphic Title Block
        p_title = first_p.insert_paragraph_before()
        p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_title.paragraph_format.space_after = Pt(16)
        r_title = p_title.add_run(formatted_title.upper())
        r_title.font.name = 'Georgia' if preset_id == "classic_book" else 'Arial'
        r_title.font.size = Pt(32)
        r_title.font.bold = True
        r_title.font.color.rgb = RGBColor(15, 23, 42)

        # Horizontal Accent Divider Line
        p_rule = first_p.insert_paragraph_before()
        p_rule.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_rule.paragraph_format.space_after = Pt(20)
        pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="24" w:space="1" w:color="{bg_color}"/></w:pBdr>')
        p_rule._p.get_or_add_pPr().append(pBdr)

        # Subtitle Paragraph
        p_sub = first_p.insert_paragraph_before()
        p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_sub.paragraph_format.space_after = Pt(70)
        r_sub = p_sub.add_run("ACADEMIC & PROFESSIONAL MANUSCRIPT SPECIFICATION")
        r_sub.font.name = 'Arial'
        r_sub.font.size = Pt(11)
        r_sub.font.bold = True
        r_sub.font.color.rgb = RGBColor(100, 116, 139)

        # Bottom Graphic Shaded Card for Metadata
        tbl_meta = doc.add_table(rows=1, cols=1)
        tbl_meta.autofit = False
        first_p._p.addprevious(tbl_meta._tbl)
        
        c_meta = tbl_meta.cell(0, 0)
        c_meta.width = Cm(17.0)
        tcPr_m = c_meta._element.get_or_add_tcPr()
        shd_m = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F1F5F9"/>')
        tcPr_m.append(shd_m)
        
        # Border for card
        tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="12" w:space="0" w:color="CBD5E1"/><w:left w:val="single" w:sz="24" w:space="0" w:color="{bg_color}"/><w:bottom w:val="single" w:sz="12" w:space="0" w:color="CBD5E1"/><w:right w:val="single" w:sz="12" w:space="0" w:color="CBD5E1"/></w:tcBorders>')
        tcPr_m.append(tcBorders)

        p_m = c_meta.paragraphs[0]
        p_m.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_m.paragraph_format.space_before = Pt(14)
        p_m.paragraph_format.space_after = Pt(14)
        p_m.paragraph_format.left_indent = Cm(0.5)

        r_m1 = p_m.add_run("AUTHOR / PUBLISHER: ")
        r_m1.font.name = 'Arial'
        r_m1.font.size = Pt(10.5)
        r_m1.font.bold = True
        r_m1.font.color.rgb = RGBColor(30, 41, 59)

        r_m2 = p_m.add_run(f"{author}\n")
        r_m2.font.name = 'Arial'
        r_m2.font.size = Pt(10.5)
        r_m2.font.color.rgb = RGBColor(51, 65, 85)

        r_m3 = p_m.add_run("DATE OF PUBLICATION: ")
        r_m3.font.name = 'Arial'
        r_m3.font.size = Pt(10.5)
        r_m3.font.bold = True
        r_m3.font.color.rgb = RGBColor(30, 41, 59)

        r_m4 = p_m.add_run(f"{time.strftime('%B %d, %Y')}\n")
        r_m4.font.name = 'Arial'
        r_m4.font.size = Pt(10.5)
        r_m4.font.color.rgb = RGBColor(51, 65, 85)

        r_m5 = p_m.add_run("DOCUMENT VERIFICATION: ")
        r_m5.font.name = 'Arial'
        r_m5.font.size = Pt(10.5)
        r_m5.font.bold = True
        r_m5.font.color.rgb = RGBColor(30, 41, 59)

        r_m6 = p_m.add_run("Verified Studio Master Output (100% Offline ML Formatted)")
        r_m6.font.name = 'Arial'
        r_m6.font.size = Pt(10.5)
        r_m6.font.color.rgb = RGBColor(51, 65, 85)

        # Page Break after cover page
        p_break = first_p.insert_paragraph_before()
        p_break.paragraph_format.space_before = Pt(0)
        p_break.paragraph_format.space_after = Pt(0)
        p_break.add_run().add_break(docx.enum.text.WD_BREAK.PAGE)
