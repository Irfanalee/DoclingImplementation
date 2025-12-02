from docling.document_converter import DocumentConverter
import json
import pandas as pd

def extract_tables_from_pdf(pdf_path: str) -> list:
    """Extract all tables from a PDF."""
    # TODO: Create converter and convert the PDF
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    document = result.document

    print(f"Document has {len(document.tables)} tables.")

    return document.tables


    # TODO: Access result.document.tables
    # TODO: Return the tables
    pass

def save_table_as_csv(table, output_path: str):
    """Save a table as a JSON file."""
    df = table.export_to_dataframe()
    df.to_csv(f"table{i}.csv", index=False)



if __name__ == "__main__":
    print("🚀 Exercise 2: Extract Tables from PDF\n")

    # Use your own PDF file with tables for testing
    test_pdf = "./data/the-state-of-ai-in-2025-agents-innovation-and-transformation.pdf"  # TODO: Update with your PDF

    tables = extract_tables_from_pdf(test_pdf)
    for i, table in enumerate(tables, 1):
        print(f"\nTable {i}:")
        print(f" Size : {table.data.num_rows} rows x {table.data.num_cols} columns")
        print(f" Page : {table.prov[0].page_no if table.prov else 'N/A'}")
        print(table.export_to_markdown())
        save_table_as_csv(table, f"./output/table_{i}.csv")  