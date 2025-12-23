#!/usr/bin/env python3
"""
Quantum Supply Chain Data Schema
Provides structured format for adding new supply chain information to the ontology
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum

class CompanyType(Enum):
    """Company types in the quantum supply chain"""
    HARDWARE = "hardware"
    SUPPLIER = "supplier"
    SOFTWARE = "software"
    MATERIALS = "materials"
    FOUNDRY = "foundry"
    INTEGRATOR = "integrator"
    RESEARCH = "research"

class QuantumModality(Enum):
    """Quantum computing modalities"""
    SUPERCONDUCTING = "SuperconductingQubit"
    TRAPPED_ION = "TrappedIon"
    PHOTONIC = "PhotonicQuantum"
    NEUTRAL_ATOM = "NeutralAtom"
    SPIN_QUBIT = "SpinQubit"
    QUANTUM_ANNEALING = "QuantumAnnealing"
    TOPOLOGICAL = "TopologicalQubit"

class ComponentType(Enum):
    """Types of components in quantum systems"""
    SUPERCONDUCTING_WIRE = "superconducting_wire"
    HTS_TAPE = "hts_tape"
    CRYOGENIC_COMPONENT = "cryogenic_component"
    MAGNETIC_SHIELDING = "magnetic_shielding"
    QUANTUM_CHIP = "quantum_chip"
    CONTROL_ELECTRONICS = "control_electronics"
    LASER_SYSTEM = "laser_system"
    ION_TRAP = "ion_trap"
    PHOTONIC_COMPONENT = "photonic_component"
    DILUTION_REFRIGERATOR = "dilution_refrigerator"

@dataclass
class Company:
    """Base company information"""
    name: str
    company_type: CompanyType
    description: Optional[str] = None
    website: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    founded_year: Optional[int] = None
    employee_count: Optional[int] = None
    public_ticker: Optional[str] = None
    operational_status: str = "active"
    notes: Optional[str] = None
    data_source: Optional[str] = None
    last_updated: str = datetime.now().isoformat()

@dataclass
class HardwareCompany(Company):
    """Quantum hardware company"""
    modalities: List[QuantumModality]
    platforms: List[str] = None
    qubit_count: Optional[int] = None
    quantum_volume: Optional[int] = None
    cloud_service: bool = False
    partnerships: List[str] = None

@dataclass
class ComponentSupplier(Company):
    """Component supplier company"""
    component_types: List[ComponentType]
    materials_supplied: List[str] = None
    clients: List[str] = None
    applications: List[str] = None
    technical_specs: Dict[str, Union[str, float]] = None

@dataclass
class SoftwareCompany(Company):
    """Software/SDK company"""
    products: List[str]
    programming_languages: List[str] = None
    supported_hardware: List[str] = None
    license_type: str = "proprietary"
    github_url: Optional[str] = None
    documentation_url: Optional[str] = None

@dataclass
class Partnership:
    """Partnership between companies"""
    company1: str
    company2: str
    partnership_type: str  # "supplier", "client", "collaboration", "investment"
    description: Optional[str] = None
    start_date: Optional[str] = None
    status: str = "active"

@dataclass
class Product:
    """Product or service"""
    name: str
    company: str
    product_type: str
    modality: Optional[QuantumModality] = None
    description: Optional[str] = None
    specifications: Dict[str, Union[str, float]] = None
    release_date: Optional[str] = None
    status: str = "active"

class SupplyChainDataManager:
    """Manager for supply chain data operations"""

    def __init__(self, schema_file="supply_chain_data.json"):
        self.schema_file = schema_file
        self.data = self.load_data()

    def load_data(self) -> Dict:
        """Load existing data from JSON file"""
        try:
            with open(self.schema_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "companies": [],
                "partnerships": [],
                "products": [],
                "metadata": {
                    "version": "1.0",
                    "last_updated": datetime.now().isoformat(),
                    "total_companies": 0
                }
            }

    def save_data(self):
        """Save data to JSON file"""
        self.data["metadata"]["last_updated"] = datetime.now().isoformat()
        self.data["metadata"]["total_companies"] = len(self.data["companies"])

        with open(self.schema_file, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)

    def add_company(self, company: Union[Company, HardwareCompany, ComponentSupplier, SoftwareCompany]):
        """Add a new company to the dataset"""
        company_dict = asdict(company)
        # Convert enums to strings
        for key, value in company_dict.items():
            if isinstance(value, list) and value and hasattr(value[0], 'value'):
                company_dict[key] = [item.value for item in value]
            elif hasattr(value, 'value'):
                company_dict[key] = value.value

        self.data["companies"].append(company_dict)
        self.save_data()

    def add_partnership(self, partnership: Partnership):
        """Add a new partnership"""
        self.data["partnerships"].append(asdict(partnership))
        self.save_data()

    def add_product(self, product: Product):
        """Add a new product"""
        product_dict = asdict(product)
        if product_dict.get('modality') and hasattr(product_dict['modality'], 'value'):
            product_dict['modality'] = product_dict['modality'].value

        self.data["products"].append(product_dict)
        self.save_data()

    def get_companies_by_modality(self, modality: QuantumModality) -> List[Dict]:
        """Get all companies working with specific modality"""
        result = []
        for company in self.data["companies"]:
            if "modalities" in company and modality.value in company["modalities"]:
                result.append(company)
        return result

    def get_suppliers_for_client(self, client_name: str) -> List[Dict]:
        """Get all suppliers for a specific client"""
        result = []
        for company in self.data["companies"]:
            if company.get("company_type") == "supplier" and company.get("clients"):
                if client_name in company["clients"]:
                    result.append(company)
        return result

    def export_for_ontology(self, modality: Optional[QuantumModality] = None) -> Dict:
        """Export data in format suitable for ontology loading"""
        companies = self.data["companies"]
        if modality:
            companies = self.get_companies_by_modality(modality)

        return {
            "modality": modality.value if modality else "all",
            "companies": companies,
            "partnerships": self.data["partnerships"],
            "products": self.data["products"]
        }

# Example data templates
EXAMPLE_TEMPLATES = {
    "superconducting_hardware_company": {
        "name": "Example Quantum Corp",
        "company_type": "hardware",
        "modalities": ["SuperconductingQubit"],
        "description": "Leading superconducting quantum computing company",
        "country": "USA",
        "founded_year": 2019,
        "qubit_count": 127,
        "cloud_service": True,
        "platforms": ["Example Quantum Platform"],
        "partnerships": ["IBM", "Microsoft"]
    },

    "component_supplier": {
        "name": "SuperConductor Materials Corp",
        "company_type": "supplier",
        "component_types": ["superconducting_wire", "hts_tape"],
        "materials_supplied": ["NbTi wire", "Nb₃Sn wire", "YBCO tape"],
        "clients": ["IBM", "Google", "Rigetti"],
        "country": "USA",
        "technical_specs": {
            "current_capacity": "300A",
            "critical_temperature": "93K",
            "wire_diameter": "0.7mm"
        }
    },

    "software_company": {
        "name": "Quantum Software Solutions",
        "company_type": "software",
        "products": ["QuantumSDK Pro", "Quantum Simulator"],
        "programming_languages": ["Python", "C++"],
        "supported_hardware": ["IBM Quantum", "IonQ", "Rigetti"],
        "license_type": "open_source",
        "github_url": "https://github.com/quantum-software/sdk"
    },

    "trapped_ion_company": {
        "name": "IonTech Quantum",
        "company_type": "hardware",
        "modalities": ["TrappedIon"],
        "description": "Trapped ion quantum computing specialist",
        "country": "Germany",
        "qubit_count": 32,
        "platforms": ["IonTech Platform"]
    }
}

def create_example_data():
    """Create example data file with sample entries"""
    manager = SupplyChainDataManager("example_supply_chain_data.json")

    # Add example companies
    hardware_company = HardwareCompany(
        name="Example Quantum Corp",
        company_type=CompanyType.HARDWARE,
        modalities=[QuantumModality.SUPERCONDUCTING],
        description="Leading superconducting quantum computing company",
        country="USA",
        founded_year=2019,
        qubit_count=127,
        cloud_service=True,
        platforms=["Example Quantum Platform"]
    )
    manager.add_company(hardware_company)

    supplier = ComponentSupplier(
        name="SuperConductor Materials Corp",
        company_type=CompanyType.SUPPLIER,
        component_types=[ComponentType.SUPERCONDUCTING_WIRE, ComponentType.HTS_TAPE],
        materials_supplied=["NbTi wire", "Nb₃Sn wire", "YBCO tape"],
        clients=["IBM", "Google", "Rigetti"],
        country="USA"
    )
    manager.add_company(supplier)

    # Add partnership
    partnership = Partnership(
        company1="Example Quantum Corp",
        company2="SuperConductor Materials Corp",
        partnership_type="supplier",
        description="Supply of superconducting materials"
    )
    manager.add_partnership(partnership)

    print("✅ Example data file created: example_supply_chain_data.json")
    return manager

if __name__ == "__main__":
    # Create example data
    create_example_data()

    # Print templates
    print("\n📋 DATA TEMPLATES:")
    print("=" * 50)
    for template_name, template_data in EXAMPLE_TEMPLATES.items():
        print(f"\n{template_name.upper()}:")
        print(json.dumps(template_data, indent=2))