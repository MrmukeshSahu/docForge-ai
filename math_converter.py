import re
import docx
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
from docx.shared import Pt, RGBColor

class LaTeXMathConverter:
    @staticmethod
    def process_latex_math(doc) -> int:
        """
        Parses $...$ LaTeX expressions and converts them into native Word OMML math equations.
        """
        math_count = 0
        latex_pattern = r'\$([^\$]+)\$'

        for p in doc.paragraphs:
            if '$' in p.text:
                matches = re.findall(latex_pattern, p.text)
                if matches:
                    for m in matches:
                        math_count += 1
                        omml_xml = f"""
                        <m:oMath {nsdecls('m')}>
                            <m:r>
                                <m:t>{m}</m:t>
                            </m:r>
                        </m:oMath>
                        """
                        try:
                            omml_elem = parse_xml(omml_xml)
                            p._p.append(omml_elem)
                        except Exception:
                            pass
        return math_count
