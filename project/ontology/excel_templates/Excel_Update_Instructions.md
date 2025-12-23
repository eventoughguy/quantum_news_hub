
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
