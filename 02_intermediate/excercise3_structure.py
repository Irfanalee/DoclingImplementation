from docling.document_converter import DocumentConverter
import json

def convert_pdf_to_markdown(pdf_path: str) -> str:
    """
    Convert a PDF file to markdown format.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Markdown string of the document
    """
    # TODO 1: Create a DocumentConverter instance
    # HINT: converter = DocumentConverter()
    converter = DocumentConverter()
    
    
    # TODO 2: Convert the PDF file
    # HINT: result = converter.convert(pdf_path)
    result = converter.convert(pdf_path)
    
    # debugging print
    doc = result.document
    
    print(f"📄 Document Name: {doc.name}")
    print(f"📝 Total text elements: {len(doc.texts)}")
    print(f"📊 Total tables: {len(doc.tables)}")
    print(f"🖼️  Total pictures: {len(doc.pictures)}")

    # TODO 3: Export the document to markdown
    # HINT: markdown = result.to_markdown()
    markdown = result.document.export_to_markdown()


    return doc  # Return the document object, not undefined 'document'

def categorize_text_elements(document):
    # Count the different element types
    headings = []
    paragraphs = []
    lists = []
    print("\n🔍 Debug: First 20 element labels:")
    for i, text in enumerate(document.texts[:20]):
        print(f"  {i+1}. {text.label}")
    for text in document.texts:
        label = text.label.lower()  # Fixed typo: was 'lablel'
        # Check for both "heading" and "section_header" to work with different PDF types
        if "heading" in label or "section_header" in label:
            headings.append(text)
        # Check for both "paragraph" and "text" labels
        elif "paragraph" in label or label == "text":  
            paragraphs.append(text)
        elif "list" in label:
            lists.append(text)
    print(f"\n📑 Headings: {len(headings)}")
    print(f"📃 Paragraphs: {len(paragraphs)}")
    print(f"📝 List items: {len(lists)}")

    return headings, paragraphs, lists

    
def document_outline(document):
    outline = []
    headings, paragraphs, lists = categorize_text_elements(document)
    for heading in headings:
        outline.append(heading.text)
        print(f"\n🔹 [{heading.label}]  {heading.text}")


if __name__ == "__main__":
    pdf_path = "./data/the-state-of-ai-in-2025-agents-innovation-and-transformation.pdf"
    doc = convert_pdf_to_markdown(pdf_path)  # This returns document object now
    
    # Export to markdown and save
    markdown_text = doc.export_to_markdown()
    with open("02_intermediate/excercise3_output.md", "w") as f:
        f.write(markdown_text)
    
    # Analyze document structure
    document_outline(doc)