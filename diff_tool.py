import html
from typing import List, Dict, Any

class DocumentDiffTool:
    @staticmethod
    def generate_html_diff(original_elements: List[Dict[str, Any]], formatted_elements: List[Dict[str, Any]], output_html_path: str):
        rows_html = []
        max_len = max(len(original_elements), len(formatted_elements))

        for idx in range(max_len):
            orig_item = original_elements[idx] if idx < len(original_elements) else None
            fmt_item = formatted_elements[idx] if idx < len(formatted_elements) else None

            orig_text = html.escape(orig_item['text']) if orig_item else "<em>[None]</em>"
            fmt_text = html.escape(fmt_item['text']) if fmt_item else "<em>[None]</em>"
            fmt_cls = fmt_item['classification'] if fmt_item else "--"

            changed_badge = '<span style="color:#10B981;">[Formatted]</span>' if fmt_item else ''

            rows_html.append(f"""
            <tr>
                <td style="width: 5%; text-align: center; color: #94A3B8;">#{idx+1}</td>
                <td style="width: 45%; vertical-align: top; background: #1E293B;">{orig_text}</td>
                <td style="width: 50%; vertical-align: top; background: #0F172A;">
                    <div style="font-size: 0.8em; color: #60A5FA; margin-bottom: 4px;"><strong>{fmt_cls}</strong> {changed_badge}</div>
                    {fmt_text}
                </td>
            </tr>
            """)

        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Side-by-Side Document Diff Comparison</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0B0F19; color: #F8FAFC; margin: 0; padding: 25px; }}
        h1 {{ color: #3B82F6; border-bottom: 2px solid #334155; padding-bottom: 10px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 14px; line-height: 1.5; }}
        th, td {{ padding: 12px; border: 1px solid #334155; text-align: left; }}
        th {{ background: #1E293B; color: #94A3B8; font-size: 13px; text-transform: uppercase; }}
    </style>
</head>
<body>
    <h1>⚖️ Side-by-Side Document Comparison & Diff</h1>
    <p style="color: #94A3B8;">Comparing Original Manuscript vs Formatted Publication Output</p>
    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>Original Manuscript Text</th>
                <th>Formatted Output & Classification</th>
            </tr>
        </thead>
        <tbody>
            {''.join(rows_html)}
        </tbody>
    </table>
</body>
</html>"""

        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(full_html)
