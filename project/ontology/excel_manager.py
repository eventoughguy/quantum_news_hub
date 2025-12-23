#!/usr/bin/env python3
"""
Excel-based Supply Chain Data Manager
Allows users to update supply chain information via Excel spreadsheets
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from quantum_supply_chain_ontology import QuantumSupplyChainOntology

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ExcelSupplyChainManager:
    """Manager for Excel-based supply chain data updates"""

    def __init__(self, base_path=None):
        self.base_path = Path(base_path) if base_path else Path("/home/liuyiwen/AI/AI Agent/quantum_news_agent/project/ontology")
        self.templates_path = self.base_path / "excel_templates"
        self.templates_path.mkdir(exist_ok=True)

    def create_excel_templates(self):
        """Create Excel templates for different quantum modalities"""

        # Template for Superconducting companies (based on existing data)
        superconducting_template = {
            'Hardware_Companies': pd.DataFrame({
                'Company_Name': ['IBM Quantum', 'Google Quantum AI', 'Rigetti Computing', '[Add New Company]'],
                'Country': ['USA', 'USA', 'USA', ''],
                'Modality': ['SuperconductingQubit', 'SuperconductingQubit', 'SuperconductingQubit', 'SuperconductingQubit'],
                'Qubit_Count': [1000, 70, 80, ''],
                'Cloud_Service': ['Yes', 'Yes', 'Yes', ''],
                'Platform_Name': ['IBM Quantum Network', 'Google Quantum AI', 'Quantum Cloud Services', ''],
                'Website': ['https://quantum.ibm.com', 'https://quantumai.google', 'https://rigetti.com', ''],
                'Founded_Year': [1911, 1998, 2013, ''],
                'Description': ['Leading quantum computing platform', 'Quantum AI research and platforms', 'Full-stack quantum computing', ''],
                'Notes': ['', '', '', '']
            }),

            'Component_Suppliers': pd.DataFrame({
                'Supplier_Name': ['Super Conductor Materials Inc.', 'Sumitomo Electric Industries', 'SuperPower Inc.', '[Add New Supplier]'],
                'Country': ['USA', 'Japan', 'USA', ''],
                'Component_Types': ['Sputtering targets, thin-film superconductors', 'HTS wire', 'HTS tape, high-field magnets', ''],
                'Materials_Supplied': ['NbTi, Nb₃Sn, superconducting films', 'HTS wire, Nb₃Sn', 'YBCO tape, superconducting wire', ''],
                'Known_Clients': ['IBM, Google, Rigetti', 'Pasqal, Japanese labs', 'Tokamak Energy, DOE labs', ''],
                'Applications': ['Quantum chips, thin films', 'Quantum logistics, magnets', 'High-field systems, cryogenics', ''],
                'Website': ['https://scmat.com', 'https://global-sei.com', 'https://superpower-inc.com', ''],
                'Technical_Specs': ['Sputtering targets for qubits', 'HTS wire optimization', 'High current capacity', ''],
                'Notes': ['Primary supplier for IBM/Google', 'Partnership with Pasqal', '$80M DOE support', '']
            }),

            'Software_Companies': pd.DataFrame({
                'Software_Name': ['Qiskit', 'Cirq', 'Forest SDK', '[Add New SDK]'],
                'Company': ['IBM', 'Google', 'Rigetti', ''],
                'Type': ['SDK', 'SDK', 'SDK', 'SDK/Platform/Framework'],
                'Programming_Languages': ['Python', 'Python', 'Python', ''],
                'Supported_Hardware': ['IBM Quantum', 'Google quantum processors', 'Rigetti systems', ''],
                'License': ['Open Source', 'Open Source', 'Open Source', ''],
                'Website': ['https://qiskit.org', 'https://quantumai.google/cirq', 'https://rigetti.com/forest', ''],
                'Github': ['https://github.com/Qiskit', 'https://github.com/quantumlib/Cirq', 'https://github.com/rigetti', ''],
                'Description': ['Open-source quantum computing SDK', 'Python framework for quantum circuits', 'Quantum-classical hybrid computing', ''],
                'Notes': ['Most popular quantum SDK', 'Focus on Google hardware', 'Hybrid workflows', '']
            })
        }

        # Create Excel file for Superconducting modality
        superconducting_file = self.templates_path / "Superconducting_Supply_Chain.xlsx"
        with pd.ExcelWriter(superconducting_file, engine='openpyxl') as writer:
            for sheet_name, df in superconducting_template.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        logging.info(f"✅ Created Superconducting template: {superconducting_file}")

        # Template for Trapped Ion companies
        trapped_ion_template = {
            'Hardware_Companies': pd.DataFrame({
                'Company_Name': ['IonQ', 'Quantinuum (Honeywell)', 'Alpine Quantum Technologies', '[Add New Company]'],
                'Country': ['USA', 'USA', 'Austria', ''],
                'Modality': ['TrappedIon', 'TrappedIon', 'TrappedIon', 'TrappedIon'],
                'Qubit_Count': [64, 56, 24, ''],
                'Cloud_Service': ['Yes', 'Yes', 'No', ''],
                'Platform_Name': ['IonQ Aria', 'H-Series', 'AQT Platform', ''],
                'Website': ['https://ionq.com', 'https://quantinuum.com', 'https://aqt.eu', ''],
                'Founded_Year': [2015, 2021, 2018, ''],
                'Description': ['Trapped ion quantum computing leader', 'Quantum computing and software', 'Trapped ion quantum systems', ''],
                'Notes': ['Public company (NYSE: IONQ)', 'Honeywell + Cambridge Quantum merger', 'European trapped ion leader', '']
            }),

            'Component_Suppliers': pd.DataFrame({
                'Supplier_Name': ['[Add Ion Trap Suppliers]', '[Add Laser Suppliers]', '[Add Electronics Suppliers]'],
                'Country': ['', '', ''],
                'Component_Types': ['Ion traps, electrodes', 'Laser systems, optics', 'RF electronics, control systems'],
                'Materials_Supplied': ['Precision electrodes, vacuum chambers', 'Laser diodes, optical components', 'RF generators, control electronics'],
                'Known_Clients': ['', '', ''],
                'Applications': ['Ion trapping, qubit control', 'Qubit manipulation, readout', 'Quantum control systems'],
                'Website': ['', '', ''],
                'Technical_Specs': ['', '', ''],
                'Notes': ['Research needed', 'Research needed', 'Research needed']
            }),

            'Software_Companies': pd.DataFrame({
                'Software_Name': ['TKET', 'Lambeq', 'PyTket', '[Add New SDK]'],
                'Company': ['Quantinuum', 'Quantinuum', 'Quantinuum', ''],
                'Type': ['Compiler', 'Framework', 'SDK', ''],
                'Programming_Languages': ['Hardware-agnostic', 'Python', 'Python', ''],
                'Supported_Hardware': ['Multiple platforms', 'NLP applications', 'Quantinuum systems', ''],
                'License': ['Commercial', 'Open Source', 'Open Source', ''],
                'Website': ['https://tket.quantinuum.com', 'https://lambeq.com', 'https://pytket.com', ''],
                'Github': ['', 'https://github.com/CQCL/lambeq', 'https://github.com/CQCL/pytket', ''],
                'Description': ['Hardware-agnostic quantum compiler', 'Quantum NLP framework', 'Python quantum development', ''],
                'Notes': ['Cross-platform optimization', 'Natural language processing', 'Quantinuum ecosystem', '']
            })
        }

        # Create Excel file for Trapped Ion modality
        trapped_ion_file = self.templates_path / "TrappedIon_Supply_Chain.xlsx"
        with pd.ExcelWriter(trapped_ion_file, engine='openpyxl') as writer:
            for sheet_name, df in trapped_ion_template.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        logging.info(f"✅ Created Trapped Ion template: {trapped_ion_file}")

        # Template for Photonic companies
        photonic_template = {
            'Hardware_Companies': pd.DataFrame({
                'Company_Name': ['Xanadu', 'PsiQuantum', 'Orca Computing', '[Add New Company]'],
                'Country': ['Canada', 'USA', 'UK', ''],
                'Modality': ['PhotonicQuantum', 'PhotonicQuantum', 'PhotonicQuantum', 'PhotonicQuantum'],
                'Qubit_Count': [216, 1000000, 8, ''],
                'Cloud_Service': ['Yes', 'No', 'Yes', ''],
                'Platform_Name': ['X-Series', 'Fault-tolerant system', 'PT-1', ''],
                'Website': ['https://xanadu.ai', 'https://psiquantum.com', 'https://orcacomputing.com', ''],
                'Founded_Year': [2016, 2016, 2019, ''],
                'Description': ['Photonic quantum computing', 'Million-qubit photonic computer', 'Quantum photonic processors', ''],
                'Notes': ['Continuous variable approach', 'Fault-tolerant focus', 'Near-term photonic systems', '']
            }),

            'Component_Suppliers': pd.DataFrame({
                'Supplier_Name': ['[Add Photonic Suppliers]', '[Add Laser Suppliers]', '[Add Detector Suppliers]'],
                'Country': ['', '', ''],
                'Component_Types': ['Photonic chips, waveguides', 'Laser sources', 'Single photon detectors'],
                'Materials_Supplied': ['Silicon photonics, integrated optics', 'Laser diodes, coherent sources', 'SNSPDs, avalanche photodiodes'],
                'Known_Clients': ['', '', ''],
                'Applications': ['Quantum photonic circuits', 'Photon generation', 'Quantum measurement'],
                'Website': ['', '', ''],
                'Technical_Specs': ['', '', ''],
                'Notes': ['Research needed', 'Research needed', 'Research needed']
            }),

            'Software_Companies': pd.DataFrame({
                'Software_Name': ['PennyLane', 'Strawberry Fields', 'Perceval', '[Add New SDK]'],
                'Company': ['Xanadu', 'Xanadu', 'Quandela', ''],
                'Type': ['Framework', 'SDK', 'SDK', ''],
                'Programming_Languages': ['Python', 'Python', 'Python', ''],
                'Supported_Hardware': ['Multiple platforms', 'Xanadu hardware', 'Photonic systems', ''],
                'License': ['Open Source', 'Open Source', 'Open Source', ''],
                'Website': ['https://pennylane.ai', 'https://strawberryfields.ai', 'https://perceval.quandela.net', ''],
                'Github': ['https://github.com/PennyLaneAI', 'https://github.com/XanaduAI', 'https://github.com/Quandela', ''],
                'Description': ['Quantum ML framework', 'Photonic quantum computing', 'Photonic quantum computing', ''],
                'Notes': ['Cross-platform ML focus', 'Continuous variable systems', 'French photonic company', '']
            })
        }

        # Create Excel file for Photonic modality
        photonic_file = self.templates_path / "Photonic_Supply_Chain.xlsx"
        with pd.ExcelWriter(photonic_file, engine='openpyxl') as writer:
            for sheet_name, df in photonic_template.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        logging.info(f"✅ Created Photonic template: {photonic_file}")

        # Create a generic template for new modalities
        generic_template = {
            'Hardware_Companies': pd.DataFrame({
                'Company_Name': ['[Company 1]', '[Company 2]', '[Add More]'],
                'Country': ['USA', 'Europe', ''],
                'Modality': ['[YourModalityHere]', '[YourModalityHere]', '[YourModalityHere]'],
                'Qubit_Count': ['', '', ''],
                'Cloud_Service': ['Yes/No', 'Yes/No', ''],
                'Platform_Name': ['', '', ''],
                'Website': ['', '', ''],
                'Founded_Year': ['', '', ''],
                'Description': ['', '', ''],
                'Notes': ['', '', '']
            }),

            'Component_Suppliers': pd.DataFrame({
                'Supplier_Name': ['[Supplier 1]', '[Supplier 2]', '[Add More]'],
                'Country': ['', '', ''],
                'Component_Types': ['[Component type]', '[Component type]', ''],
                'Materials_Supplied': ['[Materials]', '[Materials]', ''],
                'Known_Clients': ['[Client 1, Client 2]', '[Client 1, Client 2]', ''],
                'Applications': ['[Applications]', '[Applications]', ''],
                'Website': ['', '', ''],
                'Technical_Specs': ['[Specifications]', '[Specifications]', ''],
                'Notes': ['[Additional info]', '[Additional info]', '']
            }),

            'Software_Companies': pd.DataFrame({
                'Software_Name': ['[SDK/Platform 1]', '[SDK/Platform 2]', '[Add More]'],
                'Company': ['[Company]', '[Company]', ''],
                'Type': ['SDK/Platform/Framework', 'SDK/Platform/Framework', ''],
                'Programming_Languages': ['Python/C++/Other', 'Python/C++/Other', ''],
                'Supported_Hardware': ['[Hardware platforms]', '[Hardware platforms]', ''],
                'License': ['Open Source/Commercial', 'Open Source/Commercial', ''],
                'Website': ['', '', ''],
                'Github': ['', '', ''],
                'Description': ['[Description]', '[Description]', ''],
                'Notes': ['[Additional info]', '[Additional info]', '']
            })
        }

        # Create generic template
        generic_file = self.templates_path / "Generic_Modality_Template.xlsx"
        with pd.ExcelWriter(generic_file, engine='openpyxl') as writer:
            for sheet_name, df in generic_template.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        logging.info(f"✅ Created Generic template: {generic_file}")

        # Create instructions file
        self.create_instructions_file()

        return {
            'superconducting': superconducting_file,
            'trapped_ion': trapped_ion_file,
            'photonic': photonic_file,
            'generic': generic_file
        }

    def create_instructions_file(self):
        """Create instructions for using Excel templates"""
        instructions = """
# Excel Supply Chain Update Instructions

## 📝 How to Update Supply Chain Data

### 1. Choose Your Template
- `Superconducting_Supply_Chain.xlsx` - For superconducting quantum companies
- `TrappedIon_Supply_Chain.xlsx` - For trapped ion quantum companies
- `Photonic_Supply_Chain.xlsx` - For photonic quantum companies
- `Generic_Modality_Template.xlsx` - For new quantum modalities

### 2. Edit Excel Sheets

Each Excel file has 3 sheets:
- **Hardware_Companies**: Quantum hardware/platform companies
- **Component_Suppliers**: Companies supplying components/materials
- **Software_Companies**: SDK, framework, and software companies

### 3. Required Fields
- **Company_Name**: Full official company name
- **Country**: Country of primary operations
- **Modality**: Quantum computing approach (keep consistent)

### 4. Optional but Important Fields
- **Website**: Official website URL
- **Founded_Year**: Year company was founded
- **Description**: Brief company description
- **Notes**: Additional context or recent developments

### 5. Specific Fields by Type

#### Hardware Companies:
- **Qubit_Count**: Number of qubits in latest system
- **Cloud_Service**: "Yes" if offering cloud access
- **Platform_Name**: Name of quantum platform/system

#### Component Suppliers:
- **Component_Types**: Types of components supplied
- **Materials_Supplied**: Specific materials (e.g., "NbTi wire, Nb₃Sn")
- **Known_Clients**: List of known clients
- **Technical_Specs**: Key specifications

#### Software Companies:
- **Type**: SDK/Platform/Framework/Compiler
- **Programming_Languages**: Supported languages
- **Supported_Hardware**: Compatible hardware platforms
- **License**: Open Source/Commercial
- **Github**: GitHub repository URL

### 6. Data Quality Tips
- Use official company names
- Verify information from company websites
- Include source URLs when possible
- Use consistent formatting for modalities
- Add "[Research Needed]" if information is uncertain

### 7. Adding New Companies
- Add rows at the end of each sheet
- Copy formatting from existing rows
- Use "[Add New Company]" placeholder rows as templates

### 8. Loading Updates
After editing Excel files, run:
```python
from excel_manager import ExcelSupplyChainManager
manager = ExcelSupplyChainManager()
manager.sync_excel_to_ontology("Superconducting_Supply_Chain.xlsx", "SuperconductingQubit")
```

### 9. Common Modality Names
- SuperconductingQubit
- TrappedIon
- PhotonicQuantum
- NeutralAtom
- SpinQubit
- QuantumAnnealing
- TopologicalQubit

### 10. Research Sources
- Company websites and press releases
- Quantum computing industry reports
- Academic collaborations and papers
- LinkedIn company profiles
- Conference presentations (Q2B, APS)
- Patent databases
"""

        instructions_file = self.templates_path / "Excel_Update_Instructions.md"
        with open(instructions_file, 'w') as f:
            f.write(instructions)

        logging.info(f"✅ Created instructions: {instructions_file}")

    def sync_excel_to_ontology(self, excel_file: str, modality: str) -> Dict:
        """
        Sync Excel file data to ontology

        Args:
            excel_file: Path to Excel file (relative to templates_path)
            modality: Quantum modality name

        Returns:
            Dictionary with sync results
        """
        try:
            excel_path = self.templates_path / excel_file
            if not excel_path.exists():
                raise FileNotFoundError(f"Excel file not found: {excel_path}")

            # Read all sheets
            sheets = pd.read_excel(excel_path, sheet_name=None, engine='openpyxl')

            companies_data = []
            stats = {'hardware': 0, 'suppliers': 0, 'software': 0, 'total': 0}

            # Process Hardware Companies
            if 'Hardware_Companies' in sheets:
                hw_df = sheets['Hardware_Companies']
                for _, row in hw_df.iterrows():
                    company_name = str(row.get('Company_Name', '')).strip()
                    if company_name and not company_name.startswith('[') and company_name != 'nan':
                        company_data = self._process_hardware_company(row, modality)
                        companies_data.append(company_data)
                        stats['hardware'] += 1

            # Process Component Suppliers
            if 'Component_Suppliers' in sheets:
                supplier_df = sheets['Component_Suppliers']
                for _, row in supplier_df.iterrows():
                    supplier_name = str(row.get('Supplier_Name', '')).strip()
                    if supplier_name and not supplier_name.startswith('[') and supplier_name != 'nan':
                        supplier_data = self._process_component_supplier(row, modality)
                        companies_data.append(supplier_data)
                        stats['suppliers'] += 1

            # Process Software Companies
            if 'Software_Companies' in sheets:
                sw_df = sheets['Software_Companies']
                for _, row in sw_df.iterrows():
                    software_name = str(row.get('Software_Name', '')).strip()
                    if software_name and not software_name.startswith('[') and software_name != 'nan':
                        software_data = self._process_software_company(row, modality)
                        companies_data.append(software_data)
                        stats['software'] += 1

            stats['total'] = len(companies_data)

            # Update ontology if there's data
            if companies_data:
                ontology = QuantumSupplyChainOntology(self.base_path)
                ontology.build_ontology()
                ontology.add_new_modality_data(modality, companies_data)
                ontology.save_ontology()

                logging.info(f"✅ Synced {stats['total']} companies to ontology for {modality}")

            # Save processed data as JSON for backup
            backup_file = self.base_path / f"{modality}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(backup_file, 'w') as f:
                json.dump({
                    'modality': modality,
                    'companies': companies_data,
                    'stats': stats,
                    'sync_time': datetime.now().isoformat()
                }, f, indent=2, default=str)

            return {
                'success': True,
                'modality': modality,
                'stats': stats,
                'backup_file': str(backup_file)
            }

        except Exception as e:
            logging.error(f"Error syncing Excel to ontology: {e}")
            return {
                'success': False,
                'error': str(e),
                'modality': modality
            }

    def _process_hardware_company(self, row: pd.Series, modality: str) -> Dict:
        """Process hardware company row from Excel"""
        return {
            'name': str(row.get('Company_Name', '')).strip(),
            'type': 'hardware',
            'country': str(row.get('Country', '')).strip(),
            'modalities': [modality],
            'description': str(row.get('Description', '')).strip(),
            'website': str(row.get('Website', '')).strip(),
            'founded_year': self._safe_int(row.get('Founded_Year')),
            'qubit_count': self._safe_int(row.get('Qubit_Count')),
            'cloud_service': str(row.get('Cloud_Service', '')).strip().lower() == 'yes',
            'platforms': [str(row.get('Platform_Name', '')).strip()] if row.get('Platform_Name') else [],
            'notes': str(row.get('Notes', '')).strip(),
            'last_updated': datetime.now().isoformat(),
            'data_source': 'Excel update'
        }

    def _process_component_supplier(self, row: pd.Series, modality: str) -> Dict:
        """Process component supplier row from Excel"""
        return {
            'name': str(row.get('Supplier_Name', '')).strip(),
            'type': 'supplier',
            'country': str(row.get('Country', '')).strip(),
            'component_types': str(row.get('Component_Types', '')).strip(),
            'materials_supplied': str(row.get('Materials_Supplied', '')).strip(),
            'clients': [c.strip() for c in str(row.get('Known_Clients', '')).split(',') if c.strip()],
            'applications': str(row.get('Applications', '')).strip(),
            'website': str(row.get('Website', '')).strip(),
            'technical_specs': str(row.get('Technical_Specs', '')).strip(),
            'notes': str(row.get('Notes', '')).strip(),
            'last_updated': datetime.now().isoformat(),
            'data_source': 'Excel update'
        }

    def _process_software_company(self, row: pd.Series, modality: str) -> Dict:
        """Process software company row from Excel"""
        return {
            'name': str(row.get('Software_Name', '')).strip(),
            'type': 'software',
            'company': str(row.get('Company', '')).strip(),
            'product_type': str(row.get('Type', '')).strip(),
            'programming_languages': [l.strip() for l in str(row.get('Programming_Languages', '')).split(',') if l.strip()],
            'supported_hardware': [h.strip() for h in str(row.get('Supported_Hardware', '')).split(',') if h.strip()],
            'license': str(row.get('License', '')).strip(),
            'website': str(row.get('Website', '')).strip(),
            'github': str(row.get('Github', '')).strip(),
            'description': str(row.get('Description', '')).strip(),
            'notes': str(row.get('Notes', '')).strip(),
            'last_updated': datetime.now().isoformat(),
            'data_source': 'Excel update'
        }

    def _safe_int(self, value) -> Optional[int]:
        """Safely convert value to int"""
        try:
            if pd.isna(value) or value == '':
                return None
            return int(float(value))
        except (ValueError, TypeError):
            return None

    def validate_excel_file(self, excel_file: str) -> Dict:
        """Validate Excel file structure and data quality"""
        try:
            excel_path = self.templates_path / excel_file
            sheets = pd.read_excel(excel_path, sheet_name=None, engine='openpyxl')

            validation_results = {
                'valid': True,
                'warnings': [],
                'errors': [],
                'stats': {}
            }

            required_sheets = ['Hardware_Companies', 'Component_Suppliers', 'Software_Companies']

            # Check required sheets exist
            for sheet in required_sheets:
                if sheet not in sheets:
                    validation_results['errors'].append(f"Missing required sheet: {sheet}")
                    validation_results['valid'] = False

            # Validate each sheet
            for sheet_name, df in sheets.items():
                if sheet_name in required_sheets:
                    sheet_validation = self._validate_sheet(sheet_name, df)
                    validation_results['warnings'].extend(sheet_validation['warnings'])
                    validation_results['errors'].extend(sheet_validation['errors'])
                    validation_results['stats'][sheet_name] = sheet_validation['stats']

                    if sheet_validation['errors']:
                        validation_results['valid'] = False

            return validation_results

        except Exception as e:
            return {
                'valid': False,
                'errors': [f"Error reading Excel file: {e}"],
                'warnings': [],
                'stats': {}
            }

    def _validate_sheet(self, sheet_name: str, df: pd.DataFrame) -> Dict:
        """Validate individual sheet"""
        validation = {'warnings': [], 'errors': [], 'stats': {}}

        # Required columns by sheet type
        required_columns = {
            'Hardware_Companies': ['Company_Name', 'Country', 'Modality'],
            'Component_Suppliers': ['Supplier_Name', 'Country'],
            'Software_Companies': ['Software_Name', 'Type']
        }

        # Check required columns
        if sheet_name in required_columns:
            for col in required_columns[sheet_name]:
                if col not in df.columns:
                    validation['errors'].append(f"{sheet_name}: Missing required column '{col}'")

        # Count valid rows (non-placeholder)
        valid_rows = 0
        empty_rows = 0
        placeholder_rows = 0

        for _, row in df.iterrows():
            name_col = required_columns.get(sheet_name, ['Company_Name'])[0] if sheet_name in required_columns else df.columns[0]
            name_value = str(row.get(name_col, '')).strip()

            if not name_value or name_value == 'nan':
                empty_rows += 1
            elif name_value.startswith('[') and name_value.endswith(']'):
                placeholder_rows += 1
            else:
                valid_rows += 1

                # Validate specific fields
                if sheet_name == 'Hardware_Companies':
                    if not str(row.get('Country', '')).strip():
                        validation['warnings'].append(f"Hardware company '{name_value}' missing country")
                elif sheet_name == 'Component_Suppliers':
                    if not str(row.get('Component_Types', '')).strip():
                        validation['warnings'].append(f"Supplier '{name_value}' missing component types")

        validation['stats'] = {
            'total_rows': len(df),
            'valid_rows': valid_rows,
            'empty_rows': empty_rows,
            'placeholder_rows': placeholder_rows
        }

        return validation

def main():
    """Command-line interface for Excel manager"""
    import argparse

    parser = argparse.ArgumentParser(description="Excel Supply Chain Manager")
    parser.add_argument("--action", choices=['create-templates', 'sync', 'validate'],
                       required=True, help="Action to perform")
    parser.add_argument("--excel-file", help="Excel file to sync/validate")
    parser.add_argument("--modality", help="Quantum modality for sync")

    args = parser.parse_args()

    manager = ExcelSupplyChainManager()

    try:
        if args.action == 'create-templates':
            templates = manager.create_excel_templates()
            print("✅ Excel templates created:")
            for name, path in templates.items():
                print(f"  {name}: {path}")

        elif args.action == 'sync':
            if not args.excel_file or not args.modality:
                print("Error: --excel-file and --modality required for sync")
                return
            result = manager.sync_excel_to_ontology(args.excel_file, args.modality)
            if result['success']:
                print(f"✅ Successfully synced {result['stats']['total']} companies")
                print(f"  Hardware: {result['stats']['hardware']}")
                print(f"  Suppliers: {result['stats']['suppliers']}")
                print(f"  Software: {result['stats']['software']}")
            else:
                print(f"❌ Sync failed: {result['error']}")

        elif args.action == 'validate':
            if not args.excel_file:
                print("Error: --excel-file required for validation")
                return
            result = manager.validate_excel_file(args.excel_file)
            print(f"Validation result: {'✅ VALID' if result['valid'] else '❌ INVALID'}")
            if result['errors']:
                print("Errors:")
                for error in result['errors']:
                    print(f"  - {error}")
            if result['warnings']:
                print("Warnings:")
                for warning in result['warnings']:
                    print(f"  - {warning}")

    except Exception as e:
        print(f"❌ Error: {e}")
        logging.error(f"CLI Error: {e}")

if __name__ == "__main__":
    main()