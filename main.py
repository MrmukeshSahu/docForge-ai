import argparse
import sys
import time
import os
import docx
from cleaner import DocumentCleaner
from document_parser import DocumentParser
from classifier import ParagraphClassifier
from formatter import DocumentFormatter
from presets import PresetManager
from analytics import DocumentAnalytics
from exporter import DocumentExporter
from history import HistoryManager

def process_single_file(input_path: str, output_path: str, preset_id: str = "classic_book", export_format: str = "docx", title_case: bool = False, bullet_clean: bool = False, trailing_clean: bool = False, inspect: bool = False, cover: bool = False, zip_bundle: bool = False, generate_diff: bool = False):
    print(f"[*] Processing document: {os.path.basename(input_path)}")
    start_time = time.time()
    
    # Load Document
    doc = docx.Document(input_path)
    
    # 0. Cover Page Generation if requested
    if cover:
        from cover_page import CoverPageGenerator
        print("[*] Inserting Cover & Title Page...")
        title_str = os.path.splitext(os.path.basename(input_path))[0]
        CoverPageGenerator.insert_cover_page(doc, title=title_str, preset_id=preset_id)

    # 1. Clean Document
    print("[*] Cleaning typography and formatting...")
    cleaner = DocumentCleaner(doc, title_case_headings=title_case, bullet_standardization=bullet_clean, trailing_whitespace=trailing_clean)
    spacing_errors = cleaner.clean()
    print(f"[*] Fixed {spacing_errors} redundancy/typography issues.")
    
    # 2. Parse Document
    print("[*] Parsing document structure...")
    doc_parser = DocumentParser(doc)
    elements = list(doc_parser.extract_elements())
    tables = doc_parser.extract_tables()
    images_count = doc_parser.count_images()
    print(f"[*] Extracted {len(elements)} paragraphs/elements.")
    
    # 3. Classify Elements
    print("[*] Classifying document elements...")
    classifier = ParagraphClassifier()
    classified_elements = []
    tally = {}
    flagged_count = 0
    
    for element in elements:
        cls_str, conf, review_needed, explanation = classifier.classify_with_explanation(element)
        element['classification'] = cls_str
        element['confidence'] = conf
        element['review_needed'] = review_needed
        element['explanation'] = explanation
        
        if review_needed:
            flagged_count += 1
            
        classified_elements.append(element)
        tally[cls_str] = tally.get(cls_str, 0) + 1
        
    print("[*] Classification complete. Element Tally:")
    for k, v in tally.items():
        print(f"    - {k}: {v}")
        
    if inspect:
        print("\n--- Paragraph Inspection ---")
        for idx, el in enumerate(classified_elements[:15]):
            print(f"[{idx+1:02d}] Class: {el['classification']:<18} Conf: {el['confidence']*100:.0f}% | Text: {el['text'][:50]}...")
        print("-----------------------------\n")

    # Grammar & Consistency Audit
    from consistency_checker import GrammarConsistencyChecker
    consistency_data = GrammarConsistencyChecker.analyze_consistency(classified_elements)
    print(f"[*] Dialect Dominance: {consistency_data['dominant_dialect']} (US: {consistency_data['us_spelling_count']} | UK: {consistency_data['uk_spelling_count']})")
    if consistency_data['repeat_word_glitches']:
        print(f"[!] Found {len(consistency_data['repeat_word_glitches'])} duplicate word glitches.")
        
    # 4. Format and Output
    print(f"[*] Applying Preset: '{preset_id}'...")
    pm = PresetManager()
    preset = pm.get_preset(preset_id)
    
    formatter = DocumentFormatter(doc, preset=preset)
    formatter.format_elements(classified_elements)
    formatter.save(output_path)
    
    # 5. Multi-format Exporter
    exporter = DocumentExporter(classified_elements, title=os.path.splitext(os.path.basename(input_path))[0])
    base_out, _ = os.path.splitext(output_path)
    
    analytics_data = DocumentAnalytics.analyze(doc, classified_elements, tables_count=len(tables), images_count=images_count)
    analytics_data["consistency"] = consistency_data

    if export_format in ["md", "all"]:
        exporter.export_markdown(base_out + ".md")
        print(f"[*] Exported Markdown: {base_out}.md")
    if export_format in ["txt", "all"]:
        exporter.export_txt(base_out + ".txt")
        print(f"[*] Exported Text: {base_out}.txt")
    if export_format in ["html", "all"]:
        exporter.export_html(base_out + ".html")
        print(f"[*] Exported HTML: {base_out}.html")
    if export_format in ["epub", "all"]:
        exporter.export_epub(base_out + ".epub")
        print(f"[*] Exported EPUB eBook: {base_out}.epub")
    if export_format in ["audit", "all"]:
        exporter.export_audit_report(base_out + "_audit.html", analytics_data)
        print(f"[*] Exported HTML Audit Report: {base_out}_audit.html")
    if export_format in ["pdf", "all"]:
        exporter.export_pdf_fallback(output_path, base_out + ".pdf")
        print(f"[*] Exported PDF: {base_out}.pdf")

    # Side-by-Side Diff Generator
    if generate_diff:
        from diff_tool import DocumentDiffTool
        diff_path = base_out + "_diff.html"
        DocumentDiffTool.generate_html_diff(elements, classified_elements, diff_path)
        print(f"[*] Generated Side-by-Side Diff: {diff_path}")

    # Zip Package Exporter
    if zip_bundle:
        zip_path = base_out + "_bundle.zip"
        exporter.export_zip(zip_path, output_path, analytics_data)
        print(f"[*] Created 1-Click ZIP Archive: {zip_path}")
        
    elapsed = time.time() - start_time
    
    # 6. History Logging
    hm = HistoryManager()
    hm.add_entry(input_path, output_path, elapsed, len(elements), preset.name, "Success")
    
    print(f"[*] Success! Saved to {output_path}")
    print(f"[*] Summary Dashboard:")
    print(f"    Elements Processed: {len(elements)}")
    print(f"    Chapters Found: {tally.get('Heading 1', 0)}, Images: {images_count}")
    print(f"    Fixed Spacing Errors: {spacing_errors}")
    print(f"    Readability Score: {analytics_data['flesch_score']} ({analytics_data['readability_label']})")
    print(f"    Processing Time: {elapsed:.2f} seconds\n")

def main():
    parser = argparse.ArgumentParser(description="docForge-ai Pro: Intelligent Document Studio & Publication Engine")
    parser.add_argument("input", nargs="?", help="Path to input .docx file")
    parser.add_argument("output", nargs="?", help="Path to save formatted .docx file")
    parser.add_argument("--preset", default="classic_book", help="Formatting preset ID")
    parser.add_argument("--format", default="docx", choices=["docx", "pdf", "md", "txt", "html", "epub", "audit", "all"], help="Export format option")
    parser.add_argument("--batch", nargs=2, metavar=('INPUT_DIR', 'OUTPUT_DIR'), help="Process all .docx files in input directory")
    parser.add_argument("--watch", nargs=2, metavar=('WATCH_DIR', 'OUTPUT_DIR'), help="Hot-folder background watcher mode")
    parser.add_argument("--cover", action="store_true", help="Automatically generate cover page")
    parser.add_argument("--zip", action="store_true", help="Export all formats into a zip bundle")
    parser.add_argument("--diff", action="store_true", help="Generate side-by-side HTML comparison diff")
    parser.add_argument("--title_case", action="store_true", help="Auto-convert headings to title case")
    parser.add_argument("--bullet_clean", action="store_true", help="Standardize list bullet characters")
    parser.add_argument("--trailing_clean", action="store_true", help="Remove trailing whitespaces")
    parser.add_argument("--inspect", action="store_true", help="Print paragraph classification breakdown")
    
    args = parser.parse_args()

    if args.watch:
        from watcher import FolderWatcher
        w_dir, o_dir = args.watch
        def watch_callback(inp_f, out_f):
            process_single_file(inp_f, out_f, preset_id=args.preset, export_format=args.format, title_case=args.title_case, bullet_clean=args.bullet_clean, trailing_clean=args.trailing_clean, inspect=args.inspect, cover=args.cover, zip_bundle=args.zip, generate_diff=args.diff)
        watcher = FolderWatcher(w_dir, o_dir, watch_callback)
        watcher.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            watcher.stop()
            print("[*] Watcher stopped.")
        return
    
    if args.batch:
        in_dir, out_dir = args.batch
        if not os.path.exists(in_dir):
            print(f"[!] Input directory does not exist: {in_dir}")
            sys.exit(1)
        os.makedirs(out_dir, exist_ok=True)
        docx_files = [f for f in os.listdir(in_dir) if f.lower().endswith('.docx')]
        print(f"[*] Starting Batch Processing for {len(docx_files)} documents in '{in_dir}'...")
        for fname in docx_files:
            inp = os.path.join(in_dir, fname)
            out = os.path.join(out_dir, f"formatted_{fname}")
            try:
                process_single_file(inp, out, preset_id=args.preset, export_format=args.format, title_case=args.title_case, bullet_clean=args.bullet_clean, trailing_clean=args.trailing_clean, inspect=args.inspect, cover=args.cover, zip_bundle=args.zip, generate_diff=args.diff)
            except Exception as e:
                print(f"[!] Error processing {fname}: {e}")
        print("[*] Batch Processing Completed!")
        return

    if not args.input or not args.output:
        parser.print_help()
        sys.exit(1)
        
    process_single_file(args.input, args.output, preset_id=args.preset, export_format=args.format, title_case=args.title_case, bullet_clean=args.bullet_clean, trailing_clean=args.trailing_clean, inspect=args.inspect, cover=args.cover, zip_bundle=args.zip, generate_diff=args.diff)

if __name__ == "__main__":
    main()

