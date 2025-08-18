#!/usr/bin/env python3
"""
SOP API Call Generator Script
Generates API calls for all Aspirin Tablet Manufacturing SOPs
Author: AI Assistant
Date: 2024
"""

import requests
import json
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sop_api_calls.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class SOP:
    """Data class to represent an SOP"""
    code: str
    title: str
    category: str
    description: str = ""

class SOPAPIGenerator:
    """Main class for generating SOP API calls"""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 30):
        """
        Initialize the SOP API Generator
        
        Args:
            base_url: Base URL for the API
            api_key: API key for authentication (if required)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        
        # Set up authentication headers if API key is provided
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })
    
    def get_all_sops(self) -> List[SOP]:
        """
        Returns all SOPs organized by category
        """
        sops = [
            # Category 1: Quality Assurance (QA) SOPs
            SOP("SOP-QA-001", "SOP for SOPs", "Quality Assurance", "The procedure for writing, reviewing, approving, and distributing all other SOPs"),
            SOP("SOP-QA-002", "Employee Training and Qualification", "Quality Assurance", "Procedures for training and qualifying employees"),
            SOP("SOP-QA-003", "Document and Data Control", "Quality Assurance", "Control of documents and data management"),
            SOP("SOP-QA-004", "Change Control Management", "Quality Assurance", "Managing changes to processes and procedures"),
            SOP("SOP-QA-005", "Deviation Management and Reporting", "Quality Assurance", "Handling and reporting deviations"),
            SOP("SOP-QA-006", "Out of Specification (OOS) Investigations", "Quality Assurance", "Investigating out of specification results"),
            SOP("SOP-QA-007", "Corrective and Preventive Action (CAPA) System", "Quality Assurance", "CAPA system management"),
            SOP("SOP-QA-008", "Annual Product Quality Review (APQR) Compilation", "Quality Assurance", "Annual quality review procedures"),
            SOP("SOP-QA-009", "Vendor Qualification and Management", "Quality Assurance", "Qualifying and managing vendors"),
            SOP("SOP-QA-010", "Internal Audits / Self-Inspection", "Quality Assurance", "Internal audit procedures"),
            SOP("SOP-QA-011", "Handling of Product Quality Complaints", "Quality Assurance", "Managing product quality complaints"),
            SOP("SOP-QA-012", "Handling of Product Recalls", "Quality Assurance", "Product recall procedures"),
            SOP("SOP-QA-013", "Batch Record Review and Final Batch Release", "Quality Assurance", "Batch review and release procedures"),
            SOP("SOP-QA-014", "Line Clearance Procedure", "Quality Assurance", "Production line clearance procedures"),
            
            # Category 2: Materials Management (Warehouse) SOPs
            SOP("SOP-WH-001", "Receipt of Raw Materials and Packaging Components", "Materials Management", "Receiving raw materials and packaging"),
            SOP("SOP-WH-002", "Storage and Handling of Quarantined Materials", "Materials Management", "Managing quarantined materials"),
            SOP("SOP-WH-003", "Storage and Handling of Approved Materials", "Materials Management", "Managing approved materials"),
            SOP("SOP-WH-004", "Storage and Handling of Rejected Materials", "Materials Management", "Managing rejected materials"),
            SOP("SOP-WH-005", "Dispensing of Raw Materials for Production", "Materials Management", "Dispensing materials for production"),
            SOP("SOP-WH-006", "Inventory Management and Stock Control (FIFO/FEFO)", "Materials Management", "Inventory and stock control"),
            SOP("SOP-WH-007", "Control of Printed Packaging Materials", "Materials Management", "Managing printed packaging materials"),
            SOP("SOP-WH-008", "Shipping of Finished Goods", "Materials Management", "Shipping finished products"),
            SOP("SOP-WH-009", "Pest Control in the Warehouse", "Materials Management", "Warehouse pest control procedures"),
            
            # Category 3: Quality Control (QC) Laboratory SOPs
            SOP("SOP-QC-001", "Sampling of Raw Materials", "Quality Control", "Raw material sampling procedures"),
            SOP("SOP-QC-002", "Sampling of In-Process Materials", "Quality Control", "In-process material sampling"),
            SOP("SOP-QC-003", "Sampling of Finished Products", "Quality Control", "Finished product sampling"),
            SOP("SOP-QC-004", "General Laboratory Practices and Safety", "Quality Control", "Laboratory safety and practices"),
            SOP("SOP-QC-005", "Operation, Calibration, and Maintenance of the HPLC System", "Quality Control", "HPLC system management"),
            SOP("SOP-QC-006", "Operation, Calibration, and Maintenance of the IR Spectrometer", "Quality Control", "IR spectrometer management"),
            SOP("SOP-QC-007", "Operation, Calibration, and Maintenance of the Dissolution Test Apparatus", "Quality Control", "Dissolution test apparatus management"),
            SOP("SOP-QC-008", "Operation, Calibration, and Maintenance of Analytical Balances", "Quality Control", "Analytical balance management"),
            SOP("SOP-QC-009", "Handling of Laboratory Reagents and Reference Standards", "Quality Control", "Laboratory reagent management"),
            SOP("SOP-QC-010", "Stability Study Program Management", "Quality Control", "Stability study management"),
            SOP("SOP-QC-011", "Analytical Method for Assay and Impurities of Aspirin Tablets", "Quality Control", "Aspirin tablet assay methods"),
            SOP("SOP-QC-012", "Analytical Method for Dissolution of Aspirin Tablets", "Quality Control", "Aspirin tablet dissolution methods"),
            SOP("SOP-QC-013", "Microbiological Testing of Non-Sterile Products", "Quality Control", "Microbiological testing procedures"),
            
            # Category 4: Production / Manufacturing SOPs
            SOP("SOP-PROD-001", "Gowning and Hygiene in Manufacturing Areas", "Production", "Manufacturing hygiene procedures"),
            SOP("SOP-PROD-002", "Operation, Cleaning, and Maintenance of the Mechanical Sifter", "Production", "Mechanical sifter procedures"),
            SOP("SOP-PROD-003", "Operation, Cleaning, and Maintenance of the Blender (e.g., V-Blender)", "Production", "Blender operation procedures"),
            SOP("SOP-PROD-004", "Operation, Cleaning, and Maintenance of the Granulator (e.g., RMG)", "Production", "Granulator operation procedures"),
            SOP("SOP-PROD-005", "Operation, Cleaning, and Maintenance of the Fluid Bed Dryer (FBD)", "Production", "Fluid bed dryer procedures"),
            SOP("SOP-PROD-006", "Operation, Cleaning, and Maintenance of the Tablet Compression Machine", "Production", "Tablet compression procedures"),
            SOP("SOP-PROD-007", "In-Process Quality Control (IPQC) Checks for Tablet Compression", "Production", "IPQC for tablet compression"),
            SOP("SOP-PROD-008", "Handling of In-Process Materials and Batch Segregation", "Production", "In-process material handling"),
            SOP("SOP-PROD-009", "Process Yield Reconciliation", "Production", "Process yield reconciliation procedures"),
            
            # Category 5: Packaging SOPs
            SOP("SOP-PKG-001", "Operation, Cleaning, and Maintenance of the Blister Packaging Machine", "Packaging", "Blister packaging machine procedures"),
            SOP("SOP-PKG-002", "Operation, Cleaning, and Maintenance of the Bottle Filling and Capping Line", "Packaging", "Bottle filling and capping procedures"),
            SOP("SOP-PKG-003", "Control and Reconciliation of Printed Labels and Cartons", "Packaging", "Label and carton control"),
            SOP("SOP-PKG-004", "In-Process Quality Control (IPQC) Checks for Packaging", "Packaging", "IPQC for packaging operations"),
            
            # Category 6: Engineering & Maintenance SOPs
            SOP("SOP-ENG-001", "Preventive Maintenance Program", "Engineering", "Preventive maintenance procedures"),
            SOP("SOP-ENG-002", "Calibration Program for Instruments and Gauges", "Engineering", "Calibration program management"),
            SOP("SOP-ENG-003", "Operation and Maintenance of the HVAC System for Manufacturing Areas", "Engineering", "HVAC system management"),
            SOP("SOP-ENG-004", "Operation and Maintenance of the Purified Water System", "Engineering", "Purified water system management"),
            SOP("SOP-ENG-005", "Equipment Breakdown and Repair Procedure", "Engineering", "Equipment repair procedures"),
            
            # Category 7: Health, Safety & Environment (HSE) SOPs
            SOP("SOP-HSE-001", "Handling of Hazardous Materials and Waste Disposal", "Health Safety Environment", "Hazardous material handling"),
            SOP("SOP-HSE-002", "Emergency Response and Evacuation Procedure", "Health Safety Environment", "Emergency response procedures"),
        ]
        
        return sops
    
    def create_sop_payload(self, sop: SOP, additional_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create API payload for a single SOP
        
        Args:
            sop: SOP object
            additional_data: Additional data to include in payload
            
        Returns:
            Dictionary containing the API payload
        """
        payload = {
            "sop_code": sop.code,
            "title": sop.title,
            "category": sop.category,
            "description": sop.description,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "active"
        }
        
        if additional_data:
            payload.update(additional_data)
            
        return payload
    
    def make_single_api_call(self, sop: SOP, endpoint: str = "/api/sops", 
                           method: str = "POST", additional_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make a single API call for one SOP
        
        Args:
            sop: SOP object
            endpoint: API endpoint
            method: HTTP method
            additional_data: Additional data for the payload
            
        Returns:
            API response data
        """
        url = f"{self.base_url}{endpoint}"
        payload = self.create_sop_payload(sop, additional_data)
        
        try:
            logger.info(f"Making {method} request for {sop.code}: {sop.title}")
            
            if method.upper() == "POST":
                response = self.session.post(url, json=payload, timeout=self.timeout)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=payload, timeout=self.timeout)
            elif method.upper() == "GET":
                response = self.session.get(f"{url}/{sop.code}", timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            result = {
                "sop_code": sop.code,
                "status": "success",
                "status_code": response.status_code,
                "response": response.json() if response.content else {}
            }
            
            logger.info(f"✅ Success: {sop.code} - Status: {response.status_code}")
            return result
            
        except requests.exceptions.RequestException as e:
            error_result = {
                "sop_code": sop.code,
                "status": "error",
                "error": str(e),
                "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            }
            logger.error(f"❌ Error: {sop.code} - {str(e)}")
            return error_result
    
    def process_all_sops_sequential(self, endpoint: str = "/api/sops", 
                                  method: str = "POST", 
                                  additional_data: Dict[str, Any] = None,
                                  delay_between_calls: float = 0.5) -> List[Dict[str, Any]]:
        """
        Process all SOPs sequentially (one by one)
        
        Args:
            endpoint: API endpoint
            method: HTTP method
            additional_data: Additional data for payloads
            delay_between_calls: Delay between API calls in seconds
            
        Returns:
            List of API response results
        """
        sops = self.get_all_sops()
        results = []
        
        logger.info(f"🚀 Starting sequential processing of {len(sops)} SOPs")
        
        for i, sop in enumerate(sops, 1):
            logger.info(f"Processing {i}/{len(sops)}: {sop.code}")
            result = self.make_single_api_call(sop, endpoint, method, additional_data)
            results.append(result)
            
            # Add delay between calls to avoid overwhelming the API
            if delay_between_calls > 0 and i < len(sops):
                time.sleep(delay_between_calls)
        
        return results
    
    def process_all_sops_parallel(self, endpoint: str = "/api/sops", 
                                method: str = "POST", 
                                additional_data: Dict[str, Any] = None,
                                max_workers: int = 5) -> List[Dict[str, Any]]:
        """
        Process all SOPs in parallel using ThreadPoolExecutor
        
        Args:
            endpoint: API endpoint
            method: HTTP method
            additional_data: Additional data for payloads
            max_workers: Maximum number of concurrent threads
            
        Returns:
            List of API response results
        """
        sops = self.get_all_sops()
        results = []
        
        logger.info(f"🚀 Starting parallel processing of {len(sops)} SOPs with {max_workers} workers")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_sop = {
                executor.submit(self.make_single_api_call, sop, endpoint, method, additional_data): sop 
                for sop in sops
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_sop):
                sop = future_to_sop[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as exc:
                    error_result = {
                        "sop_code": sop.code,
                        "status": "error",
                        "error": f"Thread execution error: {str(exc)}"
                    }
                    results.append(error_result)
                    logger.error(f"❌ Thread error for {sop.code}: {str(exc)}")
        
        return results
    
    def process_sops_by_category(self, category: str, endpoint: str = "/api/sops", 
                               method: str = "POST", 
                               additional_data: Dict[str, Any] = None,
                               parallel: bool = True) -> List[Dict[str, Any]]:
        """
        Process SOPs for a specific category only
        
        Args:
            category: Category to filter by
            endpoint: API endpoint
            method: HTTP method
            additional_data: Additional data for payloads
            parallel: Whether to process in parallel or sequential
            
        Returns:
            List of API response results for the category
        """
        all_sops = self.get_all_sops()
        category_sops = [sop for sop in all_sops if sop.category == category]
        
        if not category_sops:
            logger.warning(f"No SOPs found for category: {category}")
            return []
        
        logger.info(f"🎯 Processing {len(category_sops)} SOPs for category: {category}")
        
        if parallel:
            return self._process_sop_list_parallel(category_sops, endpoint, method, additional_data)
        else:
            return self._process_sop_list_sequential(category_sops, endpoint, method, additional_data)
    
    def _process_sop_list_sequential(self, sops: List[SOP], endpoint: str, 
                                   method: str, additional_data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Helper method to process a list of SOPs sequentially"""
        results = []
        for sop in sops:
            result = self.make_single_api_call(sop, endpoint, method, additional_data)
            results.append(result)
        return results
    
    def _process_sop_list_parallel(self, sops: List[SOP], endpoint: str, 
                                 method: str, additional_data: Dict[str, Any] = None, 
                                 max_workers: int = 5) -> List[Dict[str, Any]]:
        """Helper method to process a list of SOPs in parallel"""
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_sop = {
                executor.submit(self.make_single_api_call, sop, endpoint, method, additional_data): sop 
                for sop in sops
            }
            
            for future in as_completed(future_to_sop):
                result = future.result()
                results.append(result)
        return results
    
    def save_results_to_file(self, results: List[Dict[str, Any]], filename: str = "sop_api_results.json"):
        """
        Save API results to a JSON file
        
        Args:
            results: List of API results
            filename: Output filename
        """
        output_path = Path(filename)
        
        # Create summary statistics
        total_sops = len(results)
        successful = len([r for r in results if r.get('status') == 'success'])
        failed = total_sops - successful
        
        output_data = {
            "summary": {
                "total_sops": total_sops,
                "successful": successful,
                "failed": failed,
                "success_rate": f"{(successful/total_sops)*100:.1f}%" if total_sops > 0 else "0%",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            "results": results
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"📄 Results saved to: {output_path.absolute()}")
            logger.info(f"📊 Summary: {successful}/{total_sops} successful ({(successful/total_sops)*100:.1f}%)")
            
        except Exception as e:
            logger.error(f"❌ Failed to save results to file: {str(e)}")
    
    def get_categories(self) -> List[str]:
        """Get list of all available categories"""
        sops = self.get_all_sops()
        categories = list(set(sop.category for sop in sops))
        return sorted(categories)
    
    def print_sop_summary(self):
        """Print a summary of all SOPs organized by category"""
        sops = self.get_all_sops()
        categories = self.get_categories()
        
        print("\n" + "="*80)
        print("📋 ASPIRIN TABLET MANUFACTURING SOPs SUMMARY")
        print("="*80)
        
        for category in categories:
            category_sops = [sop for sop in sops if sop.category == category]
            print(f"\n🏷️  {category.upper()} ({len(category_sops)} SOPs)")
            print("-" * 60)
            
            for sop in category_sops:
                print(f"   {sop.code}: {sop.title}")
        
        print(f"\n📈 TOTAL: {len(sops)} SOPs across {len(categories)} categories")
        print("="*80)


def main():
    """
    Main function demonstrating usage of the SOP API Generator
    """
    print("🏭 SOP API Generator for Aspirin Tablet Manufacturing")
    print("=" * 60)
    
    # Configuration - Update these values for your actual API
    BASE_URL = "https://your-api-endpoint.com"  # Replace with your actual API URL
    API_KEY = "your-api-key-here"  # Replace with your actual API key (if needed)
    
    # Initialize the generator
    generator = SOPAPIGenerator(
        base_url=BASE_URL,
        api_key=API_KEY,  # Set to None if no authentication required
        timeout=30
    )
    
    # Show SOP summary
    generator.print_sop_summary()
    
    # Example usage options:
    print("\n🚀 Choose processing method:")
    print("1. Process ALL SOPs sequentially")
    print("2. Process ALL SOPs in parallel (faster)")
    print("3. Process specific category only")
    print("4. Just show summary (no API calls)")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        print("\n🔄 Processing all SOPs sequentially...")
        results = generator.process_all_sops_sequential(
            endpoint="/api/sops",
            method="POST",
            delay_between_calls=0.5
        )
        generator.save_results_to_file(results, "sop_results_sequential.json")
        
    elif choice == "2":
        print("\n⚡ Processing all SOPs in parallel...")
        results = generator.process_all_sops_parallel(
            endpoint="/api/sops",
            method="POST",
            max_workers=5
        )
        generator.save_results_to_file(results, "sop_results_parallel.json")
        
    elif choice == "3":
        categories = generator.get_categories()
        print(f"\n📂 Available categories:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        try:
            cat_choice = int(input(f"\nEnter category number (1-{len(categories)}): ")) - 1
            if 0 <= cat_choice < len(categories):
                selected_category = categories[cat_choice]
                print(f"\n🎯 Processing category: {selected_category}")
                results = generator.process_sops_by_category(
                    category=selected_category,
                    endpoint="/api/sops",
                    method="POST",
                    parallel=True
                )
                generator.save_results_to_file(results, f"sop_results_{selected_category.lower().replace(' ', '_')}.json")
            else:
                print("❌ Invalid category selection")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            
    elif choice == "4":
        print("\n✅ Summary displayed above. No API calls made.")
        
    else:
        print("❌ Invalid choice. Please run the script again.")
    
    print("\n🎉 Script execution completed!")


if __name__ == "__main__":
    main()