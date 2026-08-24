import docx
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
from docx.shared import Pt, RGBColor

class WatermarkGenerator:
    @staticmethod
    def apply_watermark(doc, watermark_text: str = "CONFIDENTIAL"):
        if not watermark_text:
            return

        for section in doc.sections:
            header = section.header
            p = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
            
            # OXML VML Watermark Shape
            vml_xml = f"""
            <w:r xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
                <w:pict>
                    <v:shape id="PowerPlusWaterMarkObject" type="#_x0000_t136" 
                        style="position:absolute;margin-left:0;margin-top:0;width:415pt;height:207.5pt;z-index:-251657728;mso-position-horizontal:center;mso-position-horizontal-relative:margin;mso-position-vertical:center;mso-position-vertical-relative:margin" 
                        fillcolor="#e2e8f0" stroked="f">
                        <v:fill opacity="0.4"/>
                        <v:textpath style="font-family:&quot;Arial&quot;;font-size:1 point;font-weight:bold" string="{watermark_text}"/>
                    </v:shape>
                </w:pict>
            </w:r>
            """

            try:
                r_elem = parse_xml(vml_xml)
                p._p.append(r_elem)
            except Exception as e:
                # Fallback paragraph background text
                p_wm = header.add_paragraph()
                p_wm.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
                run = p_wm.add_run(f"[{watermark_text.upper()}]")
                run.font.size = Pt(36)
                run.font.bold = True
                run.font.color.rgb = RGBColor(203, 213, 225)
