# APQR Document Extractor

This tool extracts, organizes, and structures APQR (Annual Product Quality Review) Word documents for Aspirin Tablets 325 mg.

## Features

- **Document Parsing**: Extracts text, tables, and images from Word documents (.docx format)
- **Section Organization**: Automatically identifies and organizes content into numbered sections
- **Structured Output**: Creates organized folder structure with standardized file formats
- **Traceability**: Maintains document source and page references for all extracted content
- **Multi-document Support**: Can process multiple APQR documents simultaneously

## Installation

1. Install required dependencies:
   ```bash
   pip install -r apqr_requirements.txt
   ```

## Usage

### Basic Usage
```bash
python apqr_extractor.py document1.docx document2.docx
```

### Custom Output Directory
```bash
python apqr_extractor.py document1.docx document2.docx --output MyCustomAPQR
```

## Output Structure

The tool creates a structured folder system:

```
APQR_Aspirin325mg/
├── extraction_summary.md
├── 01_Product_Details/
│   ├── text.md
│   ├── tables.json
│   └── images/
├── 02_Batch_Summary/
│   ├── text.md
│   ├── tables.json
│   └── images/
├── 03_Yield_Reconciliation/
│   ├── text.md
│   ├── tables.json
│   └── images/
└── ... (additional sections)
```

### File Formats

- **text.md**: Contains all extracted text with document source and page references
- **tables.json**: Structured JSON format of all tables found in the section
- **images/**: Folder containing extracted images (PNG/JPG format preserved)

## Supported APQR Sections

The tool automatically recognizes common APQR sections including:

1. Product Details
2. Batch Summary
3. Yield Reconciliation
4. Deviations
5. Stability
6. Raw Materials
7. Manufacturing Process
8. In-Process Controls
9. Finished Product Testing
10. Packaging Controls
11. Quality Control Data
12. Complaints
13. Returns
14. Change Controls
15. Corrective Actions
16. Preventive Actions
17. Risk Assessment
18. Trend Analysis
19. Conclusions
20. Recommendations
21. Appendix
22. References

## Traceability Features

Each extracted section includes:
- Source document identification
- Section number and title
- Paragraph/page references
- Original formatting preservation

## Example Output

### text.md Structure
```markdown
# Product Details

**Source Document:** Doc1
**Section Number:** 1
**Start Paragraph:** 5

## Content

Product Name: Aspirin Tablets 325 mg
Product Codes: ASP32501, ASP32502, ASP32503
...
```

### tables.json Structure
```json
[
  {
    "table_index": 0,
    "data": [
      ["Batch Number", "Manufacturing Date", "Expiry Date"],
      ["ASP001", "2024-01-15", "2026-01-15"],
      ["ASP002", "2024-01-16", "2026-01-16"]
    ],
    "source_doc": "Doc1"
  }
]
```

## Error Handling

The tool includes robust error handling for:
- Missing or corrupted Word documents
- Unsupported file formats
- Permission issues
- Memory constraints for large documents

## Customization

The section patterns can be extended by modifying the `section_patterns` list in the `APQRExtractor` class to accommodate specific APQR template variations.