#!/usr/bin/env python3
"""
Quantum Computing Supply Chain Ontology Builder
Based on real supply chain data from the superconductor Excel file
"""

from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, OWL, XSD
import pandas as pd
import json
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class QuantumSupplyChainOntology:
    def __init__(self, base_path=None):
        self.g = Graph()

        # Define namespaces
        self.QSC = Namespace("http://quantum-supply-chain.org/ontology#")
        self.g.bind("qsc", self.QSC)
        self.g.bind("owl", OWL)
        self.g.bind("rdfs", RDFS)
        self.g.bind("rdf", RDF)
        self.g.bind("xsd", XSD)

        # Base path for files
        self.base_path = Path(base_path) if base_path else Path("/home/liuyiwen/AI/AI Agent/quantum_news_agent/project/ontology")

        # Initialize ontology metadata
        self.create_ontology_metadata()

    def create_ontology_metadata(self):
        """Create basic ontology metadata"""
        ontology_uri = URIRef("http://quantum-supply-chain.org/ontology")

        self.g.add((ontology_uri, RDF.type, OWL.Ontology))
        self.g.add((ontology_uri, RDFS.label, Literal("Quantum Computing Supply Chain Ontology")))
        self.g.add((ontology_uri, RDFS.comment, Literal(
            "Ontology for quantum computing supply chain based on real industry data, "
            "covering hardware companies, component suppliers, software providers, and their relationships."
        )))
        self.g.add((ontology_uri, OWL.versionInfo, Literal("1.0")))
        self.g.add((ontology_uri, RDFS.seeAlso, URIRef("http://quantum-supply-chain.org/data-schema")))

    def create_core_classes(self):
        """Define core classes based on actual supply chain structure"""

        classes = {
            # Main entity types from the data
            "Organization": "Base class for all organizations in the quantum supply chain",
            "QuantumHardwareCompany": "Company developing quantum computing hardware",
            "ComponentSupplier": "Company supplying components for quantum systems",
            "SoftwareCompany": "Company developing quantum software/SDKs",
            "MaterialsCompany": "Company supplying raw materials for quantum hardware",

            # Hardware and technology types
            "QuantumModality": "Different approaches to quantum computing",
            "SuperconductingQubit": "Superconducting-based quantum computing technology",
            "TrappedIon": "Trapped ion quantum computing technology",
            "PhotonicQuantum": "Photonic quantum computing technology",
            "NeutralAtom": "Neutral atom quantum computing technology",
            "SpinQubit": "Spin-based quantum computing technology",
            "QuantumAnnealing": "Quantum annealing technology",

            # Products and components
            "QuantumPlatform": "Complete quantum computing platform or system",
            "QuantumSDK": "Software development kit for quantum programming",
            "Component": "Physical component used in quantum systems",
            "SuperconductingMaterial": "Materials used in superconducting quantum systems",
            "CryogenicComponent": "Components for cryogenic cooling systems",
            "QuantumChip": "Quantum processing unit or chip",
            "MagneticShielding": "Magnetic shielding components",
            "Wire": "Specialized wire for quantum applications",
            "Cable": "Cables for quantum systems",
            "Tape": "High-temperature superconducting tape",

            # Relationships and partnerships
            "Partnership": "Business partnership between organizations",
            "SupplyRelationship": "Supply relationship between companies",
            "ClientRelationship": "Client-vendor relationship",

            # Geographic regions
            "Country": "Country where organization is located",
            "Region": "Geographic region",
        }

        for class_name, description in classes.items():
            class_uri = self.QSC[class_name]
            self.g.add((class_uri, RDF.type, OWL.Class))
            self.g.add((class_uri, RDFS.label, Literal(class_name)))
            self.g.add((class_uri, RDFS.comment, Literal(description)))

        # Create class hierarchies
        self.create_class_hierarchies()

    def create_class_hierarchies(self):
        """Define class inheritance relationships"""

        hierarchies = [
            # Organization hierarchy
            ("QuantumHardwareCompany", "Organization"),
            ("ComponentSupplier", "Organization"),
            ("SoftwareCompany", "Organization"),
            ("MaterialsCompany", "Organization"),

            # Modality hierarchy
            ("SuperconductingQubit", "QuantumModality"),
            ("TrappedIon", "QuantumModality"),
            ("PhotonicQuantum", "QuantumModality"),
            ("NeutralAtom", "QuantumModality"),
            ("SpinQubit", "QuantumModality"),
            ("QuantumAnnealing", "QuantumModality"),

            # Component hierarchy
            ("SuperconductingMaterial", "Component"),
            ("CryogenicComponent", "Component"),
            ("QuantumChip", "Component"),
            ("MagneticShielding", "Component"),
            ("Wire", "Component"),
            ("Cable", "Component"),
            ("Tape", "Component"),

            # Location hierarchy
            ("Country", "Region"),
        ]

        for subclass, superclass in hierarchies:
            self.g.add((self.QSC[subclass], RDFS.subClassOf, self.QSC[superclass]))

    def create_relationships(self):
        """Define object properties based on actual supply chain relationships"""

        relationships = {
            # Supply chain relationships
            "suppliesComponentTo": {
                "domain": "ComponentSupplier",
                "range": "QuantumHardwareCompany",
                "description": "Component supplier provides components to hardware company"
            },
            "hasClient": {
                "domain": "ComponentSupplier",
                "range": "Organization",
                "description": "Supplier has client relationship"
            },
            "usesModality": {
                "domain": "QuantumHardwareCompany",
                "range": "QuantumModality",
                "description": "Hardware company uses specific quantum modality"
            },
            "developsSDK": {
                "domain": "SoftwareCompany",
                "range": "QuantumSDK",
                "description": "Software company develops SDK"
            },
            "supportsHardware": {
                "domain": "QuantumSDK",
                "range": "QuantumPlatform",
                "description": "SDK supports specific hardware platform"
            },
            "partneredWith": {
                "domain": "Organization",
                "range": "Organization",
                "description": "Partnership between organizations"
            },
            "locatedIn": {
                "domain": "Organization",
                "range": "Country",
                "description": "Organization is located in country"
            },
            "producesComponent": {
                "domain": "ComponentSupplier",
                "range": "Component",
                "description": "Supplier produces specific component type"
            },
            "requiresComponent": {
                "domain": "QuantumPlatform",
                "range": "Component",
                "description": "Platform requires specific component"
            },
            # Add inverse relationships for better querying
            "clientOf": {
                "domain": "Organization",
                "range": "ComponentSupplier",
                "description": "Organization is client of supplier"
            }
        }

        for prop_name, prop_info in relationships.items():
            prop_uri = self.QSC[prop_name]
            self.g.add((prop_uri, RDF.type, OWL.ObjectProperty))
            self.g.add((prop_uri, RDFS.label, Literal(prop_name)))
            self.g.add((prop_uri, RDFS.comment, Literal(prop_info["description"])))
            self.g.add((prop_uri, RDFS.domain, self.QSC[prop_info["domain"]]))
            self.g.add((prop_uri, RDFS.range, self.QSC[prop_info["range"]]))

    def create_data_properties(self):
        """Define data properties for entity attributes"""

        data_properties = {
            # Basic information
            "name": {"range": XSD.string, "description": "Official company/product name"},
            "description": {"range": XSD.string, "description": "Detailed description"},
            "notes": {"range": XSD.string, "description": "Additional notes or details"},
            "website": {"range": XSD.anyURI, "description": "Official website URL"},

            # Geographic
            "country": {"range": XSD.string, "description": "Country of origin/operation"},
            "region": {"range": XSD.string, "description": "Geographic region"},

            # Product/service details
            "productType": {"range": XSD.string, "description": "Type of product or service"},
            "materialType": {"range": XSD.string, "description": "Type of material (e.g., NbTi, Nb₃Sn, MgB₂)"},
            "applicationArea": {"range": XSD.string, "description": "Primary application area"},
            "sdkLanguage": {"range": XSD.string, "description": "Programming language for SDK"},
            "license": {"range": XSD.string, "description": "Software license type"},

            # Technical specifications
            "wireType": {"range": XSD.string, "description": "Type of superconducting wire"},
            "temperatureRange": {"range": XSD.string, "description": "Operating temperature range"},
            "currentCapacity": {"range": XSD.decimal, "description": "Current carrying capacity"},
            "criticalTemperature": {"range": XSD.decimal, "description": "Superconducting critical temperature"},

            # Business information
            "fundingAmount": {"range": XSD.decimal, "description": "Amount of funding received"},
            "employeeCount": {"range": XSD.integer, "description": "Number of employees"},
            "foundedYear": {"range": XSD.gYear, "description": "Year company was founded"},
            "publicTicker": {"range": XSD.string, "description": "Stock ticker symbol if public"},

            # Status and classification
            "operationalStatus": {"range": XSD.string, "description": "Current operational status"},
            "companyStage": {"range": XSD.string, "description": "Company stage (startup, established, etc.)"},
            "marketFocus": {"range": XSD.string, "description": "Primary market focus"},

            # Temporal information
            "lastUpdated": {"range": XSD.dateTime, "description": "Last time information was updated"},
            "dataSource": {"range": XSD.string, "description": "Source of the information"},
        }

        for prop_name, prop_info in data_properties.items():
            prop_uri = self.QSC[prop_name]
            self.g.add((prop_uri, RDF.type, OWL.DatatypeProperty))
            self.g.add((prop_uri, RDFS.label, Literal(prop_name)))
            self.g.add((prop_uri, RDFS.comment, Literal(prop_info["description"])))
            self.g.add((prop_uri, RDFS.range, prop_info["range"]))

    def load_superconductor_data(self):
        """Load actual superconductor supply chain data"""
        try:
            excel_path = self.base_path / "supplychain.xlsx"
            df = pd.read_excel(excel_path, sheet_name="SuperConductor")
            logging.info(f"Loading superconductor data from {excel_path}")

            # Process each row of actual data
            for idx, row in df.iterrows():
                # Hardware companies
                hw_company = str(row.get('Quantum Computing (Mainly Harware)', '')).strip()
                if hw_company and hw_company != 'nan' and hw_company != 'NaN':
                    self.add_hardware_company(hw_company, "SuperconductingQubit")

                # Component suppliers
                supplier = str(row.get('Component supplier Company', '')).strip()
                if supplier and supplier != 'nan' and supplier != 'NaN':
                    clients_str = str(row.get('Known or Likely Quantum Clients (including hardware client)', ''))
                    notes = str(row.get('Notes', ''))
                    self.add_component_supplier(supplier, clients_str, notes)

                # Software companies
                software = str(row.get('Software Company', '')).strip()
                if software and software != 'nan' and software != 'NaN':
                    hw_supported = str(row.get('Hardware Used / Partnered With', ''))
                    sw_notes = str(row.get('Notes.1', ''))
                    self.add_software_company(software, hw_supported, sw_notes)

        except Exception as e:
            logging.error(f"Error loading superconductor data: {e}")

    def add_hardware_company(self, company_name, modality):
        """Add a quantum hardware company to the ontology"""
        company_uri = self.QSC[self.clean_name(company_name)]
        self.g.add((company_uri, RDF.type, self.QSC.QuantumHardwareCompany))
        self.g.add((company_uri, self.QSC.name, Literal(company_name)))
        self.g.add((company_uri, self.QSC.usesModality, self.QSC[modality]))
        self.g.add((company_uri, self.QSC.lastUpdated, Literal(datetime.now())))

    def add_component_supplier(self, supplier_name, clients_str, notes):
        """Add a component supplier to the ontology"""
        supplier_uri = self.QSC[self.clean_name(supplier_name)]
        self.g.add((supplier_uri, RDF.type, self.QSC.ComponentSupplier))
        self.g.add((supplier_uri, self.QSC.name, Literal(supplier_name)))

        if notes and notes != 'nan':
            self.g.add((supplier_uri, self.QSC.notes, Literal(notes)))

        # Extract country from supplier name
        if "USA" in supplier_name:
            self.g.add((supplier_uri, self.QSC.country, Literal("USA")))
        elif "Japan" in supplier_name:
            self.g.add((supplier_uri, self.QSC.country, Literal("Japan")))
        elif "China" in supplier_name:
            self.g.add((supplier_uri, self.QSC.country, Literal("China")))
        elif "Germany" in supplier_name:
            self.g.add((supplier_uri, self.QSC.country, Literal("Germany")))
        elif "France" in supplier_name:
            self.g.add((supplier_uri, self.QSC.country, Literal("France")))

        # Add client relationships
        if clients_str and clients_str != 'nan':
            clients = [c.strip() for c in clients_str.replace(',', ' ').split()]
            for client in clients:
                if client and len(client) > 2:  # Filter out short strings
                    client_uri = self.QSC[self.clean_name(client)]
                    self.g.add((supplier_uri, self.QSC.hasClient, client_uri))
                    self.g.add((client_uri, self.QSC.clientOf, supplier_uri))

    def add_software_company(self, software_name, hardware_supported, notes):
        """Add a software company/SDK to the ontology"""
        software_uri = self.QSC[self.clean_name(software_name)]

        # Determine if it's a company or SDK
        if "SDK" in software_name or any(x in software_name.lower() for x in ["qiskit", "cirq", "pennylane", "ocean", "forest", "tket"]):
            self.g.add((software_uri, RDF.type, self.QSC.QuantumSDK))
        else:
            self.g.add((software_uri, RDF.type, self.QSC.SoftwareCompany))

        self.g.add((software_uri, self.QSC.name, Literal(software_name)))

        if notes and notes != 'nan':
            self.g.add((software_uri, self.QSC.notes, Literal(notes)))

        # Add support relationships
        if hardware_supported and hardware_supported != 'nan':
            hw_list = [h.strip() for h in hardware_supported.replace(',', ' ').split()]
            for hw in hw_list:
                if hw and len(hw) > 2:
                    hw_uri = self.QSC[self.clean_name(hw)]
                    self.g.add((software_uri, self.QSC.supportsHardware, hw_uri))

    def clean_name(self, name):
        """Clean name for URI generation"""
        return name.replace(' ', '_').replace('(', '_').replace(')', '_').replace(',', '_').replace('.', '_').replace('-', '_')

    def add_new_modality_data(self, modality_name, companies_data):
        """
        Add new quantum modality data to the ontology

        Args:
            modality_name: Name of the quantum modality (e.g., "TrappedIon")
            companies_data: List of dictionaries with company information
        """
        # Create modality if it doesn't exist
        modality_uri = self.QSC[modality_name]
        self.g.add((modality_uri, RDF.type, self.QSC.QuantumModality))
        self.g.add((modality_uri, RDFS.subClassOf, self.QSC.QuantumModality))

        for company_data in companies_data:
            company_name = company_data.get('name', '')
            company_type = company_data.get('type', 'Organization')  # hardware, supplier, software

            company_uri = self.QSC[self.clean_name(company_name)]

            # Set appropriate class
            if company_type == 'hardware':
                self.g.add((company_uri, RDF.type, self.QSC.QuantumHardwareCompany))
                self.g.add((company_uri, self.QSC.usesModality, modality_uri))
            elif company_type == 'supplier':
                self.g.add((company_uri, RDF.type, self.QSC.ComponentSupplier))
            elif company_type == 'software':
                self.g.add((company_uri, RDF.type, self.QSC.SoftwareCompany))

            # Add all provided properties
            for prop, value in company_data.items():
                if prop != 'type' and value:
                    if hasattr(self.QSC, prop):
                        self.g.add((company_uri, getattr(self.QSC, prop), Literal(value)))

            self.g.add((company_uri, self.QSC.lastUpdated, Literal(datetime.now())))

    def build_ontology(self):
        """Build the complete ontology"""
        logging.info("Building Quantum Supply Chain Ontology...")

        self.create_core_classes()
        logging.info("✅ Created core classes and hierarchies")

        self.create_relationships()
        logging.info("✅ Created relationships")

        self.create_data_properties()
        logging.info("✅ Created data properties")

        self.load_superconductor_data()
        logging.info("✅ Loaded superconductor supply chain data")

        logging.info(f"Ontology completed with {len(self.g)} triples")

    def save_ontology(self, filename_base="quantum_supply_chain_ontology"):
        """Save ontology in multiple formats"""
        formats = {
            'turtle': 'ttl',
            'xml': 'owl',
            'n3': 'n3',
            'json-ld': 'jsonld'
        }

        for format_name, extension in formats.items():
            filepath = self.base_path / f"{filename_base}.{extension}"
            self.g.serialize(destination=str(filepath), format=format_name)
            logging.info(f"✅ Ontology saved as {format_name}: {filepath}")

    def get_statistics(self):
        """Get ontology statistics"""
        classes = list(self.g.subjects(RDF.type, OWL.Class))
        object_props = list(self.g.subjects(RDF.type, OWL.ObjectProperty))
        data_props = list(self.g.subjects(RDF.type, OWL.DatatypeProperty))

        # Count instances (excluding classes and properties)
        instances = set()
        for s, p, o in self.g:
            if p == RDF.type and o not in [OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.Ontology]:
                instances.add(s)

        return {
            'total_triples': len(self.g),
            'classes': len(classes),
            'object_properties': len(object_props),
            'data_properties': len(data_props),
            'instances': len(instances),
            'namespaces': len(list(self.g.namespaces()))
        }

    def query_suppliers_by_client(self, client_name):
        """Query suppliers for a specific client"""
        query = f"""
        PREFIX qsc: <http://quantum-supply-chain.org/ontology#>
        SELECT ?supplier ?supplierName ?notes WHERE {{
            ?supplier qsc:hasClient ?client .
            ?supplier qsc:name ?supplierName .
            ?client qsc:name "{client_name}" .
            OPTIONAL {{ ?supplier qsc:notes ?notes }}
        }}
        """
        return list(self.g.query(query))

    def query_companies_by_modality(self, modality):
        """Query companies using specific quantum modality"""
        query = f"""
        PREFIX qsc: <http://quantum-supply-chain.org/ontology#>
        SELECT ?company ?companyName WHERE {{
            ?company qsc:usesModality qsc:{modality} .
            ?company qsc:name ?companyName .
        }}
        """
        return list(self.g.query(query))

def main():
    """Main function to build the ontology"""
    try:
        ontology = QuantumSupplyChainOntology()
        ontology.build_ontology()
        ontology.save_ontology()

        # Print statistics
        stats = ontology.get_statistics()
        print("\n📊 ONTOLOGY STATISTICS")
        print("=" * 50)
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

        print("\n✅ Quantum Supply Chain Ontology created successfully!")

        # Example queries
        print("\n🔍 Example Queries:")
        print("IBM suppliers:")
        ibm_suppliers = ontology.query_suppliers_by_client("IBM")
        for result in ibm_suppliers[:3]:
            print(f"  - {result[1]} ({result[2] if result[2] else 'No notes'})")

        return ontology

    except Exception as e:
        logging.error(f"Error building ontology: {e}")
        raise

if __name__ == "__main__":
    main()