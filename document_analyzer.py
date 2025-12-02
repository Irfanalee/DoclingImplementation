from docling.document_converter import DocumentConverter
from pathlib import Path
import json
from datetime import datetime
import pandas as pd

class DocumentAnalyzer:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.converter = DocumentConverter()
        self.result = None
        self.doc = None

    def analyze(self):
        """ Run complete analysis on the PDF document. """
        print(f"Starting analysis for: {self.pdf_path}\n")

        # Convert the PDF file
        self.result = self.converter.convert(self.pdf_path)
        self.doc = self.result.document

        #gather stats
        stats = self._get_statistics()

        # Extract components
        self._save_tables()
        self._save_markdown()
        self._create_summary_report(stats)

        print("Analysis complete.")

    def _get_statistics(self):
        """ Gather statistics about the document. """
        # Count headings from text elements
        headings = [t for t in self.doc.texts if 'heading' in t.label.lower() or 'section_header' in t.label.lower()]
        
        stats = {
            "Document Name": self.doc.name,
            "Total Text Elements": len(self.doc.texts),
            "Total Headings": len(headings),
            "Total Tables": len(self.doc.tables),
            "Total Pictures": len(self.doc.pictures)
        }
        return stats
    
    def _save_tables(self):
        """ Extract and save all tables as CSV. """
        for i, table in enumerate(self.doc.tables):
            df = table.export_to_dataframe()
            csv_path = Path(self.pdf_path).with_name(f"{Path(self.pdf_path).stem}_table_{i+1}.csv")
            df.to_csv(csv_path, index=False)
            print(f"Table {i+1} saved to: {csv_path}")

    def _save_markdown(self):
        """ Extract and save all tables as CSV. """
        markdown = self.result.document.export_to_markdown()
        markdown_path = Path(self.pdf_path).with_suffix('.md')
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"Markdown saved to: {markdown_path}")
    
    def _create_summary_report(self, stats):
        """ Create and save a summary report as JSON. """
        report = {
            "Analysis Date": datetime.now().isoformat(),
            "Document Statistics": stats
        }
        report_path = Path(self.pdf_path).with_name(f"{Path(self.pdf_path).stem}_summary.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4)
        print(f"Summary report saved to: {report_path}")

if __name__ == "__main__":
    pdf_path = "./data/the-state-of-ai-in-2025-agents-innovation-and-transformation.pdf"
    analyzer = DocumentAnalyzer(pdf_path)
    analyzer.analyze()
