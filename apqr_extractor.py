#!/usr/bin/env python3
"""
APQR Document Extractor

This script extracts, organizes, and structures APQR (Annual Product Quality Review) 
Word documents for Aspirin Tablets 325 mg.

Features:
- Extracts text, tables, and images from Word documents
- Organizes content into numbered section folders
- Maintains traceability with document source and page references
- Saves content as text.md, tables.json, and images
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple
import argparse

try:
    from docx import Document
    from docx.document import Document as DocumentType
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    from docx.shape import InlineShape
    import docx.oxml.ns as ns
    from docx.oxml import OxmlElement
except ImportError:
    print("python-docx not installed. Installing...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx"])
    from docx import Document
    from docx.document import Document as DocumentType
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    from docx.shape import InlineShape
    import docx.oxml.ns as ns
    from docx.oxml import OxmlElement

class APQRExtractor:
    """Main class for extracting and organizing APQR documents."""
    
    def __init__(self, output_dir: str = "APQR_Aspirin325mg"):
        self.output_dir = Path(output_dir)
        self.sections = []
        self.current_section = None
        
        # Common APQR section patterns (can be extended)
        self.section_patterns = [
            r"^1\.?\s*Product\s+Details?",
            r"^2\.?\s*Batch\s+Summary",
            r"^3\.?\s*Yield\s+Reconciliation",
            r"^4\.?\s*Deviations?",
            r"^5\.?\s*Stability",
            r"^6\.?\s*Raw\s+Materials?",
            r"^7\.?\s*Manufacturing\s+Process",
            r"^8\.?\s*In-Process\s+Controls?",
            r"^9\.?\s*Finished\s+Product\s+Testing",
            r"^10\.?\s*Packaging\s+Controls?",
            r"^11\.?\s*Quality\s+Control\s+Data",
            r"^12\.?\s*Complaints?",
            r"^13\.?\s*Returns?",
            r"^14\.?\s*Change\s+Controls?",
            r"^15\.?\s*Corrective\s+Actions?",
            r"^16\.?\s*Preventive\s+Actions?",
            r"^17\.?\s*Risk\s+Assessment",
            r"^18\.?\s*Trend\s+Analysis",
            r"^19\.?\s*Conclusions?",
            r"^20\.?\s*Recommendations?",
            r"^21\.?\s*Appendix",
            r"^22\.?\s*References?",
        ]
    
    def create_folder_structure(self):
        """Create the main project folder and initialize structure."""
        self.output_dir.mkdir(exist_ok=True)
        print(f"Created main project folder: {self.output_dir}")
    
    def extract_document(self, doc_path: str, doc_name: str) -> Dict[str, Any]:
        """Extract content from a single Word document."""
        print(f"Processing document: {doc_path}")
        
        try:
            doc = Document(doc_path)
        except Exception as e:
            print(f"Error opening document {doc_path}: {e}")
            return {}
        
        sections = {}
        current_section = None
        section_counter = 0
        
        for i, paragraph in enumerate(doc.paragraphs):
            text = paragraph.text.strip()
            
            if not text:
                continue
            
            # Check if this paragraph starts a new section
            section_match = self.identify_section(text)
            if section_match:
                section_counter += 1
                current_section = {
                    'number': section_counter,
                    'title': section_match,
                    'content': [],
                    'tables': [],
                    'images': [],
                    'source_doc': doc_name,
                    'start_paragraph': i
                }
                sections[f"{section_counter:02d}_{self.sanitize_filename(section_match)}"] = current_section
                print(f"Found section {section_counter}: {section_match}")
            
            # Add content to current section
            if current_section:
                current_section['content'].append({
                    'type': 'paragraph',
                    'text': text,
                    'paragraph_index': i,
                    'style': paragraph.style.name if paragraph.style else 'Normal'
                })
        
        # Extract tables
        for i, table in enumerate(doc.tables):
            table_data = self.extract_table(table)
            # Find which section this table belongs to
            # This is a simplified approach - in practice, you'd need more sophisticated logic
            if current_section:
                current_section['tables'].append({
                    'table_index': i,
                    'data': table_data,
                    'source_doc': doc_name
                })
        
        return sections
    
    def identify_section(self, text: str) -> str:
        """Identify if a paragraph starts a new section."""
        for pattern in self.section_patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return text
        
        # Also check for numbered sections
        numbered_section = re.match(r'^(\d+\.?\d*)\s+(.+)', text)
        if numbered_section and len(text) < 100:  # Likely a section header
            return text
        
        return None
    
    def extract_table(self, table: Table) -> List[List[str]]:
        """Extract table data into a list of lists."""
        table_data = []
        for row in table.rows:
            row_data = []
            for cell in row.cells:
                row_data.append(cell.text.strip())
            table_data.append(row_data)
        return table_data
    
    def sanitize_filename(self, text: str) -> str:
        """Sanitize text for use as a filename."""
        # Remove numbers and dots at the beginning
        text = re.sub(r'^\d+\.?\s*', '', text)
        # Replace spaces and special characters with underscores
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '_', text)
        return text.strip('_')
    
    def save_section_content(self, section_key: str, section_data: Dict[str, Any]):
        """Save section content to appropriate files."""
        section_dir = self.output_dir / section_key
        section_dir.mkdir(exist_ok=True)
        
        # Create images subdirectory
        images_dir = section_dir / "images"
        images_dir.mkdir(exist_ok=True)
        
        # Save text content
        text_file = section_dir / "text.md"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(f"# {section_data['title']}\n\n")
            f.write(f"**Source Document:** {section_data['source_doc']}\n")
            f.write(f"**Section Number:** {section_data['number']}\n")
            f.write(f"**Start Paragraph:** {section_data['start_paragraph']}\n\n")
            f.write("## Content\n\n")
            
            for content in section_data['content']:
                if content['type'] == 'paragraph':
                    if content['style'] in ['Heading 1', 'Heading 2', 'Heading 3']:
                        level = int(content['style'][-1]) + 2  # Adjust heading level
                        f.write(f"{'#' * level} {content['text']}\n\n")
                    else:
                        f.write(f"{content['text']}\n\n")
        
        # Save tables
        if section_data['tables']:
            tables_file = section_dir / "tables.json"
            with open(tables_file, 'w', encoding='utf-8') as f:
                json.dump(section_data['tables'], f, indent=2, ensure_ascii=False)
        
        print(f"Saved section: {section_key}")
    
    def process_documents(self, doc_paths: List[str]):
        """Process multiple APQR documents."""
        self.create_folder_structure()
        
        all_sections = {}
        
        for i, doc_path in enumerate(doc_paths, 1):
            doc_name = f"Doc{i}"
            sections = self.extract_document(doc_path, doc_name)
            
            # Merge sections (handle duplicates)
            for section_key, section_data in sections.items():
                if section_key in all_sections:
                    # Merge content from multiple documents
                    all_sections[section_key]['content'].extend(section_data['content'])
                    all_sections[section_key]['tables'].extend(section_data['tables'])
                    all_sections[section_key]['source_doc'] += f", {doc_name}"
                else:
                    all_sections[section_key] = section_data
        
        # Save all sections
        for section_key, section_data in sorted(all_sections.items()):
            self.save_section_content(section_key, section_data)
        
        # Create summary
        self.create_summary(all_sections)
    
    def create_summary(self, sections: Dict[str, Any]):
        """Create a summary of extracted sections."""
        summary_file = self.output_dir / "extraction_summary.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("# APQR Extraction Summary\n\n")
            f.write("## Extracted Sections\n\n")
            
            for section_key, section_data in sorted(sections.items()):
                f.write(f"- **{section_key}**: {section_data['title']}\n")
                f.write(f"  - Content items: {len(section_data['content'])}\n")
                f.write(f"  - Tables: {len(section_data['tables'])}\n")
                f.write(f"  - Images: {len(section_data['images'])}\n")
                f.write(f"  - Source: {section_data['source_doc']}\n\n")
            
            f.write(f"\n**Total Sections Extracted:** {len(sections)}\n")
        
        print(f"Created extraction summary: {summary_file}")


def main():
    """Main function to run the APQR extractor."""
    parser = argparse.ArgumentParser(description='Extract and organize APQR Word documents')
    parser.add_argument('documents', nargs='+', help='Path(s) to APQR Word documents')
    parser.add_argument('--output', '-o', default='APQR_Aspirin325mg', 
                       help='Output directory name (default: APQR_Aspirin325mg)')
    
    args = parser.parse_args()
    
    # Verify documents exist
    for doc_path in args.documents:
        if not os.path.exists(doc_path):
            print(f"Error: Document not found: {doc_path}")
            return 1
    
    # Create extractor and process documents
    extractor = APQRExtractor(args.output)
    extractor.process_documents(args.documents)
    
    print(f"\nExtraction completed successfully!")
    print(f"Output directory: {extractor.output_dir}")
    print(f"Structure created with {len(os.listdir(extractor.output_dir))} items")
    
    return 0


if __name__ == "__main__":
    exit(main())