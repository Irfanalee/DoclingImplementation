# Learn Docling in 1 Hour 🚀

**Docling** is IBM's powerful document parsing library that converts PDFs, Word docs, and other formats into structured data (markdown, JSON, etc.).

## 🎯 Learning Path (60 minutes)

### Phase 1: Setup & Basics (15 min)
- **File**: `01_basics/exercise1_simple_conversion.py`
- Learn to convert a PDF to markdown
- Extract text from documents

### Phase 2: Intermediate (20 min)
- **File**: `02_intermediate/exercise2_tables.py`
- Extract tables from PDFs
- Work with document structure
- **File**: `02_intermediate/exercise3_metadata.py`
- Extract document metadata and images

### Phase 3: Advanced (15 min)
- **File**: `03_advanced/exercise4_custom_pipeline.py`
- Customize the conversion pipeline
- Export to different formats

### Phase 4: Practice Challenge (10 min)
- **File**: `04_challenge/final_challenge.py`
- Build a complete document processor

## 📦 Installation

```bash
# Install docling
pip install docling

# Optional: For better PDF support
pip install pypdfium2
```

## 🎓 How to Use This Tutorial

1. Each exercise file has:
   - `# TODO:` comments where you write code
   - `# HINT:` to guide you
   - `# SOLUTION:` (commented out) if you get stuck

2. Test data is in the `sample_docs/` folder

3. Work through exercises in order

4. Aim for ~10-15 min per section

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

## 🚀 Getting Started

Start with: `python 01_basics/exercise1_simple_conversion.py`

Good luck! 💪
