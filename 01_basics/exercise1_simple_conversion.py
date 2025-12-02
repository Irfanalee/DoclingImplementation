"""
EXERCISE 1: Simple PDF to Markdown Conversion
==============================================
Time: ~10 minutes

LEARNING GOALS:
- Import and use DocumentConverter
- Convert a PDF to markdown
- Access the converted text
- Save output to a file

INSTRUCTIONS:
Complete the TODOs below. Run the script to test your code.
"""

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
    
    


    # TODO 3: Export the result to markdown
    # HINT: markdown_text = result.document.export_to_markdown()
    markdown = result.document.export_to_markdown()

    
    return markdown


def save_markdown_to_file(markdown_text: str, output_path: str):
    """
    Save markdown text to a file.
    
    Args:
        markdown_text: The markdown content
        output_path: Path where to save the file
    """
    # TODO 4: Write the markdown text to a file
    # HINT: Use open() with 'w' mode and write the text
    
    pass


def main():
    """Main function to test your code."""
    print("🚀 Exercise 1: Simple PDF Conversion\n")
    
    # Test with a simple text file first (since we may not have PDFs yet)
    test_file = "./data/the-state-of-ai-in-2025-agents-innovation-and-transformation.pdf"
    output_file = "./output/output_exercise1.md"
    
    try:
        print(f"📄 Converting: {test_file}")
        
        # TODO 5: Call your convert_pdf_to_markdown function
        # HINT: markdown = convert_pdf_to_markdown(test_file)
        markdown = convert_pdf_to_markdown(test_file)
        
        print(f"✅ Conversion successful!")
        print(f"📝 Preview (first 200 chars):")
        # TODO 6: Print the first 200 characters of markdown
        # HINT: print(markdown[:200])
        print(markdown[:200])
        
        # TODO 7: Save the markdown to a file
        # HINT: save_markdown_to_file(markdown, output_file)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown)

        
        
        print(f"\n💾 Saved to: {output_file}")
        
    except FileNotFoundError:
        print(f"⚠️  File not found: {test_file}")
        print("💡 Create a sample PDF or update the path above")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()


