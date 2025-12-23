# Excel Supply Chain Update Workflow

A simple guide for updating the quantum computing supply chain ontology using Excel spreadsheets.

## 🎯 Quick Start

### 1. Create Templates (One-Time Setup)
```bash
cd /home/liuyiwen/AI/AI\ Agent/quantum_news_agent/project/ontology
source ../../../.venv/bin/activate
python excel_manager.py --action create-templates
```

This creates Excel templates in `excel_templates/`:
- `Superconducting_Supply_Chain.xlsx` - For superconducting companies
- `TrappedIon_Supply_Chain.xlsx` - For trapped ion companies
- `Photonic_Supply_Chain.xlsx` - For photonic companies
- `Generic_Modality_Template.xlsx` - For any new modality

### 2. Update Excel Files

Open any Excel template and add new companies to the appropriate sheets:

#### **Hardware_Companies Sheet**
- Add quantum hardware/platform companies
- Fill in: Company_Name, Country, Qubit_Count, Platform_Name, Website, etc.

#### **Component_Suppliers Sheet**
- Add suppliers of materials/components
- Fill in: Supplier_Name, Component_Types, Materials_Supplied, Known_Clients, etc.

#### **Software_Companies Sheet**
- Add SDK, framework, and software companies
- Fill in: Software_Name, Company, Programming_Languages, Supported_Hardware, etc.

### 3. Sync to Ontology
```bash
python excel_manager.py --action sync --excel-file Superconducting_Supply_Chain.xlsx --modality SuperconductingQubit
```

### 4. Validate Before Syncing (Optional)
```bash
python excel_manager.py --action validate --excel-file TrappedIon_Supply_Chain.xlsx
```

## 📋 Available Templates

| Template | Use For | Example Companies |
|----------|---------|-------------------|
| `Superconducting_Supply_Chain.xlsx` | Superconducting quantum | IBM, Google, Rigetti |
| `TrappedIon_Supply_Chain.xlsx` | Trapped ion quantum | IonQ, Quantinuum, Alpine QT |
| `Photonic_Supply_Chain.xlsx` | Photonic quantum | Xanadu, PsiQuantum, Orca |
| `Generic_Modality_Template.xlsx` | Any new modality | Copy and customize |

## 🔧 Excel Editing Tips

### Required Fields
- **Company_Name/Supplier_Name/Software_Name**: Official name (required)
- **Country**: Country of operation (recommended)
- **Modality**: Keep consistent with template (e.g., "SuperconductingQubit")

### Data Quality Guidelines
1. **Use Official Names**: Get company names from official websites
2. **Verify Information**: Cross-check details from multiple sources
3. **Be Specific**: "NbTi wire, Nb₃Sn wire" instead of just "wire"
4. **Include Context**: Use Notes field for additional context
5. **Add Sources**: Mention where you got the information

### Example Entries

**Hardware Company:**
```
Company_Name: Alpine Quantum Technologies
Country: Austria
Modality: TrappedIon
Qubit_Count: 24
Cloud_Service: No
Platform_Name: AQT Platform
Website: https://aqt.eu
Founded_Year: 2018
Description: European trapped ion quantum systems
Notes: Focus on industrial applications
```

**Component Supplier:**
```
Supplier_Name: Quantum Wire Corp
Country: USA
Component_Types: Superconducting wire, cryogenic cables
Materials_Supplied: NbTi wire, Nb₃Sn wire, coaxial cables
Known_Clients: IBM, Rigetti, MIT
Applications: Quantum processors, cryogenic systems
Technical_Specs: Current capacity: 500A at 4K
Notes: Primary supplier for university labs
```

## 🚀 Advanced Usage

### Adding New Quantum Modalities

1. **Create Template:**
```bash
python excel_manager.py --action template --modality NVCenters --file nv_centers_template.xlsx
```

2. **Edit Template:** Add companies working with NV centers/diamond defects

3. **Sync to Ontology:**
```bash
python excel_manager.py --action sync --excel-file nv_centers_template.xlsx --modality NVCenters
```

### Batch Processing Multiple Files

```bash
# Process multiple modalities
python excel_manager.py --action sync --excel-file Superconducting_Supply_Chain.xlsx --modality SuperconductingQubit
python excel_manager.py --action sync --excel-file TrappedIon_Supply_Chain.xlsx --modality TrappedIon
python excel_manager.py --action sync --excel-file Photonic_Supply_Chain.xlsx --modality PhotonicQuantum
```

## 📊 Validation and Stats

### Check Excel File Quality
```bash
python excel_manager.py --action validate --excel-file your_file.xlsx
```

### View Ontology Statistics
```bash
python ontology_manager.py --action stats
```

## 🔍 Data Sources for Research

### Reliable Sources
- **Company Websites**: Official pages and press releases
- **Industry Reports**: Quantum computing market reports
- **Academic Papers**: Research collaborations and affiliations
- **Conference Talks**: Q2B, APS March Meeting presentations
- **Patent Databases**: USPTO, Google Patents
- **LinkedIn**: Company profiles and employee information
- **News Articles**: Quantum computing industry news

### Research Tips
1. **Start with Hardware Companies**: They're easier to identify and verify
2. **Follow Supply Chain**: Look at hardware company suppliers and partners
3. **Check Recent News**: Company announcements, funding, partnerships
4. **Use Multiple Sources**: Verify information from 2+ sources
5. **Document Uncertainty**: Use "[Research Needed]" for uncertain info

## 📁 File Locations

After setup, you'll have:
```
project/ontology/
├── excel_templates/
│   ├── Superconducting_Supply_Chain.xlsx
│   ├── TrappedIon_Supply_Chain.xlsx
│   ├── Photonic_Supply_Chain.xlsx
│   ├── Generic_Modality_Template.xlsx
│   └── Excel_Update_Instructions.md
├── quantum_supply_chain_ontology.ttl
├── quantum_supply_chain_ontology.owl
└── EXCEL_WORKFLOW_GUIDE.md (this file)
```

## ❗ Important Notes

- **Always backup** your Excel files before major edits
- **Validate before syncing** to catch errors early
- **Keep modality names consistent** (SuperconductingQubit, TrappedIon, etc.)
- **Don't edit placeholder rows** starting with `[` and ending with `]`
- **Sync creates backup JSON files** for reference

## 🐛 Troubleshooting

**"Excel file not found"** → Check file is in `excel_templates/` directory

**"Validation failed"** → Check required fields are filled, no empty company names

**"Sync failed"** → Validate Excel file first, check modality name spelling

**"No companies synced"** → Make sure you're not editing placeholder rows

## 🎯 Next Steps

1. **Start Small**: Pick one modality and add 2-3 well-known companies
2. **Research Systematically**: Use the data sources above
3. **Validate Often**: Run validation after adding several companies
4. **Sync Regularly**: Don't wait until you have hundreds of companies
5. **Document Progress**: Use Excel Notes field to track your research

The ontology will automatically update with your Excel changes and create comprehensive knowledge graphs of the quantum computing supply chain!