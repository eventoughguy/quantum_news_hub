#!/usr/bin/env python3
"""
Quantum Supply Chain Ontology Manager
Easy-to-use interface for updating and querying the ontology
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

from quantum_supply_chain_ontology import QuantumSupplyChainOntology
from data_schema import (
    SupplyChainDataManager, CompanyType, QuantumModality,
    HardwareCompany, ComponentSupplier, SoftwareCompany
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class OntologyManager:
    """High-level manager for quantum supply chain ontology operations"""

    def __init__(self, ontology_path=None, data_path=None):
        self.ontology_path = Path(ontology_path) if ontology_path else Path("/home/liuyiwen/AI/AI Agent/quantum_news_agent/project/ontology")
        self.data_manager = SupplyChainDataManager(data_path or str(self.ontology_path / "supply_chain_data.json"))
        self.ontology = None

    def load_or_create_ontology(self):
        """Load existing ontology or create new one"""
        try:
            self.ontology = QuantumSupplyChainOntology(self.ontology_path)
            self.ontology.build_ontology()
            logging.info("✅ Ontology loaded/created successfully")
        except Exception as e:
            logging.error(f"Error loading ontology: {e}")
            raise

    def add_modality_companies(self, modality: str, companies_file: str):
        """
        Add companies for a specific quantum modality from JSON file

        Args:
            modality: Quantum modality name (e.g., "TrappedIon", "PhotonicQuantum")
            companies_file: Path to JSON file containing company data
        """
        try:
            with open(companies_file, 'r') as f:
                companies_data = json.load(f)

            if not self.ontology:
                self.load_or_create_ontology()

            # Add companies to ontology
            self.ontology.add_new_modality_data(modality, companies_data.get('companies', []))

            # Save updated ontology
            self.ontology.save_ontology()

            logging.info(f"✅ Added {len(companies_data.get('companies', []))} companies for {modality} modality")

        except Exception as e:
            logging.error(f"Error adding modality companies: {e}")
            raise

    def update_superconducting_data(self, new_companies: List[Dict]):
        """Update superconducting modality with new companies"""
        return self.add_modality_companies("SuperconductingQubit", {"companies": new_companies})

    def add_individual_company(self, company_data: Dict):
        """Add a single company to the ontology"""
        if not self.ontology:
            self.load_or_create_ontology()

        # Determine company type and create appropriate object
        company_type = company_data.get('company_type', 'hardware')

        if company_type == 'hardware':
            company = HardwareCompany(**company_data)
        elif company_type == 'supplier':
            company = ComponentSupplier(**company_data)
        elif company_type == 'software':
            company = SoftwareCompany(**company_data)

        # Add to data manager
        self.data_manager.add_company(company)

        # Add to ontology
        modalities = company_data.get('modalities', ['SuperconductingQubit'])
        for modality in modalities:
            self.ontology.add_new_modality_data(modality, [company_data])

        # Save updates
        self.ontology.save_ontology()
        logging.info(f"✅ Added company: {company_data.get('name')}")

    def query_supply_chain(self, query_type: str, **kwargs) -> List[Dict]:
        """
        Query the supply chain data

        Args:
            query_type: Type of query ('suppliers_for_client', 'companies_by_modality', 'all_companies')
            **kwargs: Query parameters
        """
        if query_type == 'suppliers_for_client':
            client_name = kwargs.get('client_name')
            return self.data_manager.get_suppliers_for_client(client_name)

        elif query_type == 'companies_by_modality':
            modality = kwargs.get('modality')
            if isinstance(modality, str):
                modality = QuantumModality(modality)
            return self.data_manager.get_companies_by_modality(modality)

        elif query_type == 'all_companies':
            return self.data_manager.data.get('companies', [])

        else:
            raise ValueError(f"Unknown query type: {query_type}")

    def export_modality_data(self, modality: str, output_file: str):
        """Export data for specific modality to JSON file"""
        try:
            modality_enum = QuantumModality(modality)
            data = self.data_manager.export_for_ontology(modality_enum)

            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)

            logging.info(f"✅ Exported {modality} data to {output_file}")
        except Exception as e:
            logging.error(f"Error exporting data: {e}")

    def get_ontology_stats(self) -> Dict:
        """Get statistics about the current ontology"""
        if not self.ontology:
            self.load_or_create_ontology()

        ontology_stats = self.ontology.get_statistics()
        data_stats = {
            'companies_in_data': len(self.data_manager.data.get('companies', [])),
            'partnerships': len(self.data_manager.data.get('partnerships', [])),
            'products': len(self.data_manager.data.get('products', []))
        }

        return {**ontology_stats, **data_stats}

    def validate_and_clean_data(self):
        """Validate and clean the data"""
        companies = self.data_manager.data.get('companies', [])
        cleaned = 0

        for company in companies:
            # Clean empty fields
            for key in list(company.keys()):
                if company[key] in [None, '', 'nan', 'NaN']:
                    del company[key]
                    cleaned += 1

            # Ensure required fields
            if 'name' not in company:
                company['name'] = 'Unknown Company'
            if 'company_type' not in company:
                company['company_type'] = 'hardware'

        if cleaned > 0:
            self.data_manager.save_data()
            logging.info(f"✅ Cleaned {cleaned} empty fields")

    def create_modality_template(self, modality: str, output_file: str):
        """Create a template file for adding companies to specific modality"""
        template = {
            "modality": modality,
            "description": f"Template for adding companies to {modality} quantum computing",
            "companies": [
                {
                    "name": "Example Company Name",
                    "type": "hardware",  # or "supplier", "software"
                    "description": "Brief description of the company",
                    "country": "USA",
                    "website": "https://example.com",
                    "founded_year": 2020,
                    "modalities": [modality] if modality else ["SuperconductingQubit"],
                    "notes": "Additional information",
                    "clients": ["Client1", "Client2"],  # for suppliers
                    "component_types": ["superconducting_wire"],  # for suppliers
                    "products": ["SDK Name"],  # for software companies
                    "qubit_count": 50,  # for hardware companies
                    "platforms": ["Platform Name"]  # for hardware companies
                }
            ],
            "instructions": [
                "1. Replace example data with real company information",
                "2. Remove fields that don't apply to your company type",
                "3. Add multiple companies by copying the company object",
                "4. Save file and use: manager.add_modality_companies(modality, file_path)"
            ]
        }

        with open(output_file, 'w') as f:
            json.dump(template, f, indent=2)

        print(f"✅ Template created: {output_file}")
        print("Edit the template file and use:")
        print(f"  manager.add_modality_companies('{modality}', '{output_file}')")

def main():
    """Main function for command-line usage"""
    import argparse

    parser = argparse.ArgumentParser(description="Quantum Supply Chain Ontology Manager")
    parser.add_argument("--action", choices=[
        'create', 'stats', 'query', 'template', 'add-company', 'clean'
    ], required=True, help="Action to perform")

    parser.add_argument("--modality", help="Quantum modality (SuperconductingQubit, TrappedIon, etc.)")
    parser.add_argument("--file", help="Input/output file path")
    parser.add_argument("--client", help="Client name for supplier queries")
    parser.add_argument("--company-name", help="Company name")
    parser.add_argument("--company-type", choices=['hardware', 'supplier', 'software'], help="Company type")

    args = parser.parse_args()

    manager = OntologyManager()

    try:
        if args.action == 'create':
            manager.load_or_create_ontology()
            print("✅ Ontology created/updated successfully")

        elif args.action == 'stats':
            stats = manager.get_ontology_stats()
            print("\n📊 ONTOLOGY STATISTICS")
            print("=" * 50)
            for key, value in stats.items():
                print(f"{key.replace('_', ' ').title()}: {value}")

        elif args.action == 'template':
            if not args.modality or not args.file:
                print("Error: --modality and --file required for template creation")
                return
            manager.create_modality_template(args.modality, args.file)

        elif args.action == 'query':
            if args.client:
                results = manager.query_supply_chain('suppliers_for_client', client_name=args.client)
                print(f"\n🔍 Suppliers for {args.client}:")
                for result in results:
                    print(f"  - {result.get('name')} ({result.get('country', 'Unknown')})")

        elif args.action == 'clean':
            manager.validate_and_clean_data()

        elif args.action == 'add-company':
            print("Interactive company addition not implemented in CLI.")
            print("Use the Python API: manager.add_individual_company(company_data)")

    except Exception as e:
        print(f"❌ Error: {e}")
        logging.error(f"CLI Error: {e}")

if __name__ == "__main__":
    main()