import docx
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
from docx.shared import Pt, RGBColor

class WatermarkGenerator:
    @staticmethod
    def apply_watermark(doc, watermark_text: str = "CONFIDENTIAL"):
        if not watermark_text or not watermark_text.strip():
            return

        wm_str = watermark_text.strip().upper()

        for section in doc.sections:
            header = section.header
            # Create dedicated background paragraph for VML Watermark object
            p_wm = header.add_paragraph()
            p_wm.paragraph_format.space_before = Pt(0)
            p_wm.paragraph_format.space_after = Pt(0)
            
            # Official MS Word OpenXML VML Watermark Shape with full shapetype & 315-degree diagonal rotation
            vml_xml = f"""
            <w:r xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
                <w:pict>
                    <v:shapetype id="_x0000_t136" coordsize="21600,21600" o:spt="136" path="m@7,l@8,m@5,l@6,e">
                        <v:formulas>
                            <v:f eqn="sum #0 0 10800"/>
                            <v:f eqn="prod #0 2 1"/>
                            <v:f eqn="sum 21600 0 @1"/>
                            <v:f eqn="sum 0 0 @2"/>
                            <v:f eqn="sum 21600 0 @3"/>
                            <v:f eqn="sum #1 0 10800"/>
                            <v:f eqn="prod #1 2 1"/>
                            <v:f eqn="sum 21600 0 @6"/>
                            <v:f eqn="sum 0 0 @7"/>
                            <v:f eqn="sum 21600 0 @8"/>
                        </v:formulas>
                        <v:path textpathok="t" o:connecttype="custom" o:connectlocs="@9,0;@10,10800;@11,21600;@12,10800" o:connectangles="270,180,90,0"/>
                        <v:textpath on="t" fitshape="t"/>
                        <v:handles>
                            <v:h position="#0,bottomRight" xrange="6000,21600"/>
                        </v:handles>
                    </v:shapetype>
                    <v:shape id="PowerPlusWaterMarkObject" type="#_x0000_t136" 
                        style="position:absolute;margin-left:0;margin-top:0;width:450pt;height:180pt;rotation:315;z-index:-251657728;mso-position-horizontal:center;mso-position-horizontal-relative:margin;mso-position-vertical:center;mso-position-vertical-relative:margin" 
                        fillcolor="#94a3b8" stroked="f">
                        <v:fill opacity="0.45"/>
                        <v:textpath style="font-family:&quot;Arial&quot;;font-size:1pt;font-weight:bold" string="{wm_str}"/>
                    </v:shape>
                </w:pict>
            </w:r>
            """

            try:
                r_elem = parse_xml(vml_xml)
                p_wm._p.append(r_elem)
            except Exception as e:
                p_wm.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
                run = p_wm.add_run(f"[{wm_str}]")
                run.font.size = Pt(36)
                run.font.bold = True
                run.font.color.rgb = RGBColor(148, 163, 184)
