from docling.document_converter import DocumentConverter
from pathlib import Path
import json
from datetime import datetime
import fitz  # PyMuPDF
import argparse
from typing import List


class DoclingServer:
    def __init__(self, input_folder: str, output_folder: str):
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)
        self.converter = DocumentConverter()
        self.processing_summary = []

        # Create output directory structure
        self.tables_dir = self.output_folder / "tables"
        self.images_dir = self.output_folder / "images"
        self.markdown_dir = self.output_folder / "markdown"

        # Create all directories
        self.output_folder.mkdir(exist_ok=True)
        self.tables_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)
        self.markdown_dir.mkdir(exist_ok=True)

    def process_all_files(self):
        """Process all PDF files in the input folder."""
        print(f"Starting DoclingServer...")
        print(f"Input folder: {self.input_folder}")
        print(f"Output folder: {self.output_folder}\n")

        # Find all PDF files
        pdf_files = list(self.input_folder.glob("*.pdf"))

        if not pdf_files:
            print(f"No PDF files found in {self.input_folder}")
            return

        print(f"Found {len(pdf_files)} PDF file(s) to process\n")

        for pdf_file in pdf_files:
            print(f"{'='*60}")
            print(f"Processing: {pdf_file.name}")
            print(f"{'='*60}")

            try:
                self.process_single_file(pdf_file)
                self.processing_summary.append({
                    "file": pdf_file.name,
                    "status": "success",
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                print(f"ERROR processing {pdf_file.name}: {e}")
                self.processing_summary.append({
                    "file": pdf_file.name,
                    "status": "failed",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })

        # Create summary report
        self._create_summary_report()
        print(f"\n{'='*60}")
        print("Processing complete!")
        print(f"{'='*60}")

    def process_single_file(self, pdf_path: Path):
        """Process a single PDF file."""
        # Convert the PDF
        print("Converting document...")
        result = self.converter.convert(str(pdf_path))
        doc = result.document

        file_stem = pdf_path.stem

        # Extract tables
        print(f"Extracting tables...")
        tables_count = self._extract_tables(doc, file_stem)

        # Extract images
        print(f"Extracting images...")
        images_count = self._extract_images(pdf_path, file_stem)

        # Extract markdown
        print(f"Extracting markdown...")
        self._extract_markdown(result, file_stem)

        print(f"✅ Completed: {tables_count} tables, {images_count} images extracted\n")

    def _extract_tables(self, doc, file_stem: str) -> int:
        """Extract all tables from the document."""
        if not doc.tables:
            print("  No tables found")
            return 0

        for i, table in enumerate(doc.tables):
            df = table.export_to_dataframe()
            csv_path = self.tables_dir / f"{file_stem}_table_{i+1}.csv"
            df.to_csv(csv_path, index=False)
            print(f"  Table {i+1} saved to: {csv_path.name}")

        return len(doc.tables)

    def _extract_images(self, pdf_path: Path, file_stem: str) -> int:
        """Extract all images from the PDF using PyMuPDF."""
        # Create a subdirectory for this document's images
        doc_images_dir = self.images_dir / file_stem
        doc_images_dir.mkdir(exist_ok=True)

        saved_count = 0

        # Use PyMuPDF to extract images
        doc = fitz.open(str(pdf_path))
        for page_num in range(len(doc)):
            page = doc[page_num]
            images = page.get_images()

            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                image_path = doc_images_dir / f"page{page_num+1}_img{img_index+1}.{image_ext}"
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                saved_count += 1

        doc.close()

        if saved_count == 0:
            print("  No images found")
        else:
            print(f"  {saved_count} image(s) saved to: {doc_images_dir.name}/")

        return saved_count

    def _extract_markdown(self, result, file_stem: str):
        """Extract markdown from the document."""
        markdown = result.document.export_to_markdown()
        markdown_path = self.markdown_dir / f"{file_stem}.md"

        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown)

        print(f"  Markdown saved to: {markdown_path.name}")

    def _create_summary_report(self):
        """Create a summary report of all processed files."""
        report_path = self.output_folder / "summary_report.txt"

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("DOCLING SERVER - PROCESSING SUMMARY\n")
            f.write("="*60 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Input Folder: {self.input_folder}\n")
            f.write(f"Output Folder: {self.output_folder}\n\n")

            f.write(f"Total Files Processed: {len(self.processing_summary)}\n")

            successful = [s for s in self.processing_summary if s['status'] == 'success']
            failed = [s for s in self.processing_summary if s['status'] == 'failed']

            f.write(f"Successful: {len(successful)}\n")
            f.write(f"Failed: {len(failed)}\n\n")

            f.write("-"*60 + "\n")
            f.write("FILE DETAILS\n")
            f.write("-"*60 + "\n\n")

            for item in self.processing_summary:
                f.write(f"File: {item['file']}\n")
                f.write(f"Status: {item['status'].upper()}\n")
                f.write(f"Timestamp: {item['timestamp']}\n")
                if 'error' in item:
                    f.write(f"Error: {item['error']}\n")
                f.write("\n")

            f.write("-"*60 + "\n")
            f.write("OUTPUT STRUCTURE\n")
            f.write("-"*60 + "\n")
            f.write(f"{self.output_folder}/\n")
            f.write(f"├── tables/          # CSV files with extracted tables\n")
            f.write(f"├── images/          # Extracted images organized by document\n")
            f.write(f"├── markdown/        # Markdown exports of documents\n")
            f.write(f"└── summary_report.txt  # This file\n")

        print(f"\n📄 Summary report saved to: {report_path}")


def main():
    parser = argparse.ArgumentParser(
        description="DoclingServer - Batch process PDF files and extract tables, images, and markdown"
    )
    parser.add_argument(
        "input_folder",
        type=str,
        help="Path to folder containing PDF files to process"
    )
    parser.add_argument(
        "output_folder",
        type=str,
        help="Path to folder where output will be saved"
    )

    args = parser.parse_args()

    # Create and run server
    server = DoclingServer(args.input_folder, args.output_folder)
    server.process_all_files()


if __name__ == "__main__":
    # Example usage (can be run directly or via command line)
    # Uncomment the lines below to run with hardcoded paths
    # server = DoclingServer("./data", "./output")
    # server.process_all_files()

    # Or use command line arguments
    main()
