# Docling Learning Session - Context Summary

## Session Overview
**Date**: December 2, 2025  
**Goal**: Learn IBM Docling library in 1 hour through hands-on coding exercises  
**Approach**: Student writes code with guided hints and debugging support

## Environment Setup
- **Python**: Virtual environment (venv)
- **Library**: Docling (installed via requirements.txt)
- **PDFs Used**: 
  - `openAI-File.pdf` (image-heavy, 13MB, 25 pages)
  - `the-state-of-ai-in-2025-agents-innovation-and-transformation.pdf` (text-rich)

## Key Learnings & Patterns

### 1. Core Docling Object Model
```python
# Conversion flow
converter = DocumentConverter()
result = converter.convert("file.pdf")
doc = result.document

# Key distinction:
# - `result.document` = Rich data structure (navigate, analyze)
# - `doc.export_to_markdown()` = Plain text output (save, display)
```

### 2. Common Attribute Names (Learned Through Errors)
```python
# Correct attribute names:
table.data.num_rows       # NOT table.num_rows
table.data.num_cols       # NOT table.num_columns
table.prov[0].page_no     # NOT table.prov[0].page_number
text.label                # NOT text.lablel
```

### 3. Document Structure Access
```python
doc.name                  # Document name
doc.texts                 # All text elements
doc.tables                # All tables
doc.pictures              # All images

# Text element properties:
text.label                # "text", "section_header", "paragraph", "list_item"
text.text                 # Actual content
text.prov[0].page_no      # Page location
```

### 4. PDF Type Variations (Critical Discovery)
Different PDFs use different label conventions:
- **Type 1**: Uses "heading", "paragraph"
- **Type 2**: Uses "section_header", "text"

**Robust solution**:
```python
# Handle both types
if "heading" in label or "section_header" in label:
    # Treat as heading
if "paragraph" in label or label == "text":
    # Treat as paragraph
```

### 5. Table Export Methods
```python
table.export_to_markdown()      # Markdown format
table.export_to_dataframe()     # Pandas DataFrame
table.export_to_dict()          # Python dictionary
```

## Completed Exercises

### Exercise 1: Basic Conversion (`01_basics/exercise1_simple_conversion.py`)
- Convert PDF to markdown
- Save output to file
- Debug path navigation (`./` vs `../`)
- Learned: Image-heavy PDFs extract minimal text

### Exercise 2: Table Extraction (`02_intermediate/excercise2_tables.py`)
- Extract tables from PDFs
- Access table dimensions and location
- Export tables to CSV/DataFrame
- **Key insight**: Table data is at `table.data`, not `table` directly

### Exercise 3: Document Structure (`02_intermediate/excercise3_structure.py`)
- Categorize text elements by type
- Generate document outline
- Count headings, paragraphs, lists
- **Key insight**: PDF label conventions vary - must check both types

## Common Debugging Patterns

### Pattern 1: Attribute Not Found
**Error**: `AttributeError: 'X' object has no attribute 'Y'`
**Solution**: Check correct object hierarchy (e.g., `table.data.num_rows` not `table.num_rows`)

### Pattern 2: Type Confusion
**Error**: `AttributeError: 'str' object has no attribute 'texts'`
**Solution**: Passing wrong type - pass `document` object, not `markdown` string

### Pattern 3: Label Mismatch
**Issue**: Zero headings found
**Solution**: Debug with sample labels, adjust matching logic to handle variations

## File Path Conventions
```python
# Running from project root (doclingTest/)
"./data/file.pdf"              # ✅ Correct
"../data/file.pdf"             # ❌ Wrong (goes outside project)

# Best practice: Use absolute paths
from pathlib import Path
project_root = Path(__file__).parent
pdf_path = project_root / "data" / "file.pdf"
```

## Next Steps: Final Project
**Goal**: Build `document_analyzer.py` - a complete document processing tool

**Requirements**:
1. Accept any PDF file
2. Extract all components (tables, images, text)
3. Generate comprehensive analysis report
4. Save organized outputs (CSV tables, markdown, JSON summary)
5. Handle errors gracefully

**Key skills to apply**:
- Combining conversion + analysis in single class
- Robust label detection (handle multiple PDF types)
- File organization (create output directories)
- Summary reporting (JSON + Markdown formats)

## Technical Notes

### OCR Behavior
- Docling automatically selects OCR engine (observed: `ocrmac` on macOS)
- Processing time: ~15-85 seconds depending on PDF complexity
- Accelerator: Uses `mps` (Metal Performance Shaders) on macOS

### Export Formats Available
- Markdown: `doc.export_to_markdown()`
- JSON: `doc.export_to_dict()` → `json.dump()`
- DataFrame: `table.export_to_dataframe()` (requires pandas)

### Project Structure Created
```
doclingTest/
├── data/                    # PDF inputs
├── output/                  # Conversion outputs
├── 01_basics/              # Exercise 1
├── 02_intermediate/        # Exercises 2-3
├── document_analyzer.py    # Final project
└── requirements.txt        # Dependencies
```

## Learning Methodology Success Factors
1. **Hands-on coding**: Student writes all code
2. **Error-driven learning**: Debug real issues together
3. **Incremental complexity**: Start simple, build up
4. **Pattern recognition**: Attribute naming conventions, PDF variations
5. **Real-world awareness**: Different PDFs behave differently

## Time Allocation (60 min target)
- Setup: 5 min ✅
- Exercise 1: 15 min ✅
- Exercise 2: 15 min ✅
- Exercise 3: 15 min ✅
- Final Project: 10 min (in progress)
