# Docling Implementation

**Docling** is IBM's powerful document parsing library that converts PDFs, Word docs, and other formats into structured data (markdown, JSON, etc.).

This repository contains practical examples and exercises for learning and implementing Docling.

## 📂 Project Structure

```
DoclingImplementation/
├── 01_basics/                  # Basic conversion examples
│   └── exercise1_simple_conversion.py
├── 02_intermediate/            # Intermediate features
│   ├── excercise2_tables.py    # Table extraction
│   └── excercise3_structure.py # Document structure analysis
├── data/                       # Sample documents for processing
├── output/                     # Generated output files
├── document_analyzer.py        # Main document analysis script
└── requirements.txt            # Python dependencies
```

## 📦 Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd DoclingImplementation

# Install dependencies
pip install -r requirements.txt
```

### Requirements
- Python 3.8+
- docling
- pandas

## 🚀 Getting Started

### 1. Basic Conversion
Start with simple document conversion:
```bash
python 01_basics/exercise1_simple_conversion.py
```

### 2. Table Extraction
Extract tables from documents:
```bash
python 02_intermediate/excercise2_tables.py
```

### 3. Document Structure Analysis
Analyze document structure and hierarchy:
```bash
python 02_intermediate/excercise3_structure.py
```

### 4. Document Analyzer
Use the main analyzer for comprehensive document processing:
```bash
python document_analyzer.py
```

## 📚 Quick Reference

### Core Concepts

**DocumentConverter**: Main class for converting documents
```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("document.pdf")
```

**Export Formats**:
- Markdown (`.export_to_markdown()`)
- JSON (`.export_to_json()`)
- Doctags (`.export_to_doctags()`)

**Key Classes**:
- `DocumentConverter`: Main conversion engine
- `ConversionResult`: Contains parsed document
- `PipelineOptions`: Configure conversion behavior

## 📁 Data Folder

The `data/` folder contains sample documents for testing and learning purposes.

## 📤 Output Folder

The `output/` folder stores generated files from document processing (markdown, JSON, etc.).

## 🤝 Contributing

Feel free to add more examples and exercises to help others learn Docling!

## 📄 License

This project is for educational purposes.
