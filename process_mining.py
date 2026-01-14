"""
🎯 Open Source Process Mining - Single Script Solution

Simple end-to-end process mining: Excel → SQLite → Event Log → Process Map

Author: Dr. Nick Blackbourn
Usage: python process_mining.py
"""

import sqlite3
import pandas as pd
import pm4py
import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import defaultdict


def create_fallback_visualization(dfg, event_log):
    """Create simple process flow diagram using matplotlib."""

    # Extract unique activities and their frequencies
    activities = sorted(event_log['Activities'].unique())
    activity_counts = event_log['Activities'].value_counts()

    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, len(activities) + 2)

    # Position activities vertically
    activity_positions = {}
    for i, activity in enumerate(activities):
        y_pos = len(activities) - i
        activity_positions[activity] = (6, y_pos)

        # Draw activity box
        rect = patches.Rectangle((4.5, y_pos-0.4), 3, 0.8,
                                 linewidth=2, edgecolor='navy', facecolor='lightblue', alpha=0.8)
        ax.add_patch(rect)

        # Clean activity name and add count
        clean_name = activity.replace('Date', '')
        count = activity_counts.get(activity, 0)
        ax.text(6, y_pos, f"{clean_name}\n({count} events)",
                ha='center', va='center', fontsize=10, weight='bold')

    # Draw process flows with arrows
    for (source, target), frequency in dfg.items():
        if source in activity_positions and target in activity_positions:
            src_pos = activity_positions[source]
            tgt_pos = activity_positions[target]

            # Calculate arrow positions
            start_x = src_pos[0] + 1.5
            end_x = tgt_pos[0] - 1.5

            # Draw curved arrow
            ax.annotate('', xy=(end_x, tgt_pos[1]),
                        xytext=(start_x, src_pos[1]),
                        arrowprops=dict(arrowstyle='->', lw=max(1, frequency/4),
                                        color='darkgreen', alpha=0.8,
                                        connectionstyle="arc3,rad=0.1"))

            # Add frequency label
            mid_x = (start_x + end_x) / 2 + 0.5
            mid_y = (src_pos[1] + tgt_pos[1]) / 2
            ax.text(mid_x, mid_y, str(frequency),
                    ha='center', va='center', fontsize=9, weight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", facecolor='yellow', alpha=0.7))

    # Title and formatting
    ax.set_title('Process Flow Discovery Results\nExcel → SQLite → PM4PY Analysis',
                 fontsize=16, weight='bold', pad=20)

    # Add summary statistics
    stats_text = f"""Process Mining Results:
• Total Cases: {event_log['OrderID'].nunique()}
• Total Events: {len(event_log)}
• Activity Types: {len(activities)}
• Time Span: {(pd.to_datetime(event_log['Timestamp']).max() - pd.to_datetime(event_log['Timestamp']).min()).days} days"""

    ax.text(0.5, 1, stats_text, fontsize=11, verticalalignment='top',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.9))

    ax.set_xlabel('Process Flow Direction →', fontsize=12)
    ax.axis('off')

    plt.tight_layout()
    plt.savefig('output/process_map_matplotlib.png', dpi=300,
                bbox_inches='tight', facecolor='white')
    plt.close()


def main():
    """Complete process mining pipeline in one script."""

    print("🎯 Open Source End-to-End Process Mining")
    print("=" * 50)

    # Check if sample data exists
    excel_file = "sample_data.xlsx"
    if not os.path.exists(excel_file):
        print(f"❌ Error: {excel_file} not found")
        print("   Please ensure the sample Excel file is in this directory")
        return

    print("📥 STEP 1: Load Excel → SQLite")
    print("-" * 30)

    # Load Excel data into SQLite
    conn = sqlite3.connect("output/process_data.db")
    xl = pd.ExcelFile(excel_file)

    tables_loaded = 0
    for sheet_name in xl.sheet_names:
        if sheet_name == 'DB structure':  # Skip metadata sheet
            continue

        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        table_name = sheet_name.lower().replace(" ", "")
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"  ✓ {sheet_name} → {len(df)} rows")
        tables_loaded += 1

    print(f"✅ Loaded {tables_loaded} tables into SQLite")

    print("\n🔄 STEP 2: ETL Transformation (Unpivot + Concatenate)")
    print("-" * 50)

    # SQL query that replicates KNIME unpivot + concatenate operations
    event_log_query = """
    WITH unpivoted_events AS (
        -- ORDER TABLE EVENTS (using column names as activities)
        SELECT OrderID, 'OrderDate' as Activities, OrderDate as Timestamp, 'order' as source_type
        FROM ordertable WHERE OrderDate IS NOT NULL
        UNION ALL
        SELECT OrderID, 'PickedDate', PickedDate, 'order' 
        FROM ordertable WHERE PickedDate IS NOT NULL
        UNION ALL  
        SELECT OrderID, 'PackedDate', PackedDate, 'order'
        FROM ordertable WHERE PackedDate IS NOT NULL
        UNION ALL
        -- SHIPPING TABLE EVENTS (using column names as activities)
        SELECT OrderID, 'DeliveredDate', DeliveredDate, 'shipping'
        FROM shippingtable WHERE DeliveredDate IS NOT NULL
        UNION ALL
        SELECT OrderID, 'PickUpDate', PickUpDate, 'shipping'  
        FROM shippingtable WHERE PickUpDate IS NOT NULL
        UNION ALL
        -- SUPPORT TABLE EVENTS (using column names as activities)
        SELECT OrderID, 'TicketReceived', TicketReceived, 'support'
        FROM supporttable WHERE TicketReceived IS NOT NULL
        UNION ALL
        SELECT OrderID, 'TicketResolved', TicketResolved, 'support'
        FROM supporttable WHERE TicketResolved IS NOT NULL
        UNION ALL
        SELECT OrderID, 'RefundIssued', RefundIssued, 'support'
        FROM supporttable WHERE RefundIssued IS NOT NULL
    )
    
    -- JOIN with all tables to create enriched event log
    SELECT 
        ue.OrderID,
        ue.Activities,
        ue.Timestamp,
        c.CustomerID,
        c.ShippingAddress,
        o.OrderDetails,
        o.OrderTotal,
        o.Warehouse,
        s.DeliveryCompany,
        s.ShipmentID,
        sup.TicketID,
        sup.SupportTeam,
        sup.IssueCategory,
        sup.CustomerNPS,
        c.SignUpDate,
        c.HasLoyaltyCard
    FROM unpivoted_events ue
    LEFT JOIN ordertable o ON ue.OrderID = o.OrderID
    LEFT JOIN customertable c ON o.CustomerID = c.CustomerID  
    LEFT JOIN shippingtable s ON ue.OrderID = s.OrderID
    LEFT JOIN supporttable sup ON ue.OrderID = sup.OrderID
    ORDER BY ue.OrderID, ue.Timestamp
    """

    # Execute transformation
    event_log = pd.read_sql_query(event_log_query, conn)
    conn.close()

    print(f"  ✓ Event log created: {len(event_log)} events")
    print(f"  ✓ Unique cases: {event_log['OrderID'].nunique()}")
    print(f"  ✓ Activities: {sorted(event_log['Activities'].unique())}")

    # Save intermediate result
    event_log.to_csv('output/event_log.csv', index=False)
    print(f"  ✓ Saved: event_log.csv")

    print("\n🔍 STEP 3: Process Discovery & Visualization")
    print("-" * 40)

    # Convert to PM4PY format
    pm4py_log = event_log.rename(columns={
        'OrderID': 'case:concept:name',
        'Activities': 'concept:name',
        'Timestamp': 'time:timestamp'
    }).copy()

    # Convert timestamp and add resource
    pm4py_log['time:timestamp'] = pd.to_datetime(pm4py_log['time:timestamp'])
    pm4py_log['org:resource'] = pm4py_log.apply(lambda row:
                                                row['Warehouse'] if pd.notna(row['Warehouse']) else
                                                row['DeliveryCompany'] if pd.notna(row['DeliveryCompany']) else
                                                row['SupportTeam'] if pd.notna(row['SupportTeam']) else 'Unknown', axis=1)

    # Create PM4PY event log
    event_log_pm4py = pm4py.convert_to_event_log(
        pm4py_log[['case:concept:name', 'concept:name',
                   'time:timestamp', 'org:resource']]
    )

    # Discover process flows
    dfg, start_activities, end_activities = pm4py.discover_dfg(event_log_pm4py)

    print(f"  ✓ Process flows discovered:")
    for (source, target), frequency in dfg.items():
        print(f"    {source} → {target} ({frequency}x)")

    # Create visualizations - Focus on Petri net
    try:
        # Save DFG visualization
        pm4py.save_vis_dfg(dfg, start_activities,
                           end_activities, "output/process_map.png")
        print(f"  ✓ Process map saved: output/process_map.png")

    except Exception as e:
        print(f"  ⚠ Graphviz visualization failed: {e}")
        print("  📊 Falling back to matplotlib process flow diagram...")
        create_fallback_visualization(dfg, event_log)
        print(f"  ✓ Process map saved: output/process_map_matplotlib.png")

    print("\n📊 STEP 4: Process Analytics")
    print("-" * 30)

    # Calculate basic metrics
    total_cases = event_log['OrderID'].nunique()
    total_events = len(event_log)
    avg_events_per_case = total_events / total_cases

    print(f"  ✓ Cases processed: {total_cases}")
    print(f"  ✓ Total events: {total_events}")
    print(f"  ✓ Avg events per case: {avg_events_per_case:.1f}")

    # Activity frequency
    activity_counts = event_log['Activities'].value_counts()
    print(
        f"  ✓ Most common activity: {activity_counts.index[0]} ({activity_counts.iloc[0]}x)")
    print(
        f"  ✓ Least common activity: {activity_counts.index[-1]} ({activity_counts.iloc[-1]}x)")

    # Time-based analysis
    event_log['Timestamp'] = pd.to_datetime(event_log['Timestamp'])
    date_range = event_log['Timestamp'].max() - event_log['Timestamp'].min()
    print(f"  ✓ Data spans: {date_range.days} days")

    print("\n🎉 PROCESS MINING COMPLETE!")
    print("=" * 50)
    print("📄 Files created:")
    print("  • process_data.db     (SQLite database)")
    print("  • event_log.csv       (Process event log)")

    # Check which visualization files exist
    if os.path.exists("output/process_map.png"):
        print("  • process_map.png     (Direct-follows graph)")
    if os.path.exists("output/process_map_matplotlib.png"):
        print("  • process_map_matplotlib.png (Process flow diagram)")

    print("\n🚀 Next steps:")
    if os.path.exists("output/process_map.png"):
        print("  • Open output/process_map.png to see your process flow")
    elif os.path.exists("output/process_map_matplotlib.png"):
        print("  • Open output/process_map_matplotlib.png to see your process flow")
    print("  • Analyze output/event_log.csv for detailed insights")
    print("  • Use PM4PY for advanced process mining")
    print("  • Replace with your own Excel data")


if __name__ == "__main__":
    main()
