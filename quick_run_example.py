#!/usr/bin/env python3
"""
Quick Run Example - One Button SOP API Execution
This is a simplified version for quick execution
"""

from sop_api_generator import SOPAPIGenerator
import json

def one_button_sop_execution():
    """
    One-button execution for all SOP API calls
    Update the configuration below and run this function
    """
    
    # 🔧 CONFIGURATION - UPDATE THESE VALUES
    BASE_URL = "https://your-api-endpoint.com"  # Your API URL
    API_KEY = None  # Your API key (or None if not needed)
    ENDPOINT = "/api/sops"  # Your API endpoint
    METHOD = "POST"  # HTTP method
    USE_PARALLEL = True  # True for parallel processing, False for sequential
    
    print("🏭 Starting One-Button SOP API Execution")
    print("=" * 50)
    
    try:
        # Initialize the generator
        generator = SOPAPIGenerator(
            base_url=BASE_URL,
            api_key=API_KEY,
            timeout=30
        )
        
        # Show summary
        print(f"📊 Total SOPs to process: {len(generator.get_all_sops())}")
        print(f"🔄 Processing method: {'Parallel' if USE_PARALLEL else 'Sequential'}")
        print(f"🎯 Target endpoint: {BASE_URL}{ENDPOINT}")
        print("-" * 50)
        
        # Process all SOPs
        if USE_PARALLEL:
            print("⚡ Processing all SOPs in parallel...")
            results = generator.process_all_sops_parallel(
                endpoint=ENDPOINT,
                method=METHOD,
                max_workers=5
            )
        else:
            print("🔄 Processing all SOPs sequentially...")
            results = generator.process_all_sops_sequential(
                endpoint=ENDPOINT,
                method=METHOD,
                delay_between_calls=0.5
            )
        
        # Save results
        generator.save_results_to_file(results, "one_button_sop_results.json")
        
        # Print summary
        successful = len([r for r in results if r.get('status') == 'success'])
        failed = len(results) - successful
        
        print("\n" + "=" * 50)
        print("🎉 EXECUTION COMPLETED!")
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {(successful/len(results))*100:.1f}%")
        print("📄 Results saved to: one_button_sop_results.json")
        print("=" * 50)
        
        return results
        
    except Exception as e:
        print(f"❌ Error during execution: {str(e)}")
        return None

def process_specific_categories():
    """
    Process specific categories only
    """
    # Categories to process (modify as needed)
    CATEGORIES_TO_PROCESS = [
        "Quality Assurance",
        "Production"
    ]
    
    BASE_URL = "https://your-api-endpoint.com"
    API_KEY = None
    
    generator = SOPAPIGenerator(base_url=BASE_URL, api_key=API_KEY)
    
    all_results = []
    
    for category in CATEGORIES_TO_PROCESS:
        print(f"🎯 Processing category: {category}")
        results = generator.process_sops_by_category(
            category=category,
            parallel=True
        )
        all_results.extend(results)
    
    # Save combined results
    generator.save_results_to_file(all_results, "category_specific_results.json")
    return all_results

if __name__ == "__main__":
    print("🚀 SOP API Quick Execution")
    print("Choose execution mode:")
    print("1. Process ALL SOPs (one button)")
    print("2. Process specific categories only")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        one_button_sop_execution()
    elif choice == "2":
        process_specific_categories()
    else:
        print("Invalid choice. Running default one-button execution...")
        one_button_sop_execution()