# 🎯 Open Source End-to-End Process Mining

**Transform business data into process insights in 2 minutes:** Excel → SQLite → Event Log → Process Map

## 🤔 Why This Repository?

Most process mining tutorials use toy datasets or require complex enterprise tools. This repository bridges that gap by:

✅ **Real business scenario** - E-commerce order fulfillment with realistic complexity  
✅ **Complete pipeline** - Raw Excel data to actionable process visualization  
✅ **Zero complexity** - Single Python script, no Docker, no configuration  
✅ **Production techniques** - SQL ETL, PM4PY algorithms, proper event log structure  
✅ **Immediate results** - See your process map in under 2 minutes  

Perfect for data analysts, business analysts, and students learning process mining fundamentals.

## ⚡ Quick Start

```bash
# 1. Install Graphviz (required for process visualizations)
# Windows: winget install Graphviz.Graphviz
# macOS: brew install graphviz
# Linux: sudo apt-get install graphviz

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Run the complete pipeline
python process_mining.py
```

**That's it!** Your process map will be generated automatically.

## 📊 What You Get

- **process_data.db** - Your Excel data transformed into SQLite format
- **event_log.csv** - PM4PY-compatible event log with Case ID, Activity, Timestamp
- **process_map.png** - Direct-follows graph showing activity flows with frequencies
- **process_map_matplotlib.png** - Backup visualization (if Graphviz fails)

## 🔄 The Complete Pipeline

```
Excel Business Data → SQLite ETL → Event Log → Process Discovery → Visual Process Map
```

### Step-by-Step Breakdown:

**1. Data Ingestion** 📥
- Load 4 Excel sheets (Orders, Customers, Shipping, Support) into SQLite
- Validate data structure and relationships

**2. ETL Transformation** 🔄  
- Unpivot date columns into activity events (OrderDate → "OrderDate" activity)
- Join customer, shipping, and support data to enrich events
- Create proper event log: Case ID (OrderID) + Activity + Timestamp + Resources

**3. Process Discovery** 🔍
- Use PM4PY to discover directly-follows relationships
- Calculate activity frequencies and process variants
- Identify process flows: OrderDate → PickedDate → PackedDate → DeliveredDate

**4. Visualization** 📊
- Generate process map showing activities as nodes, flows as arrows
- Display frequency counts on each flow (e.g., "OrderDate → PickedDate (15x)")
- Create fallback matplotlib visualization if Graphviz unavailable

## 📁 Your Data Structure

Place your Excel file as `sample_data.xlsx` with these sheets:
- **OrderTable** - Orders with OrderDate, PickedDate, PackedDate
- **CustomerTable** - Customer information
- **ShippingTable** - Delivery dates and logistics
- **SupportTable** - Tickets and support interactions

## 🔧 Customization

Replace `sample_data.xlsx` with your own data following the same structure. The script automatically:
- Detects all Excel sheets
- Unpivots date columns into activities
- Creates complete event log with case enrichment
- Generates process visualizations

## 🛠️ Requirements

- Python 3.8+
- **Graphviz** (system binary for visualizations)
- Python packages: pandas, pm4py, openpyxl, matplotlib, graphviz, pydotplus

## 📖 Understanding Your Process Map

### **E-Commerce Order Fulfillment Process Discovered:**

**Main Happy Path (75% of orders):**  
`OrderDate → PickedDate → PackedDate → PickUpDate → DeliveredDate`

**Process Variants:**
- **Pre-fulfillment amendments**: OrderDate → TicketReceived → TicketResolved → PickedDate...
- **Post-delivery issues**: ...DeliveredDate → TicketReceived → TicketResolved → RefundIssued
- **Cancellations**: OrderDate → TicketReceived → TicketResolved → RefundIssued

**Key Insights Revealed:**
- 📊 **Process complexity**: 8 distinct activities, 4 main process variants
- ⏱️ **Timing patterns**: Average 6 events per order case
- 🔄 **Exception handling**: Support tickets can occur at any stage
- 📈 **Frequencies**: Shows which paths are most common (numbers on arrows)

### **Reading the Process Map:**
- **Boxes** = Activities (OrderDate, PickedDate, etc.)
- **Arrows** = Process flows with frequency counts
- **Thickness** = More frequent flows have thicker arrows
- **Layout** = Left-to-right temporal flow

## 🎓 Learning Process Mining

This repository demonstrates core process mining concepts:
- **Event Log Creation** from business data
- **Process Discovery** using frequency-based algorithms  
- **Process Visualization** with directly-follows graphs
- **Performance Analysis** with timing and metrics

## 👤 Author

**Dr. Nick Blackbourn** - Process Mining & Data Engineering Consultant

## 📄 License

MIT License - Use freely for learning and commercial projects.