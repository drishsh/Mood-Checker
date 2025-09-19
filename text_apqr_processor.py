#!/usr/bin/env python3
"""
Text-based APQR Document Processor

This script processes APQR documents provided as text and organizes them
into the structured folder system as specified.
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple
import argparse

class TextAPQRProcessor:
    """Processor for text-based APQR documents."""
    
    def __init__(self, output_dir: str = "APQR_Aspirin325mg"):
        self.output_dir = Path(output_dir)
        self.sections = {}
        
    def create_folder_structure(self):
        """Create the main project folder."""
        self.output_dir.mkdir(exist_ok=True)
        print(f"Created main project folder: {self.output_dir}")
    
    def extract_tables_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract table-like structures from text."""
        tables = []
        
        # Look for patterns that indicate tables
        # Pattern 1: Multiple columns separated by spaces/tabs
        lines = text.split('\n')
        current_table = []
        
        for line in lines:
            # Check if line has multiple columns (simple heuristic)
            if re.search(r'\s{2,}', line.strip()) and len(line.strip()) > 20:
                # Split by multiple spaces to get columns
                columns = re.split(r'\s{2,}', line.strip())
                if len(columns) > 1:
                    current_table.append(columns)
            else:
                if current_table and len(current_table) > 1:  # Save table if it has multiple rows
                    tables.append({
                        'data': current_table,
                        'type': 'space_separated'
                    })
                current_table = []
        
        # Add final table if exists
        if current_table and len(current_table) > 1:
            tables.append({
                'data': current_table,
                'type': 'space_separated'
            })
        
        return tables
    
    def process_document_1(self, doc_path: str) -> Dict[str, Any]:
        """Process Document 1 - the detailed form-based APQR."""
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        sections = {}
        
        # Document 1 sections based on the content analysis
        doc1_sections = [
            ("01_Product_Details", "1. Product Details", "Product details including dosage form, label claim, shelf life, etc."),
            ("02_Batch_Summary", "2. Number of Batches manufactured", "Monthly batch manufacturing summary"),
            ("03_Marketing_Authorization", "3. A review of marketing Authorization variations", "Marketing authorization variations review"),
            ("04_Starting_Materials", "4. A review of starting materials", "Starting materials and packaging materials review"),
            ("05_API_Critical_Parameters", "5. Active Pharmaceutical Ingredients (API) critical parameters", "API critical parameters and trend analysis"),
            ("06_Environment_Control", "6. Environment Control Result During Mixing", "Environmental control during mixing process"),
            ("07_Water_Testing", "7. Water Testing Result", "Water testing results and analysis"),
            ("08_Bulk_Analysis", "8. Bulk Analysis Test", "Bulk testing and analysis results"),
            ("09_Bio_Burden", "9. Bio burden Test Result", "Bio burden testing results"),
            ("10_Filter_Integrity", "10. Filter Integrity test", "Filter integrity testing results"),
            ("11_Yield_Critical_Stages", "11. Yield of all critical stages", "Yield analysis for critical manufacturing stages"),
            ("12_Final_Batch_Yield", "12. Final Batch Yield", "Final batch yield and analysis report"),
            ("13_Failed_Batches", "13. A review of all batches that failed", "Review of failed batches and investigations"),
            ("14_Process_Changes", "14. A review of all changes carried out", "Process and analytical method changes"),
            ("15_OOS_Investigations", "15. Out of specifications and laboratory Investigations", "Out of specification investigations"),
            ("16_Process_Validation", "16. Process Validation Status", "Process validation status review"),
            ("17_Deviation_Review", "17. Review of Deviation", "Deviation review and analysis"),
            ("18_Quality_Returns", "18. A review of all quality –related returns", "Quality-related returns, complaints and recalls"),
            ("19_Control_Sample", "19. Control Sample Review", "Control sample review"),
            ("20_Previous_APQRs", "20. A review of previous APQRs", "Previous APQR review and CAPA delays"),
            ("21_Stability_Monitoring", "21. A review of the results of the stability monitoring", "Stability monitoring program results"),
            ("22_Equipment_Qualification", "22. The qualification status of relevant equipment", "Equipment and utilities qualification status"),
            ("23_Sterilization_Parameters", "23. A review of Product Sterilization parameters", "Product sterilization parameters review"),
            ("24_Contractual_Arrangements", "24. A review of any contractual arrangements", "Contractual arrangements review"),
            ("25_Annual_Report_Summary", "25. Annual Product Report – Summary", "Annual product report summary and conclusions")
        ]
        
        # Extract content for each section
        for section_key, section_title, description in doc1_sections:
            section_content = self.extract_section_content(content, section_title, "Doc1")
            if section_content:
                sections[section_key] = {
                    'title': section_title,
                    'description': description,
                    'content': section_content,
                    'source_doc': 'Document_1',
                    'tables': self.extract_tables_from_text(section_content.get('text', ''))
                }
        
        return sections
    
    def process_document_2(self, doc_path: str) -> Dict[str, Any]:
        """Process Document 2 - the US template APQR."""
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        sections = {}
        
        # Document 2 sections based on the US template structure
        doc2_sections = [
            ("01_Objective_Scope", "1. Objective and Scope", "APQR objective and scope definition"),
            ("02_Product_Identification", "2. Product Identification & Background", "Product identification and background information"),
            ("03_Executive_Summary", "3. Executive Summary", "High-level summary of manufacturing performance"),
            ("04_Manufacturing_Batch_Records", "4. Manufacturing & Batch Records Summary", "Manufacturing and batch records summary"),
            ("05_Quality_Control_Results", "5. Quality Control / QC Results Summary", "Quality control results and analysis"),
            ("06_Trend_Analysis", "6. Trend Analysis and Statistical Review", "Statistical analysis and trending"),
            ("07_Deviations_OOS_CAPA", "7. Deviations, OOS/OOT and CAPA Summary", "Deviations, OOS/OOT and CAPA summary"),
            ("08_Stability_Program", "8. Stability Program and Results", "Stability program and results review"),
            ("09_Supplier_Materials", "9. Supplier and Materials Review", "Supplier and materials performance review"),
            ("10_Change_Control", "10. Change Control and Regulatory Commitments", "Change control and regulatory commitments"),
            ("11_Validation_Qualification", "11. Validation and Equipment Qualification Summary", "Validation and equipment qualification"),
            ("12_Complaints_Recalls", "12. Complaints, Recalls and Market Actions", "Complaints, recalls and market actions"),
            ("13_Inspection_Audit", "13. Inspection and Audit Findings", "Inspection and audit findings"),
            ("14_Conclusions_Recommendations", "14. Conclusions and Recommendations", "Conclusions and recommendations"),
            ("15_Action_Plan", "15. Action Plan (Owners & Timelines)", "Action plan with owners and timelines"),
            ("16_Appendices", "16. Appendices / Attachments", "Appendices and attachments")
        ]
        
        # Extract content for each section
        for section_key, section_title, description in doc2_sections:
            section_content = self.extract_section_content(content, section_title, "Doc2")
            if section_content:
                sections[section_key] = {
                    'title': section_title,
                    'description': description,
                    'content': section_content,
                    'source_doc': 'Document_2',
                    'tables': self.extract_tables_from_text(section_content.get('text', ''))
                }
        
        return sections
    
    def extract_section_content(self, content: str, section_title: str, doc_id: str) -> Dict[str, Any]:
        """Extract content for a specific section."""
        # Find the section in the content
        lines = content.split('\n')
        section_start = -1
        section_end = -1
        
        # Look for the section title
        for i, line in enumerate(lines):
            if section_title.lower() in line.lower():
                section_start = i
                break
        
        if section_start == -1:
            return None
        
        # Find the end of the section (next numbered section or end of document)
        for i in range(section_start + 1, len(lines)):
            line = lines[i].strip()
            # Look for next numbered section
            if re.match(r'^\d+\.', line) and len(line) < 100:
                section_end = i
                break
        
        if section_end == -1:
            section_end = len(lines)
        
        # Extract the section content
        section_lines = lines[section_start:section_end]
        section_text = '\n'.join(section_lines)
        
        return {
            'text': section_text,
            'start_line': section_start,
            'end_line': section_end,
            'line_count': section_end - section_start
        }
    
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
            f.write(f"**Description:** {section_data['description']}\n")
            if 'content' in section_data and section_data['content']:
                f.write(f"**Start Line:** {section_data['content']['start_line']}\n")
                f.write(f"**End Line:** {section_data['content']['end_line']}\n")
                f.write(f"**Line Count:** {section_data['content']['line_count']}\n\n")
            f.write("## Content\n\n")
            
            if 'content' in section_data and section_data['content']:
                # Clean and format the content
                content_text = section_data['content']['text']
                # Remove excessive whitespace and format
                content_text = re.sub(r'\n\s*\n', '\n\n', content_text)
                content_text = re.sub(r'Format No\.- xxx.*?Page \d+ of \d+', '', content_text)
                f.write(content_text)
            
            # Add references to tables and images if they exist
            if section_data.get('tables'):
                f.write(f"\n\n## Tables\n\nThis section contains {len(section_data['tables'])} table(s). See `tables.json` for structured data.\n")
            
            # Note about images (placeholder since we don't have actual images)
            f.write(f"\n\n## Images\n\nImages referenced in this section would be stored in the `./images/` directory.\n")
        
        # Save tables if they exist
        if section_data.get('tables'):
            tables_file = section_dir / "tables.json"
            with open(tables_file, 'w', encoding='utf-8') as f:
                json.dump(section_data['tables'], f, indent=2, ensure_ascii=False)
        
        print(f"Saved section: {section_key}")
    
    def merge_sections(self, doc1_sections: Dict[str, Any], doc2_sections: Dict[str, Any]) -> Dict[str, Any]:
        """Merge sections from both documents, prioritizing completeness."""
        merged = {}
        
        # Start with all sections from both documents
        all_section_keys = set(doc1_sections.keys()) | set(doc2_sections.keys())
        
        for section_key in sorted(all_section_keys):
            if section_key in doc1_sections and section_key in doc2_sections:
                # Merge content from both documents
                merged_section = doc1_sections[section_key].copy()
                merged_section['source_doc'] = f"{doc1_sections[section_key]['source_doc']}, {doc2_sections[section_key]['source_doc']}"
                
                # Combine content
                if 'content' in doc2_sections[section_key]:
                    merged_section['content']['text'] += f"\n\n--- Content from {doc2_sections[section_key]['source_doc']} ---\n\n"
                    merged_section['content']['text'] += doc2_sections[section_key]['content']['text']
                
                # Combine tables
                if doc2_sections[section_key].get('tables'):
                    merged_section['tables'].extend(doc2_sections[section_key]['tables'])
                
                merged[section_key] = merged_section
            elif section_key in doc1_sections:
                merged[section_key] = doc1_sections[section_key]
            else:
                merged[section_key] = doc2_sections[section_key]
        
        return merged
    
    def create_summary(self, sections: Dict[str, Any]):
        """Create a summary of extracted sections."""
        summary_file = self.output_dir / "extraction_summary.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("# APQR Extraction Summary\n\n")
            f.write("## Document Sources\n")
            f.write("- **Document 1**: Detailed form-based APQR template (25 sections)\n")
            f.write("- **Document 2**: US FDA-aligned APQR template (16 sections)\n\n")
            f.write("## Extracted Sections\n\n")
            
            for section_key, section_data in sorted(sections.items()):
                f.write(f"### {section_key}\n")
                f.write(f"**Title:** {section_data['title']}\n\n")
                f.write(f"**Description:** {section_data['description']}\n\n")
                f.write(f"**Source:** {section_data['source_doc']}\n\n")
                if section_data.get('tables'):
                    f.write(f"**Tables:** {len(section_data['tables'])}\n\n")
                f.write("---\n\n")
            
            f.write(f"\n**Total Sections Extracted:** {len(sections)}\n")
            f.write(f"**Output Directory:** {self.output_dir}\n")
        
        print(f"Created extraction summary: {summary_file}")
    
    def process_documents(self, doc1_path: str, doc2_path: str):
        """Process both APQR documents."""
        print("Processing APQR documents...")
        self.create_folder_structure()
        
        # Process both documents
        print("Processing Document 1...")
        doc1_sections = self.process_document_1(doc1_path)
        
        print("Processing Document 2...")
        doc2_sections = self.process_document_2(doc2_path)
        
        # Merge sections
        print("Merging sections...")
        merged_sections = self.merge_sections(doc1_sections, doc2_sections)
        
        # Save all sections
        print("Saving sections...")
        for section_key, section_data in merged_sections.items():
            self.save_section_content(section_key, section_data)
        
        # Create summary
        self.create_summary(merged_sections)
        
        print(f"\nProcessing completed successfully!")
        print(f"Created {len(merged_sections)} sections in {self.output_dir}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Process text-based APQR documents')
    parser.add_argument('--doc1', default='/workspace/APQR_Document_1.txt', 
                       help='Path to first APQR document')
    parser.add_argument('--doc2', default='/workspace/APQR_Document_2.txt', 
                       help='Path to second APQR document')
    parser.add_argument('--output', '-o', default='APQR_Aspirin325mg', 
                       help='Output directory name')
    
    args = parser.parse_args()
    
    # Verify documents exist
    for doc_path in [args.doc1, args.doc2]:
        if not os.path.exists(doc_path):
            print(f"Error: Document not found: {doc_path}")
            return 1
    
    # Process documents
    processor = TextAPQRProcessor(args.output)
    processor.process_documents(args.doc1, args.doc2)
    
    return 0


if __name__ == "__main__":
    exit(main())