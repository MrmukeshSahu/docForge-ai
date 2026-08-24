import os
import html
from typing import List, Dict, Any

class DocumentExporter:
    def __init__(self, elements_with_classes: List[Dict[str, Any]], title: str = "Formatted Document"):
        self.elements = elements_with_classes
        self.title = title

    def export_markdown(self, output_path: str):
        lines = [f"# {self.title}\n\n"]
        for item in self.elements:
            text = item['text']
            cls = item['classification']
            
            if cls == "Title":
                lines.append(f"# {text}\n\n")
            elif cls == "Author":
                lines.append(f"**By {text}**\n\n")
            elif cls in ["Heading 1", "References Heading"]:
                lines.append(f"## {text}\n\n")
            elif cls in ["Subheading", "Heading 2"]:
                lines.append(f"### {text}\n\n")
            elif cls == "Heading 3":
                lines.append(f"#### {text}\n\n")
            elif cls == "Caption":
                lines.append(f"*{text}*\n\n")
            elif cls == "List":
                lines.append(f"- {text}\n")
            elif cls == "Code Block":
                lines.append(f"```\n{text}\n```\n\n")
            elif cls == "Blockquote":
                lines.append(f"> {text}\n\n")
            else:
                lines.append(f"{text}\n\n")
                
        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    def export_txt(self, output_path: str):
        lines = []
        for item in self.elements:
            lines.append(item['text'] + "\n\n")
        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    def export_html(self, output_path: str):
        body_html = []
        for item in self.elements:
            t = html.escape(item['text'])
            cls = item['classification']
            
            if cls == "Title":
                body_html.append(f'<h1 class="doc-title">{t}</h1>')
            elif cls == "Author":
                body_html.append(f'<p class="doc-author">By {t}</p>')
            elif cls in ["Heading 1", "References Heading"]:
                body_html.append(f'<h2>{t}</h2>')
            elif cls in ["Subheading", "Heading 2"]:
                body_html.append(f'<h3>{t}</h3>')
            elif cls == "Heading 3":
                body_html.append(f'<h4>{t}</h4>')
            elif cls == "Caption":
                body_html.append(f'<p class="caption"><em>{t}</em></p>')
            elif cls == "List":
                body_html.append(f'<li>{t}</li>')
            elif cls == "Code Block":
                body_html.append(f'<pre><code>{t}</code></pre>')
            elif cls == "Blockquote":
                body_html.append(f'<blockquote>{t}</blockquote>')
            else:
                body_html.append(f'<p>{t}</p>')
                
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{html.escape(self.title)}</title>
    <style>
        body {{
            font-family: 'Times New Roman', Times, serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            line-height: 1.6;
            color: #1a1a1a;
            background-color: #fdfdfd;
        }}
        h1.doc-title {{ text-align: center; color: #0f172a; margin-bottom: 5px; }}
        p.doc-author {{ text-align: center; font-weight: bold; color: #475569; margin-bottom: 30px; }}
        h2 {{ border-bottom: 1px solid #e2e8f0; padding-bottom: 5px; margin-top: 30px; }}
        blockquote {{ border-left: 4px solid #3b82f6; padding-left: 15px; color: #475569; font-style: italic; }}
        pre {{ background: #0f172a; color: #f8fafc; padding: 15px; border-radius: 8px; overflow-x: auto; }}
        p.caption {{ text-align: center; color: #64748b; font-size: 0.9em; }}
    </style>
</head>
<body>
    {''.join(body_html)}
</body>
</html>"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_html)

    def export_epub(self, output_path: str):
        """
        Creates a 100% valid, standalone EPUB eBook archive without external dependencies.
        """
        import zipfile
        
        body_html_items = []
        for item in self.elements:
            t = html.escape(item['text'])
            cls = item['classification']
            if cls == "Title":
                body_html_items.append(f'<h1 class="title">{t}</h1>')
            elif cls == "Author":
                body_html_items.append(f'<p class="author">By {t}</p>')
            elif cls in ["Heading 1", "References Heading"]:
                body_html_items.append(f'<h2>{t}</h2>')
            elif cls in ["Subheading", "Heading 2"]:
                body_html_items.append(f'<h3>{t}</h3>')
            elif cls == "Caption":
                body_html_items.append(f'<p class="caption"><em>{t}</em></p>')
            elif cls == "List":
                body_html_items.append(f'<li>{t}</li>')
            else:
                body_html_items.append(f'<p>{t}</p>')

        ch1_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>{html.escape(self.title)}</title>
  <style type="text/css">
    body {{ font-family: Georgia, serif; line-height: 1.5; padding: 5%; }}
    h1.title {{ text-align: center; color: #111827; }}
    p.author {{ text-align: center; font-weight: bold; color: #4B5563; }}
    h2 {{ color: #1F2937; border-bottom: 1px solid #E5E7EB; }}
    p {{ text-indent: 1em; margin-bottom: 0.5em; }}
    p.caption {{ text-align: center; font-size: 0.9em; color: #6B7280; }}
  </style>
</head>
<body>
  {''.join(body_html_items)}
</body>
</html>"""

        container_xml = """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
   <rootfiles>
      <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
   </rootfiles>
</container>"""

        content_opf = f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookID" version="2.0">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:title>{html.escape(self.title)}</dc:title>
        <dc:language>en</dc:language>
        <dc:identifier id="BookID">urn:uuid:docforge-ai-{hash(self.title)}</dc:identifier>
    </metadata>
    <manifest>
        <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
        <item id="chapter1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>
    </manifest>
    <spine toc="ncx">
        <itemref idref="chapter1"/>
    </spine>
</package>"""

        toc_ncx = f"""<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
    <head>
        <meta name="dtb:uid" content="urn:uuid:docforge-ai-{hash(self.title)}"/>
    </head>
    <docTitle><text>{html.escape(self.title)}</text></docTitle>
    <navMap>
        <navPoint id="navpoint-1" playOrder="1">
            <navLabel><text>Start Reading</text></navLabel>
            <content src="chapter1.xhtml"/>
        </navPoint>
    </navMap>
</ncx>"""

        with zipfile.ZipFile(output_path, 'w') as zf:
            zf.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
            zf.writestr("META-INF/container.xml", container_xml, compress_type=zipfile.ZIP_DEFLATED)
            zf.writestr("OEBPS/content.opf", content_opf, compress_type=zipfile.ZIP_DEFLATED)
            zf.writestr("OEBPS/toc.ncx", toc_ncx, compress_type=zipfile.ZIP_DEFLATED)
            zf.writestr("OEBPS/chapter1.xhtml", ch1_xhtml, compress_type=zipfile.ZIP_DEFLATED)

    def export_audit_report(self, output_path: str, analytics_data: Dict[str, Any]):
        """
        Generates an interactive HTML Audit & Readability Report detailing document structure, overused words, and low confidence items.
        """
        overused_items = analytics_data.get("overused_words", [])
        overused_html = "".join([f"<tr><td><code>{html.escape(w)}</code></td><td>{cnt} times</td></tr>" for w, cnt in overused_items])

        tally_items = analytics_data.get("classification_tally", {})
        tally_html = "".join([f"<tr><td>{html.escape(k)}</td><td>{v}</td></tr>" for k, v in tally_items.items()])

        flagged_rows = []
        for idx, item in enumerate(self.elements):
            if item.get('review_needed', False):
                flagged_rows.append(f"<tr><td>#{idx+1}</td><td>{html.escape(item['classification'])}</td><td>{item['confidence']*100:.0f}%</td><td>{html.escape(item['text'][:80])}...</td></tr>")

        flagged_html = "".join(flagged_rows) if flagged_rows else "<tr><td colspan='4' style='color:#10B981;'>No items flagged for manual review! Perfect classification confidence.</td></tr>"

        report_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Audit & Readability Report - {html.escape(self.title)}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 30px; }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        h1 {{ color: #3b82f6; border-bottom: 2px solid #334155; padding-bottom: 10px; }}
        .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0; }}
        .card {{ background: #1e293b; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #334155; }}
        .card .val {{ font-size: 24px; font-weight: bold; color: #10b981; margin-top: 5px; }}
        .section {{ background: #1e293b; padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #334155; }}
        h2 {{ color: #60a5fa; margin-top: 0; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #334155; }}
        th {{ background: #0f172a; color: #94a3b8; }}
        code {{ background: #334155; padding: 2px 6px; border-radius: 4px; color: #f43f5e; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Audit & Readability Report: {html.escape(self.title)}</h1>
        <div class="grid">
            <div class="card"><div>Readability Score</div><div class="val">{analytics_data.get('flesch_score', '--')}</div></div>
            <div class="card"><div>Grade Level</div><div class="val">{analytics_data.get('fk_grade', '--')}</div></div>
            <div class="card"><div>Total Words</div><div class="val">{analytics_data.get('total_words', 0)}</div></div>
            <div class="card"><div>Reading Time</div><div class="val">{analytics_data.get('reading_time_mins', 0)} min</div></div>
        </div>

        <div class="section">
            <h2>⚠️ Overused & High-Frequency Words Alert</h2>
            <table>
                <thead><tr><th>Word</th><th>Frequency Count</th></tr></thead>
                <tbody>{overused_html}</tbody>
            </table>
        </div>

        <div class="section">
            <h2>📑 Document Element Breakdown</h2>
            <table>
                <thead><tr><th>Element Component</th><th>Count</th></tr></thead>
                <tbody>{tally_html}</tbody>
            </table>
        </div>

        <div class="section">
            <h2>🔍 Low Confidence Review Audit List</h2>
            <table>
                <thead><tr><th>#</th><th>Classification</th><th>Confidence</th><th>Snippet</th></tr></thead>
                <tbody>{flagged_html}</tbody>
            </table>
        </div>
    </div>
</body>
</html>"""

    def export_zip(self, zip_output_path: str, docx_path: str, analytics_data: Dict[str, Any]):
        """
        Archives all generated format outputs into a single .zip bundle file.
        """
        import zipfile
        base_out, _ = os.path.splitext(docx_path)
        
        md_path = base_out + ".md"
        txt_path = base_out + ".txt"
        html_path = base_out + ".html"
        epub_path = base_out + ".epub"
        audit_path = base_out + "_audit.html"
        pdf_path = base_out + ".pdf"
        
        # Ensure individual formats exist
        self.export_markdown(md_path)
        self.export_txt(txt_path)
        self.export_html(html_path)
        self.export_epub(epub_path)
        self.export_audit_report(audit_path, analytics_data)
        self.export_pdf_fallback(docx_path, pdf_path)
        
        with zipfile.ZipFile(zip_output_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            if os.path.exists(docx_path): zf.write(docx_path, os.path.basename(docx_path))
            if os.path.exists(md_path): zf.write(md_path, os.path.basename(md_path))
            if os.path.exists(txt_path): zf.write(txt_path, os.path.basename(txt_path))
            if os.path.exists(html_path): zf.write(html_path, os.path.basename(html_path))
            if os.path.exists(epub_path): zf.write(epub_path, os.path.basename(epub_path))
            if os.path.exists(audit_path): zf.write(audit_path, os.path.basename(audit_path))
            if os.path.exists(pdf_path): zf.write(pdf_path, os.path.basename(pdf_path))

    def export_pdf_fallback(self, docx_path: str, pdf_path: str):
        try:
            from docx2pdf import convert
            convert(docx_path, pdf_path)
            return True
        except Exception:
            pass
            
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            
            doc = SimpleDocTemplate(pdf_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            for item in self.elements:
                text = html.escape(item['text'])
                cls = item['classification']
                if cls == "Title":
                    story.append(Paragraph(text, styles['Title']))
                elif cls in ["Heading 1", "References Heading"]:
                    story.append(Paragraph(text, styles['Heading1']))
                elif cls in ["Subheading", "Heading 2"]:
                    story.append(Paragraph(text, styles['Heading2']))
                else:
                    story.append(Paragraph(text, styles['BodyText']))
                story.append(Spacer(1, 6))
                
            doc.build(story)
            return True
        except Exception as e:
            print(f"[!] PDF export error: {e}")
            return False

