# docForge-ai Pro — Intelligent Document Studio & Publication Engine

A powerful, offline, AI-driven document formatting, inspection, analytics, and publication studio for `.docx` manuscripts, academic papers, books, and corporate reports.

---

## 🌟 Key Features

### 1. 📌 Single Document Quick Formatter
- 1-Click AI-powered document formatting and typography standardization.
- Full Drag & Drop file input support.
- Real-time progress bar, status feedback, and automatic output path generation.

### 2. 🔍 Interactive Live Paragraph Inspector & Override Studio
- Inspect every extracted document paragraph in a table view.
- View ML classifier confidence scores (%) and underlying classification logic.
- Filter low-confidence items flagged for review.
- Manually override any paragraph's classification (`Heading 1`, `Heading 2`, `Heading 3`, `Title`, `Author`, `Code Block`, `Blockquote`, `List`, `Caption`, etc.) before saving!

### 3. 🎨 Multi-Style Preset Studio
- Choose from professional built-in style presets:
  - **Classic Publication Book**: Traditional book layout with Times New Roman, indented body paragraphs, header chapter titles, and TOC.
  - **Academic / IEEE Journal**: Compact academic styling with bold headers, formal tables, and strict margins.
  - **Modern Corporate Report**: Clean Arial typography, navy headings, modern table grid, left-aligned body.
  - **Minimalist E-Book**: Georgia serif font with 1.6x line height and wide margins for digital reading.
  - **APA 7th Edition Paper**: Official APA paper standard (Times New Roman 12pt, double spacing, 1-inch margins).
- Custom preset manager: Create and save custom presets.

### 4. 📁 Batch Processing Studio
- Process multiple `.docx` documents or an entire folder in bulk.
- Batch queue status tracking and summary reports.

### 5. 📊 Readability & Structural Analytics Dashboard
- Flesch Reading Ease Score & Flesch-Kincaid Grade Level calculations.
- Estimated Reading Time calculation (WPM).
- Full document structural hierarchy tree (Headings, Chapters, Subheadings).
- Detailed statistics: Words, Paragraphs, Sentences, Characters, Tables, Images.

### 6. 🧹 Advanced Typography Cleaner Studio
- Configurable cleaning rules:
  - Standardize double hyphens (`--`) to Em-Dashes (`—`).
  - Convert straight quotes to Smart Quotes (`“` `”`).
  - Remove double spaces and redundant tabs.
  - Delete blank/empty paragraphs.
  - Auto-convert headings to Proper Title Case.
  - Standardize list bullet symbols (`*`, `-`, `+` -> `•`).
  - Clean trailing whitespaces across runs.

### 7. 📤 Multi-Format Document Exporter
- Export formatted documents into multiple formats:
  - `.docx` (Primary Word Document with OXML STYLEREF chapter titles, PAGE numbers, TOC field, table grid styling)
  - `.md` (Markdown document)
  - `.txt` (Plain text dump)
  - `.html` (Standalone styled web document with CSS)
  - `.pdf` (PDF document)

### 8. 📜 Persistent Activity History & Task Logger
- Keeps track of all processed files with timestamps, element counts, execution time, and preset used.

---

## 🖥️ UI Architecture (Desktop Application Layout)

The UI is built with **CustomTkinter** featuring a modern native desktop layout:
- **Left Navigation Sidebar**: Quick Format, Paragraph Inspector, Style Preset Studio, Batch Processing, Analytics, Cleaner, History, Settings.
- **Top Header**: Active Section Title, Theme Toggle (Dark / Light Mode).
- **Bottom Native Status Bar**: Real-time status indicators, model status, active preset info.

---

## 🚀 How to Run

### Desktop Application UI
```bash
python gui.py
```

### Command Line Interface (CLI)
```bash
# Basic usage (defaults to Classic Book preset)
python main.py input.docx output.docx

# Advanced usage with custom preset and all export formats
python main.py manuscript.docx formatted_manuscript.docx --preset academic_ieee --format all --inspect

# Batch folder processing
python main.py --batch ./raw_docs ./formatted_docs --preset modern_corporate
```

### Train ML Model
```bash
python train_model.py
```

---

## 🛠️ Project Structure

- `gui.py` — Native Desktop Application Interface (CustomTkinter)
- `main.py` — Command Line Interface (CLI)
- `cleaner.py` — `DocumentCleaner` typography engine
- `document_parser.py` — `DocumentParser` structure extractor
- `classifier.py` — `ParagraphClassifier` ML + Rule engine
- `formatter.py` — `DocumentFormatter` layout & OXML styling engine
- `presets.py` — `StylePreset` & `PresetManager`
- `analytics.py` — `DocumentAnalytics` readability & stats engine
- `exporter.py` — `DocumentExporter` multi-format exporter
- `history.py` — `HistoryManager` persistent task logger
- `train_model.py` — Synthetic dataset generator & model trainer
- `mock_generator.py` — Synthetic document generator
