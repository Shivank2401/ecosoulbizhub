import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import altair as alt
import plotly.express as px

# Load data
inventory_data = pd.read_excel(
    "C:/Users/rajpu/OneDrive - EcoSoul Home/Central Repository/inventory/IMS_new_Dashboard_files/Inventory-Database.xlsx",  sheet_name="Inventory_S-D")
inventory_data = inventory_data.loc[:, ['SKU', '3G', 'Updike', 'Walmart', 'Amazon-USA', 'Amazon-Canada', 'Amazon-UAE',
                                        'Amazon-UK', 'Amazon-Germany', 'Amazon-India', 'Easy Ecom', 'Flipkart']]

container_data = pd.read_excel(r"C:\Users\rajpu\OneDrive - EcoSoul Home\Central Repository\inventory\IMS_new_Dashboard_files\Container_Data.xlsx", sheet_name='Container SKU')
container_data = container_data.loc[:, ['Container_No','Reference_No','SKU','Cases','Box/Cases','QTY in Box','Total price /box','Total Amount /SKU (Inclusive Commission)',
                                        'Dispatched Date from WH','Departure Date from Port','Arrival Date on Port','WH_Arrival_Month','Origin','Destination Port','US WH Name',
                                        'Main Delivery Date','Status','Reflecting in WH Inventory','Main_Container No.','Delivery Type','Location','Month_Year','Month_diff','Aging']]   

amazon_shipment = pd.read_excel(r"C:\Users\rajpu\OneDrive - EcoSoul Home\Central Repository\inventory\IMS_new_Dashboard_files\All-Shipment_Amazon.xlsx")

zoho_db= pd.read_excel(r"C:\Users\rajpu\OneDrive - EcoSoul Home\Central Repository\inventory\IMS_new_Dashboard_files\Zoho_as_of_Today.xlsx", sheet_name='Pivot_RM_Calculator')
zoho_pivot = pd.read_excel(r"C:\Users\rajpu\OneDrive - EcoSoul Home\Central Repository\inventory\IMS_new_Dashboard_files\Zoho_as_of_Today.xlsx", sheet_name='zoho_pivot')

threeg_orders = pd.read_excel(r"C:\Users\rajpu\OneDrive - EcoSoul Home\Central Repository\inventory\IMS_new_Dashboard_files\USA-3G_WH.xlsx", sheet_name='3G-Orders')
threeg_db = pd.read_excel(r"C:\Users\rajpu\OneDrive - EcoSoul Home\Central Repository\inventory\IMS_new_Dashboard_files\USA-3G_WH.xlsx", sheet_name='3G-Inventory')
threeg_age = pd.read_excel(r"C:\Users\rajpu\OneDrive - EcoSoul Home\Central Repository\inventory\IMS_new_Dashboard_files\USA-3G_WH.xlsx", sheet_name='3G-Aging')

updike_db = pd.read_excel(r"C:\Users\rajpu\OneDrive - EcoSoul Home\Central Repository\inventory\IMS_new_Dashboard_files\USA-Updike_WH.xlsx", sheet_name='Updk-Inveto')
updike_orders = pd.read_excel(r"C:\Users\rajpu\OneDrive - EcoSoul Home\Central Repository\inventory\IMS_new_Dashboard_files\USA-Updike_WH.xlsx", sheet_name='Updk-Outgoing')

retail_overview = pd.read_csv(r"C:\Users\rajpu\OneDrive - EcoSoul Home\Central Repository\retail\Retail-Dashboard_Files\retail_po_sku_data.csv")

website_customer = pd.read_excel(r"C:\Users\rajpu\OneDrive - EcoSoul Home\Central Repository\Digital Marketing\dashboard_files\Sales_data.xlsx")


# Main Header
st.set_page_config(
    page_title="Ecosoul Home",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

# Sidebar Navigation with Custom Buttons and Icons
with st.sidebar:
    st.markdown("## Ecosoul: A Holistic View of Business")
    main_page = option_menu(
        "Main Menu", 
        ["Main", "Inventory", "Retail", "Quick Commerce", "Zoho",'Digital Marketing'],
        icons=["house", "archive", "cart",  "cart", "database", "graph-up-arrow"],
        menu_icon= 'list' ,
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#000f0c"}, # 00624E 071D3B 000f0c
            "icon": {"color": "white", "font-size": "20px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#F4877A"},
            "nav-link-selected": {"background-color": "#00624E"}, } )

# Main Page Logic
if main_page == "Main":
    st.write("Welcome to the Ecosoul Home Dashboard! 🎉")
    st.write("This dashboard provides a holistic view of the business, including inventory management, retail insights, quick commerce data, and Zoho platform integration.")
    st.write("Navigate to the sidebar to explore different sections of the dashboard.")
# ____________________________________________ for Inventory page _________________________________________________________________________________________________________________________ 
elif main_page == "Inventory":
    st.header("🚛 Inventory Management")
    
    # Define tabs for navigation
    tab1, tab2, tab3, tab4 = st.tabs(["Inventory Overview", "Shipment Tracker", "Warehouses", "Amazon"])    

    with tab1: # Inventory Overview
        st.subheader("Inventory Snapshot📦")
        # Define columns for filters and key metrics side by side
        metrics_col, filter_col = st.columns([15, 6])  # Adjust column width as needed (e.g., 4 for filters, 8 for metrics)

        # **Filters**
        with filter_col:
            st.markdown('<p class="header-font">Filters</p>', unsafe_allow_html=True)
            
            # SKU Filter
            unique_sku = inventory_data['SKU'].unique()
            selected_sku = st.multiselect("Select SKU(s):", options=["All"] + list(unique_sku), default=["All"])  
        
        # Filter data based on selections
        filtered_data = inventory_data.copy()
        if "All" not in selected_sku:
            filtered_data = filtered_data[filtered_data['SKU'].isin(selected_sku)]

        # **Key Metrics**
        with metrics_col:
            # Calculate totals for each numeric column
            numeric_columns = filtered_data.select_dtypes(include=["number"]).columns
            totals = filtered_data[numeric_columns].sum()

            # Display totals in a 3x3 matrix
            st.markdown('<p class="header-font">🧐 Key Metrics</p>', unsafe_allow_html=True)
            num_cols = 3
            rows = [numeric_columns[i:i + num_cols] for i in range(0, len(numeric_columns), num_cols)]

            for row in rows:
                cols = st.columns(len(row))
                for idx, col_name in enumerate(row):
                    with cols[idx]:
                        st.info(f"**{col_name}\n Total Sellable:**\n {totals[col_name]:,.2f}")

        # Add some spacing
        st.markdown("---")

        # **Data Table for Raw Material as of Today**
        st.markdown("""
            <p style="background-color: #4CAF50; color: white; padding: 10px; border-radius: 50px; text-align: center; font-weight: bold;">
                Sellable as of Today
            </p>
            """, unsafe_allow_html=True)
        st.dataframe(filtered_data, width=2500, height=500, use_container_width=True, hide_index=None)

# ______________________________________________________________________________ for shipment _____________________________________________________________________________________________________________
    with tab2: # Shipment Tracker
        st.subheader("Shipments🚢")

                # **Set Style for Headers with White Banner**
        st.markdown("""
            <style>
                .banner {
                    background-color: white;  /* White background */
                    color: black;  /* Black text */
                    font-size: 25px;  /* Adjust font size */
                    font-weight: bold;
                    text-align: center;  /* Center align */
                    padding: 8px;  /* Add padding for better spacing */
                    border-radius: 5px;  /* Rounded corners */
                    border: 1px solid black;  /* Black border for emphasis */
                }
            </style>
        """, unsafe_allow_html=True)

        # **Display Header with Banner**
        st.markdown('<div class="banner">Container Tracking</div>', unsafe_allow_html=True)

        st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)

        # Convert Month_Year to datetime format and then to MM-YY
        container_data = container_data.dropna(subset=['Month_Year'])  # Remove NaT values
        container_data['Month_Year'] = pd.to_datetime(container_data['Month_Year'], format='%b-%Y')
        container_data['Month Year'] = container_data['Month_Year'].dt.strftime('%b-%y')
        container_data["Reference_No"] = container_data["Reference_No"].astype(object)

        # Sort Month_Year in ascending order
        container_data = container_data.sort_values(by='Month Year')

        # Unique Year-Month for filter
        unique_months = container_data['Month Year'].unique()

        # **Filters in Matrix Form Above Key Metrics**
        metrics_col, donut_col,filter_col, = st.columns([6, 10, 6]) 

        # **Set Common Font Size for Headers**
        header_style = """
            <style>
                .header-font {
                    font-size: 20px;
                    font-weight: bold;
                }
            </style>
        """
        # Inject the styling into the Streamlit app
        st.markdown(header_style, unsafe_allow_html=True)
        
        # Filters
        with filter_col:
            st.markdown('<p class="header-font">Filters</p>', unsafe_allow_html=True)
            # Your filter options here (year-month, SKU, etc.)

            # Year-Month Filter
            selected_month = st.selectbox("Select Year-Month:", ["All"] + list(unique_months))
            
            # SKU Filter
            unique_skus = container_data['SKU'].unique()
            selected_sku = st.multiselect("Select SKU(s):", options=["All"] + list(unique_skus), default=["All"])
            
            # Reference No Filter
            unique_reference_no = container_data['Reference_No'].unique()
            selected_reference_no = st.multiselect("Select Reference No(s):", options=["All"] + list(unique_reference_no), default=["All"])
            
            # US WH Name Filter
            unique_wh_names = container_data['US WH Name'].unique()
            selected_wh_name = st.multiselect("Select US WH Name(s):", options=["All"] + list(unique_wh_names), default=["All"])
            
            # Status Filter
            unique_status = container_data['Status'].unique()
            selected_status = st.multiselect("Select Status(es):", options=["All"] + list(unique_status), default=["All"])

        # Filter data based on selections
        filtered_data = container_data.copy()

        if selected_month != "All":
            filtered_data = filtered_data[filtered_data['Month Year'] == selected_month]

        if "All" not in selected_sku:
            filtered_data = filtered_data[filtered_data['SKU'].isin(selected_sku)]

        if "All" not in selected_reference_no:
            filtered_data = filtered_data[filtered_data['Reference_No'].isin(selected_reference_no)]

        if "All" not in selected_wh_name:
            filtered_data = filtered_data[filtered_data['US WH Name'].isin(selected_wh_name)]

        if "All" not in selected_status:
            filtered_data = filtered_data[filtered_data['Status'].isin(selected_status)]

        # Compute key metrics for filtered data
        unique_reference_count = filtered_data['Reference_No'].nunique()
        total_amount = filtered_data['Total Amount /SKU (Inclusive Commission)'].sum()

        # **Key Metrics**
        with metrics_col:
            st.markdown('<p class="header-font">🧐 Key Metrics</p>', unsafe_allow_html=True)
            st.info(f"**Unique Reference Count:** {unique_reference_count}")
            st.info(f"**Total Amount:** ${total_amount:,.2f}")

        # **Donut Chart - Status vs Unique Reference No (Filtered data)**
        status_counts = filtered_data.groupby("Status")["Reference_No"].nunique().reset_index()

        # Define color mapping for statuses
        status_colors = {"Reached": "023047", "Awaited": "ffb703"}

        fig_donut = px.pie(
            status_counts, values="Reference_No", names="Status", 
            hole=0.4, title="Container Count by Status", 
            color="Status", color_discrete_map=status_colors
        )

        # Add an outside border to the donut chart (border around the whole chart)
        fig_donut.update_layout(
            font=dict(size=12),  # Adjust font size if needed
            margin=dict(t=50, b=50, l=50, r=50), title_x = 0.3,) # Add margin around the plot )
        
        # **Display Donut Chart**
        with donut_col:
            st.plotly_chart(fig_donut, use_container_width=True)

        # Group data by "Month Year" and count unique "Reference_No"
        monthly_counts = filtered_data.groupby("Month Year")["Reference_No"].nunique().reset_index()

        # Create line chart
        fig_line = px.line( monthly_counts,
                            x="Month Year", y="Reference_No",
                            title="Container Count by Month Year", markers=True,  # Show data points
                            line_shape="linear",        )

        # Enhance styling
        fig_line.update_traces(
            mode='lines+markers+text',  # Show lines, markers, and text labels
            text=monthly_counts['Reference_No'].apply(lambda x: f"{x:,}"),  # Format numbers with commas
            textposition='top center',
            marker=dict(size=8, color='#0D4C92'),  # Adjust marker size and color
            line=dict(color='#0D4C92', width=3))  # Adjust line color and thickness

        # Improve layout
        fig_line.update_layout(
            xaxis_title="Month Year",
            yaxis_title="Unique Container Count",
            xaxis_tickangle=-45,  # Rotate x-axis labels for readability
            title_x=0.35,  # Center title
            title_y=0.95,
            margin=dict(l=20, r=50, t=50, b=100),)  # Adjust margins

        # Display the chart in Streamlit with full width
        st.plotly_chart(fig_line, use_container_width=True)

        # **Ensure date columns are in datetime format before formatting**
        date_columns = ["Dispatched Date from WH", "Departure Date from Port", "Arrival Date on Port", "Main Delivery Date"]

        for col in date_columns:
            if col in filtered_data.columns:
                filtered_data[col] = pd.to_datetime(filtered_data[col], errors='coerce')  # Convert to datetime
                filtered_data[col] = filtered_data[col].dt.strftime('%d-%b-%y')  # Format as 'DD-MMM-YY'

        # Drop 'Month_Year' column if it exists
        filtered_data = filtered_data.drop(columns=['Month_Year', 'Main_Container No.', 'Aging', ], errors='ignore')

        # **Display Filtered Container Data as a Table**
        st.markdown("""
            <p style="background-color: #4CAF50; color: white; padding: 10px; border-radius: 50px; text-align: center; font-weight: bold;">
                Container Data
            </p>
            """, unsafe_allow_html=True)
        st.dataframe(filtered_data, width=2500, height=500, use_container_width=True, hide_index=None)

        # Add some spacing
        st.markdown("---")     

## --------------------------------------------------------------------------- for amazon shipment-------------------------------------------------------------------------------------
        # **Set Style for Headers with White Banner**
        st.markdown("""
            <style>
                .banner {
                    background-color: white;  /* White background */
                    color: black;  /* Black text */
                    font-size: 28px;  /* Adjust font size */
                    font-weight: bold;
                    text-align: center;  /* Center align */
                    padding: 10px;  /* Add padding for better spacing */
                    border-radius: 0px;  /* Rounded corners */
                    border: 2px solid black;  /* Black border for emphasis */
                }
            </style>
        """, unsafe_allow_html=True)

        # **Display Header with Banner**
        st.markdown('<div class="banner">Amazon Shipments</div>', unsafe_allow_html=True)

        # **Define Layout: Filters Next to Charts**
        col1, col2, col3 = st.columns([9, 9, 4])  # Allocate space for Charts and Filters

        # **Filters Section**
        with col3:
            st.markdown('<p class="header-font">Filters</p>', unsafe_allow_html=True)

            # SKU Filter
            unique_skus = amazon_shipment["Merchant_SKU"].unique()
            selected_skus = st.multiselect("Select SKU(s):", options=["All"] + list(unique_skus), default=["All"])

            # Reference No. Filter
            unique_references = amazon_shipment["Reference No."].unique()
            selected_refs = st.multiselect("Select Reference No(s):", options=["All"] + list(unique_references), default=["All"])

            # Country Filter
            unique_countries = amazon_shipment["Country"].unique()
            selected_countries = st.multiselect("Select Country:", options=["All"] + list(unique_countries), default=["All"])

            # Status Filter
            unique_status = amazon_shipment["Status"].unique()
            selected_status = st.multiselect("Select Status:", options=["All"] + list(unique_status), default=["All"])

        # **Filter Data Based on Selections**
        amazon_shipment = amazon_shipment.copy()

        if "All" not in selected_skus:
            amazon_shipment = amazon_shipment[amazon_shipment["SKU"].isin(selected_skus)]

        if "All" not in selected_refs:
            amazon_shipment = amazon_shipment[amazon_shipment["Reference No."].isin(selected_refs)]

        if "All" not in selected_countries:
            amazon_shipment = amazon_shipment[amazon_shipment["Country"].isin(selected_countries)]

        if "All" not in selected_status:
            amazon_shipment = amazon_shipment[amazon_shipment["Status"].isin(selected_status)]

        # **Column Chart - Unique Shipment Name by Country**
        shipment_counts = amazon_shipment.groupby("Country")["Reference No."].nunique().reset_index()

        fig_col = px.bar(
            shipment_counts, x="Country", y="Reference No.", 
            title="Unique Shipments by Country", text_auto=True, color="Country"  )

        # **Donut Chart - Status by Unique Shipment Name**
        status_counts = amazon_shipment.groupby("Status")["Reference No."].nunique().reset_index()

        fig_donut = px.pie(
            status_counts, values="Reference No.", names="Status", 
            title="Shipment Status Distribution", hole=0.4, color="Status" )

        # **Display Charts with Filters Side-by-Side**
        with col1:
            st.plotly_chart(fig_col, use_container_width=True)

        with col2:
            st.plotly_chart(fig_donut, use_container_width=True)

        # **Filtered Data Table**
        st.markdown("""
            <p style="background-color: #4CAF50; color: white; padding: 10px; border-radius: 50px; text-align: center; font-weight: bold;">
                Amazon Shipment
            </p>
            """, unsafe_allow_html=True)
        st.dataframe(amazon_shipment, width=2500, height=500, use_container_width=True, hide_index=None)

        # Add some spacing
        st.markdown("---")      

# __________________________________________________________________________ for Warehouses(3G & Updike) ____________________________________________________________________________________________
    with tab3:  # Warehouses

        # Create two columns to align subheader and navigation pills on the same line
        col1, col2, col3 = st.columns([0.43, 0.25, 0.25])

        with col1:
            st.subheader("Select Warehouse🏭 →")

        # Display logos as clickable buttons (images)
        st.markdown("""   <style>.logo-container { display: flex;  justify-content: space-evenly;  padding: 10px; }
        .logo-container img { height: 100px; cursor: pointer; border-radius: 5px;    border: 2px solid #000;  }</style> """, unsafe_allow_html=True)

        # Logo container with clickable images for 3G and Updike
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)

        # Logo for 3G
        with col2:
            if st.button("3G Warehouse"):
                st.session_state.page = "3G Details"
        # Logo for Updike
        with col3:
            if st.button("Updike Warehouse"):
                st.session_state.page = "Updike Details"       # Page to show Updike content

        st.markdown('</div>', unsafe_allow_html=True)   

        # Logo container with clickable images for 3G and Updike
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)

        # Show respective pages based on session state
        if st.session_state.get('page') == '3G Details':
            st.markdown(""" <div style="margin: 20px 0;"> <div class="banner">3G Warehouse Details</div>
            </div> <style> .banner {  background-color: white;  /* White background */
            color: black;  /* Black text */
            font-size: 25px;  /* Adjust font size */
            font-weight: bold; text-align: center;  /* Center align */
            padding: 8px;  /* Add padding for better spacing */ border-radius: 5px;  /* Rounded corners */
            border: 1px solid black;  /* Black border for emphasis */ </style> """, unsafe_allow_html=True) 

            # Navigation Links for Inventory and Orders Tracking
            st.markdown("""
            <div style="padding: 10px; border-radius: 5px; text-align: center; display: flex; justify-content: space-evenly;">
                <a href="#Sellable Inventory" style="font-size: 18px; text-decoration: none; color:rgb(4, 192, 35); margin-right: 20px;">Sellable Inventory</a> |
                <a href="#Ageing Report" style="font-size: 18px; text-decoration: none; color:rgb(4, 192, 35); margin-left: 20px;">Ageing Report</a> |
                <a href="#Orders Oubound Report" style="font-size: 18px; text-decoration: none; color:rgb(4, 192, 35); margin-left: 20px;">Orders Oubound Tracking</a>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("---")  # Add a horizontal rule
            
            # Remove 'Sample' SKU
            threeg_db = threeg_db[threeg_db['SKU'] != "Sample"]

            # Convert Date column to datetime and get the latest date
            threeg_db['Date'] = pd.to_datetime(threeg_db['Date'])
            latest_date = threeg_db['Date'].max().strftime('%d-%b-%y')

            # Rename columns for clarity
            threeg_db = threeg_db.rename(columns={
                "$Sellable_Box": "Sellable Stock Value (box)",
                "$On_Hand_Box": "Total 3G Stock Value (box)",
                "$Reserved_Box": "Reserved Stock Value (box)",
                "3G On Hand": "Total 3G Stock (case)",
                "3G Committed": "Reserved Stock (case)",
                "3G Fulfillable": "Sellable Stock (case)"        })

            # Calculate the total for key metrics
            total_sellable_box = threeg_db['Sellable Stock Value (box)'].sum()
            total_on_hand_box = threeg_db['Total 3G Stock Value (box)'].sum()
            total_reserved_box = threeg_db['Reserved Stock Value (box)'].sum()
            total_3g_on_hand = threeg_db['Total 3G Stock (case)'].sum()
            total_3g_committed = threeg_db['Reserved Stock (case)'].sum()
            total_3g_fulfillable = threeg_db['Sellable Stock (case)'].sum()

                    # Display key metrics
            metrics_col, chart_col, filter_col = st.columns([4, 9, 3])

            with metrics_col: # Info box 
                st.markdown('<p class="header-font">🧐 Key Metrics</p>', unsafe_allow_html=True)

                st.markdown(f"""<div style="background-color: #e7ecef; padding: 10px; border-radius: 5px; width: 200px; color: black; text-align: center; height: 70px; margin-bottom: 15px;">
                                <strong>Total 3G Stock Value (box): ${total_on_hand_box:,.2f} cases </div>""", unsafe_allow_html=True)

                st.markdown(f"""<div style="background-color: #e7ecef; padding: 10px; border-radius: 5px; width: 200px; color: black; text-align: center; height: 70px; margin-bottom: 15px;">
                                <strong>Sellable Stock Value (box): ${total_sellable_box:,.2f} cases </div>""", unsafe_allow_html=True)
                        
                st.markdown(f"""<div style="background-color: #e7ecef; padding: 10px; border-radius: 5px; width: 200px; color: black; text-align: center; height: 70px; margin-bottom: 15px;">
                                <strong>Reserved Stock Value (box): ${total_reserved_box:,.2f} cases </div>""", unsafe_allow_html=True)
                
                st.markdown(f"""<div style="background-color: #e7ecef; padding: 10px; border-radius: 5px; width: 200px; color: black; text-align: center; height: 70px; margin-bottom: 15px;">
                                <strong>Total 3G Stock (case): {total_3g_on_hand:,.2f} cases </div>""", unsafe_allow_html=True)
                
                st.markdown(f"""<div style="background-color: #e7ecef; padding: 10px; border-radius: 5px; width: 200px; color: black; text-align: center; height: 70px; margin-bottom: 15px;">
                                <strong>Sellable Stock (case): {total_3g_fulfillable:,.2f} cases </div>""", unsafe_allow_html=True)
                
                st.markdown(f"""<div style="background-color: #e7ecef; padding: 10px; border-radius: 5px; width: 200px; color: black; text-align: center; height: 70px; margin-bottom: 15px;">
                                <strong>Reserved Stock (case): {total_3g_committed:,.2f} cases </div>""", unsafe_allow_html=True)

            # Create SKU and Material filters
            with filter_col:
                st.markdown('<p class="header-font">Filters</p>', unsafe_allow_html=True)
                # Create SKU and Material filters
                unique_skus = threeg_db["SKU"].unique()
                sku_filter = st.multiselect("Select SKU(s):", options=["All"] + list(unique_skus), default=["All"])

                unique_material = threeg_db["Material"].unique()
                material_filter = st.multiselect("Select Material:", options=["All"] + list(unique_material), default=["All"])

            # Apply filters to data
            filtered_data = threeg_db.copy()
            if "All" not in sku_filter:
                filtered_data = filtered_data[filtered_data['SKU'].isin(sku_filter)]
            if "All" not in material_filter:
                filtered_data = filtered_data[filtered_data['Material'].isin(material_filter)]

                # Filter data based on SKU and Material
                if "All" not in sku_filter:
                    threeg_db = threeg_db[threeg_db['SKU'].isin(sku_filter)]
                if "All" not in material_filter:
                    threeg_db = threeg_db[threeg_db['Material'].isin(material_filter)]

            # Group by 'Material' and sum values for Total 3G Stock Value (box)
            material_summary = threeg_db.groupby('Material').agg({'Sellable Stock Value (box)': 'sum', 'Total 3G Stock Value (box)': 'sum',
                                                                    'Reserved Stock Value (box)': 'sum'        }).reset_index()

            # Create stacked bar chart for Material vs Total 3G Stock Value (box)
            with chart_col:
                fig = px.bar(
                    material_summary,
                    x="Material",
                    y="Total 3G Stock Value (box)",
                    text="Total 3G Stock Value (box)",  # Show values on bars
                    labels={"Material": "Material", "value": "Stock Value (box)"},
                    color = "Material",
                    color_discrete_sequence=px.colors.qualitative.D3,  # Use predefined color scheme
                    #barmode='group',  # Cluster the bars (group them side by side)
                    title="Material vs Total Stock Value (box)",
                    height=500 )
                
                # Update the layout and format the text values
                fig.update_traces(
                    texttemplate='$%{y:,.0f}',  # Display whole numbers with $ sign
                    textposition='outside',  # Show the labels outside bars for better visibility
                    hovertemplate="Material: %{x}<br>Total Stock Value: $%{y:,.0f}<extra></extra>" ) # Format hover values
                    
                # Update layout for stacked chart with borders
                fig.update_layout(
                    xaxis_title=None,  # Remove x-axis label
                    yaxis_title=None,  # Remove y-axis label
                    xaxis_tickangle=0,  # Rotate x labels for readability
                    title_x=0.35,  # Center the title horizontally
                    title_y=0.95,  # Adjust vertical alignment for the title
                    margin=dict(l=20, r=20, t=50, b=100),  # Adjust margins
                )

                # Display the Plotly chart in Streamlit
                st.plotly_chart(fig, use_container_width=True)

            st.write("") # Add some spacing

            st.markdown("""<a id="Sellable Inventory"></a>""", unsafe_allow_html=True)  # Anchor for Inventory
            st.markdown(f"""
                    <p style="background-color: #0D4C92; color: white; padding: 10px; border-radius: 50px; text-align: center; font-weight: bold;">
                        Sellable Inventory as of ({latest_date})
                    </p>
                """, unsafe_allow_html=True)
            # Prepare the table with relevant columns for display
            threeg_dbms = threeg_db.loc[:, ['SKU', 'Material', 'Total 3G Stock (case)', 'Sellable Stock (case)', 'Reserved Stock (case)', 
                                            '3G_to_Amazon_CA', '3G_to_Amazon_US', 'Amazon', 'Retail', 'Walmart', 'Samples']]
            st.dataframe(threeg_dbms, width=2500, height=500, use_container_width=True, hide_index=None)    

            # Group by 'Material' and sum the 'Sellable' values
            threeg_dbms = threeg_db.groupby('Material')['Sellable Stock (case)'].sum().reset_index()

            # Rename column for clarity
            threeg_dbms = threeg_dbms.rename(columns={"Sellable Stock (case)": "Sellable"})

            # Handle missing values in 'Material' column
            threeg_dbms = threeg_dbms.dropna(subset=['Material'])  # Remove rows where Material is NaN
            threeg_dbms['Material'] = threeg_dbms['Material'].astype(str)  # Convert to string
            total_sellable = threeg_dbms['Sellable'].sum()

            # Create bar chart using Plotly for Sellable Stock
            fig = px.bar(
                threeg_dbms,
                x="Material",
                    y="Sellable",
                    text="Sellable",  # Show values on bars
                    title="Material vs Sellable",
                    color_discrete_sequence=px.colors.qualitative.Dark2  # Automatic color scale (you can change it to other scales like 'Viridis', 'Cividis', etc.)
                )

                # Update layout for better visualization
            fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')  # Format text
            fig.update_layout(
                    xaxis_title=None,  # Remove x-axis label
                    yaxis_title=None,  # Remove y-axis label
                    xaxis_tickangle=0,  # Rotate x labels for readability
                    title_x=0.5,  # Center the title
                    title_y=0.95,  # Adjust vertical alignment for the title
                    margin=dict(l=20, r=20, t=50, b=100),  # Adjust margins
                )

                # Display the Plotly chart in Streamlit
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")  # Add a horizontal rule

    ## ====================================================================  3G Inventory Ageing ===================================================================================
            # Display the latest date in a formatted header
            st.markdown("""<a id="Ageing Report"></a>""", unsafe_allow_html=True)  # Anchor for Ageing Inventory

            st.markdown(f"""<p style="background-color: #0D4C92; color: white; padding: 10px; border-radius: 50px; text-align: center; font-weight: bold;">
                        Inventory Ageing ({latest_date})  </p> """, unsafe_allow_html=True)
                # **Step 2: SKU Filter next to Aged Inventory Matrix**
            matrix_col, filter_col = st.columns([3, 1])  # Adjust width ratio as needed

            with filter_col:
                st.markdown("### Filter")  
                unique_skus = threeg_age["SKU"].unique()
                    
                # Multi-select with "All" option
                selected_skus = st.multiselect("Select SKU(s):", options=["All"] + list(unique_skus), default=["All"])

            # **Step 3: Apply SKU Filter BEFORE Displaying Data**
            if "All" in selected_skus or not selected_skus:
                filtered_data = threeg_age.copy()  # Keep all SKUs
            else:
                    filtered_data = threeg_age[threeg_age["SKU"].isin(selected_skus)]

            st.write("")

                # **Step 4: Display the filtered table** Agring Table
            st.markdown('<p class="header-font" style="font-size:20px; font-weight:bold;">3G Inventory Ageing (Cases)</p>', unsafe_allow_html=True)
            # Drop unnecessary columns
            filtered_data = filtered_data.drop(columns=['Report', 'Date'], errors='ignore')
            st.dataframe(filtered_data, width=2500, height=500, use_container_width=True, hide_index=None)

            st.markdown("---")  # Add a horizontal rule

            with matrix_col: # Info box
                st.markdown('<p class="header-font" style="font-size:20px; font-weight:bold;">Aged Inventory (Cases)</p>', 
                                unsafe_allow_html=True)

                # Ensure numeric column selection
                numeric_columns = filtered_data.select_dtypes(include=["number"]).columns
                totals = filtered_data[numeric_columns].sum()

                # Define column order
                column_order = ["30 Days", "31-60", "61-90", "91-120", "121-150", 
                                    "151-180", "181-365", "1yr-2yr", "2yr-3yr", "+3yr"]

               # Display infoboxes in a 5x2 layout
                rows = [column_order[i:i + 5] for i in range(0, len(column_order), 5)]

                for row in rows:
                    cols = st.columns(len(row))
                    for idx, col_name in enumerate(row):
                        with cols[idx]:
                            value = totals.get(col_name, 0)  # Avoid KeyError
                            # box color based on value
                            if col_name in ["151-180", "181-365", "1yr-2yr", "2yr-3yr", "+3yr"]:
                                st.markdown(f"""<div style="background-color: #e63946; padding: 10px; border-radius: 10px;color: white; text-align: center;
                                                height: 90px;margin-bottom: 15px;">
                                                <strong>Aged Stock:</strong><br><strong>{col_name}</strong></br>{value:,.0f} cases</div>""", unsafe_allow_html=True)
                            else:
                                st.markdown(f"""<div style="background-color: #588157; padding: 10px; border-radius: 10px;color: white; text-align: center;
                                            height: 90px;margin-bottom: 15px;"> <strong>Aged Stock:</strong>
                                            <br><strong>{col_name}</strong></br>{value:,.0f} cases""", unsafe_allow_html=True)

    ## ==================================================================== 3g orders data ========================================================================================
            # Display the order header
            st.markdown("""<a id="Orders Oubound Report"></a>""", unsafe_allow_html=True)  # Anchor for Ageing Inventory

            st.markdown(f"""<p style="background-color: #0D4C92; color: white; padding: 10px; border-radius: 50px; text-align: center; font-weight: bold;">
                            3G Orders Tracking </p> """, unsafe_allow_html=True)

            # Rename columns for clarity
            threeg_orders = threeg_orders.rename(columns={
                "Reference_No": "Reference No", "Closed_Date": "Order Closed Date", "Creation_Date": "Order Create Date", 
                "Qty_out_3G": "Outbound Qty (case)", 'PoNum': 'PO Number',
                "ship_Box_3G": "Outbound Qty (box)", "RCVD_Qty": "Received Qty (box)", '3G_Status': 'Status' })

            # Separate closed and non-closed orders
            closed_orders = threeg_orders[threeg_orders["Status"] == "Closed"]
            pivot_closed = closed_orders.pivot_table(
                index=["Company",'Reference No','PO Number', 'SKU','Material', "Order Closed Date"],
                values=["Outbound Qty (case)", "Outbound Qty (box)", "Received Qty (box)"],
                aggfunc="sum").reset_index()

            # **1️⃣ Filter Controls in a Single Row with padding**
            filters = st.container()
            with filters:
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                
                with col1:
                    company_filter = st.multiselect("Shipped Company", options=["All"] + list(threeg_orders['Company'].unique()), default=["All"])
                with col2:
                    reference_no_filter = st.multiselect("Select Reference No", options=["All"] + list(threeg_orders['Reference No'].unique()), default=["All"])
                with col3:
                    po_number_filter = st.multiselect("Select PO Number", options=["All"] + list(threeg_orders['PO Number'].unique()), default=["All"])
                with col4:
                    sku_filter = st.multiselect("Select SKU", options=["All"] + list(threeg_orders['SKU'].unique()), default=["All"])
                with col5:
                    material_filter = st.multiselect("Select Material", options=["All"] + list(threeg_orders['Material'].unique()), default=["All"])
                with col6:
                    status_filter = st.multiselect("Select Status", options=["All"] + list(threeg_orders['Status'].unique()), default=["All"])

                # Add padding to the filters
                for column in [col1, col2, col3, col4, col5, col6]:
                    column.markdown("<style>div[data-testid='stSelectbox']{padding:10px;}</style>", unsafe_allow_html=True)

            # **2️⃣ Filter the Non-Closed Orders**
            non_closed_orders = threeg_orders[threeg_orders["Status"] != "Closed"]

            # Apply filters to non-closed orders
            filtered_non_closed_orders = non_closed_orders[
                (non_closed_orders['Company'].isin(company_filter) | (company_filter == ["All"])) &
                (non_closed_orders['Reference No'].isin(reference_no_filter) | (reference_no_filter == ["All"])) &
                (non_closed_orders['PO Number'].isin(po_number_filter) | (po_number_filter == ["All"])) &
                (non_closed_orders['SKU'].isin(sku_filter) | (sku_filter == ["All"])) &
                (non_closed_orders['Material'].isin(material_filter) | (material_filter == ["All"])) &
                (non_closed_orders['Status'].isin(status_filter) | (status_filter == ["All"]))
            ]

            # **3️⃣ Display Non-Closed Orders (Filtered)**
            st.markdown("### 3G Open Orders")
            st.dataframe(filtered_non_closed_orders.loc[:, ['Reference No', 'PO Number','SKU', 'Material', 'Outbound Qty (case)', 'Outbound Qty (box)',
                                                            'Company', 'Status', 'Order Create Date']], use_container_width=True, hide_index=True)

            # **4️⃣ Filter the Pivoted Closed Orders**
            filtered_pivot_closed = pivot_closed[
                (pivot_closed['Company'].isin(company_filter) | (company_filter == ["All"])) &
                (pivot_closed['Reference No'].isin(reference_no_filter) | (reference_no_filter == ["All"])) &
                (pivot_closed['PO Number'].isin(po_number_filter) | (po_number_filter == ["All"])) &
                (pivot_closed['SKU'].isin(sku_filter) | (sku_filter == ["All"])) &
                (pivot_closed['Material'].isin(material_filter) | (material_filter == ["All"])) &
                (pivot_closed['Order Closed Date'].isin(status_filter) | (status_filter == ["All"]))
            ]

            # **5️⃣ Display Pivot Table for "Closed" 3G_Status (Filtered)**
            st.markdown("### 3G Closed Orders")
            st.dataframe(filtered_pivot_closed.loc[:, ["Company", 'Reference No', 'PO Number', 'SKU', 'Material', "Order Closed Date",
                                                        "Outbound Qty (case)", "Outbound Qty (box)", "Received Qty (box)"]], use_container_width=True)

            st.markdown("---")  # Add a horizontal rule
            
# ------------------------------------------------------------------------ Updike -----------------------------------------------------------------------------------------------------------
        
        elif st.session_state.get('page') == 'Updike Details':
            st.markdown(""" <div style="margin: 20px 0;"> <div class="banner">Updike Warehouse Details</div>
                        <style> .banner {  background-color: white;  /* White background */
                        color: black;  /* Black text */ font-size: 25px;  /* Adjust font size */ 
                        font-weight: bold; text-align: center;  /* Center align */
                        padding: 8px;  /* Add padding for better spacing */ border-radius: 5px;  /* Rounded corners */
                        border: 1px solid black;  /* Black border for emphasis */ </style> """, unsafe_allow_html=True) 
            
            # Navigation Links for Inventory and Orders Tracking
            st.markdown("""<div style="padding: 10px; border-radius: 5px; text-align: center;">
                <a href="#Updike Inventory" style="font-size: 18px; text-decoration: none; color:rgb(4, 192, 35); margin-right: 20px;">Updike Inventory</a> |
                <a href="#Updike Orders" style="font-size: 18px; text-decoration: none; color:rgb(4, 192, 35); margin-left: 20px;">Updike Orders Tracking</a> </div>""", unsafe_allow_html=True)

            st.markdown("---")  # Add a horizontal rule

            st.markdown("""<a id="Updike Inventory"></a>""", unsafe_allow_html=True)  # Anchor for updike Inventory

            st.markdown('<p class="header-font" style="font-size:20px; font-weight:bold;">Updike Inventory Report</p>', unsafe_allow_html=True)

            # Rename columns for clarity
            updike_db = updike_db.rename(columns={"$Sellable": "Sellable Stock Value (box)", "Updike On Hand": "Total Updike Stock (case)",
                                                "Updike Comitted": "Reserved Stock (case)", "Updike Sellable": "Sellable Stock (case)",
                                                'Amazon Incoming From Updike' : 'Amazon', 'Retail Committed Updike' : 'Retail',
                                                'Walmart Incoming From Updike' : 'Walmart', 'Shipbob Incoming From Updike' : 'Shipbob' })
            
            # **Step 2: SKU Filter next to Inventory Matrix**
            matrix_col, filter_col = st.columns([3, 1])  # Adjust width ratio as needed

            with filter_col:
                st.markdown('<p class="header-font" style="font-size:20px; font-weight:bold;">Filter</p>', unsafe_allow_html=True)  
                unique_skus = updike_db["SKU"].unique()
                    
                # Multi-select with "All" option
                selected_skus = st.multiselect("Select SKU(s):", options=["All"] + list(unique_skus), default=["All"])
                selected_materials = st.multiselect("Select Material(s):", options=["All"] + list(updike_db["Material"].unique()), default=["All"])

            # **Step 3: Apply SKU Filter BEFORE Displaying Data**
            if "All" not in selected_skus:
                updike_db = updike_db[updike_db["SKU"].isin(selected_skus)]

            if "All" not in selected_materials:
                updike_db = updike_db[updike_db["Material"].isin(selected_materials)]

            st.write("")

            # Display the filtered table** sellable Table
            st.markdown(f"""<p style="background-color: #0D4C92; color: white; padding: 10px; border-radius: 50px; text-align: center; font-weight: bold;">
                        Sellable Inventory as of: {updike_db.Date.max()}</p> """, unsafe_allow_html=True)            
            # Drop unnecessary columns
            updike_db = updike_db.drop(columns=['Report', 'Date'], errors='ignore')
            st.dataframe(updike_db.loc[:,['SKU','Material', 'Total Updike Stock (case)','Sellable Stock (case)','Reserved Stock (case)',
                                        'Amazon','Retail','Shipbob', 'Walmart']], width=2500, height=500, use_container_width=True, hide_index=None) 

            st.markdown("---")  # Add a horizontal rule

            with matrix_col: # Info box
                st.markdown('<p class="header-font" style="font-size:20px; font-weight:bold;">🧐 Key Metrics</p>', unsafe_allow_html=True)

                # Ensure numeric column selection
                numeric_columns = updike_db.select_dtypes(include=["number"]).columns
                totals = updike_db[numeric_columns].sum()

                # Define column order
                column_order = ['Sellable Stock Value (box)','Sellable Stock (case)','Reserved Stock (case)','Amazon','Retail','Shipbob', 'Walmart', ]

               # Display infoboxes in a 5x2 layout
                rows = [column_order[i:i + 3] for i in range(0, len(column_order), 3)]

                for row in rows:
                    cols = st.columns(len(row))
                    for idx, col_name in enumerate(row):
                        with cols[idx]:
                            value = totals.get(col_name, 0)  # Avoid KeyError
                            # box color based on value
                            if col_name in ['Amazon','Retail','Shipbob', 'Walmart']:
                                st.markdown(f"""<div style="background-color: #e63946; padding: 10px; border-radius: 10px;color: white; text-align: center;
                                                height: 90px;margin-bottom: 15px;"> <strong>Reserve for:</strong><br><strong>{col_name}</strong></br>{value:,.0f} cases</div>""",
                                                unsafe_allow_html=True)
                            else:
                                st.markdown(f"""<div style="background-color: #588157; padding: 10px; border-radius: 10px;color: white; text-align: center;
                                            height: 90px;margin-bottom: 15px;"> <strong>Updike:</strong> <br><strong>{col_name}</strong></br>{value:,.0f} cases""", unsafe_allow_html=True)

            # Group by 'Material' and sum values for Total Updike Stock Value (box)
            material_summary = updike_db.groupby('Material').agg({'Sellable Stock Value (box)': 'sum',}).reset_index()

            # Create bar chart
            fig_col = px.bar(
                material_summary,
                x="Material",
                y="Sellable Stock Value (box)",
                title="Sellable Stock Value (box) by Material",
                text_auto=True,  # Auto-display values on bars
                color="Material",  # Color bars by Material 
                color_discrete_sequence=px.colors.qualitative.D3,)  # Improve color differentiation

            # Enhance styling
            fig_col.update_traces(
                texttemplate='$%{y:,.0f}',  # Format numbers with commas
                textposition='outside',  # Display text above bars
                marker=dict(line=dict(width=1, color='black')),)  # Add bar borders for clarity
                    
            # Update layout for stacked chart with borders
            fig_col.update_layout(
                    xaxis_title=None,
                    yaxis_title="Sellable Stock boxes Value",
                    xaxis_tickangle=0,  # Rotate x-axis labels for readability
                    title_x=0.35,  # Center title
                    title_y=0.95,
                    margin=dict(l=20, r=20, t=50, b=100),)

            # Display the Plotly chart in Streamlit
            st.plotly_chart(fig_col, use_container_width=True)


#==================================================================== Updike orders Tracking Report===================================================================================
            st.markdown("""<a id="Updike Orders"></a>""", unsafe_allow_html=True)  # Anchor for updike Inventory

            st.markdown(f"""<p style="background-color: #0D4C92; color: white; padding: 10px; border-radius: 50px; text-align: center; font-weight: bold;">
                            Updike Orders Tracking </p> """, unsafe_allow_html=True)

            # Rename columns for clarity
            updike_orders = updike_orders.rename(columns={
                "Reference_No": "Reference No.", "Order_Closed_Date": "Orders Closed Date", 'Carrier' : 'Shipped Company',
                "Ship_Qty_Updike": "Outbound Qty(case)", "Ship_Qty_Box": "Outbound Qty(box)", "Received_Qty": "Received Qty(box)",
                'Status': 'Updike Status' })

            # Separate closed and non-closed orders
            closed_stats=['Closed','Delivered-Amazon','Delivered-Samples','Delivered-Shipbob','Delivered-ThreeG','Delivered Untracked-Retail',
            'Delivered-Walmart','Delivered-Tradeful','Short Shipped','Over Shipped']

            closed_orders = updike_orders[updike_orders["Updike Status"].isin(closed_stats)]

            pivot_closed = closed_orders.pivot_table(
                index=["Shipped Company",'Reference No.','Updike Status', 'SKU', 'Material', "Orders Closed Date"],
                values=["Outbound Qty(case)", "Outbound Qty(box)", "Received Qty(box)"],
                aggfunc="sum").reset_index()

            # **1️⃣ Filter Controls in a Single Row with padding**
            filters = st.container()
            with filters:
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    company_filter = st.multiselect("Shipped to Company", options=["All"] + list(updike_orders['Shipped Company'].unique()), default=["All"])
                with col2:
                    reference_no_filter = st.multiselect("Reference No", options=["All"] + list(updike_orders['Reference No.'].unique()), default=["All"])
                with col3:
                    sku_filter = st.multiselect("Select SKU(s)", options=["All"] + list(updike_orders['SKU'].unique()), default=["All"])
                with col4:
                    material_filter = st.multiselect("Select Material", options=["All"] + list(updike_orders['Material'].unique()), default=["All"])
                with col5:
                    status_filter = st.multiselect("Select Status", options=["All"] + list(updike_orders['Updike Status'].unique()), default=["All"])

                # Add padding to the filters
                for column in [col1, col2, col3, col4, col5]:
                    column.markdown("<style>div[data-testid='stSelectbox']{padding:10px;}</style>", unsafe_allow_html=True)

            # **2️⃣ Filter the Non-Closed Orders**
            non_closed_orders = updike_orders[~updike_orders["Updike Status"].isin(closed_stats)]

            # Apply filters to non-closed orders
            filtered_non_closed_orders = non_closed_orders[
                (non_closed_orders['Shipped Company'].isin(company_filter) | (company_filter == ["All"])) &
                (non_closed_orders['Reference No.'].isin(reference_no_filter) | (reference_no_filter == ["All"])) &
                (non_closed_orders['SKU'].isin(sku_filter) | (sku_filter == ["All"])) &
                (non_closed_orders['Material'].isin(material_filter) | (material_filter == ["All"])) &
                (non_closed_orders['Updike Status'].isin(status_filter) | (status_filter == ["All"]))  ]

            # **3️⃣ Display Non-Closed Orders (Filtered)**
            st.markdown("### Updike Open Orders")
            st.dataframe(filtered_non_closed_orders.loc[:, ['Reference No.','SKU', 'Material', 'Outbound Qty(case)', 'Outbound Qty(box)',
                                                            'Shipped Company', 'Updike Status']], width=2500, height=500, use_container_width=True, hide_index=True)

            # **4️⃣ Filter the Pivoted Closed Orders**
            filtered_pivot_closed = pivot_closed[
                (pivot_closed['Shipped Company'].isin(company_filter) | (company_filter == ["All"])) &
                (pivot_closed['Reference No.'].isin(reference_no_filter) | (reference_no_filter == ["All"])) &
                (pivot_closed['SKU'].isin(sku_filter) | (sku_filter == ["All"])) &
                (pivot_closed['Material'].isin(material_filter) | (material_filter == ["All"])) &
                (pivot_closed['Updike Status'].isin(status_filter) | (status_filter == ["All"]))   ]

            # **5️⃣ Display Pivot Table for "Closed" updike_Status (Filtered)**
            st.markdown("### Updike Closed Orders")
            st.dataframe(filtered_pivot_closed.loc[:, ['Reference No.','SKU', 'Material', 'Outbound Qty(case)', 'Outbound Qty(box)',
                                                            'Shipped Company', 'Updike Status', 'Orders Closed Date']], width=2500, height=500, use_container_width=True, hide_index=True)

            # Group data by "Shipped Company" and count unique "Reference No."
            shipment_counts = filtered_pivot_closed.groupby("Shipped Company")["Reference No."].nunique().reset_index()

            # Create bar chart
            fig_col = px.bar(
                shipment_counts,
                x="Shipped Company",
                y="Reference No.",
                title="Closed Shipments Count by Channels",
                text_auto=True,  # Auto-display values on bars
                color="Shipped Company",
                color_discrete_sequence=px.colors.qualitative.D3,)  # Improve color differentiation

            # Enhance styling
            fig_col.update_traces(
                texttemplate='%{y:,}',  # Format numbers with commas
                textposition='outside',  # Display text above bars
                marker=dict(line=dict(width=1, color='black')),)  # Add bar borders for clarity

            # Improve layout
            fig_col.update_layout(
                xaxis_title="Shipped Company",
                yaxis_title="Unique Shipment Count",
                xaxis_tickangle=0,  # Rotate x-axis labels for readability
                title_x=0.35,  # Center title
                title_y=0.95,
                margin=dict(l=20, r=20, t=50, b=100),)  # Adjust margins

            # Display the chart in Streamlit with full width
            st.plotly_chart(fig_col, use_container_width=True)

            
            # Chart 2️⃣ Group data by "Shipped Status" and count unique "Reference No."
            shipment_counts = filtered_pivot_closed.groupby("Updike Status")["Reference No."].nunique().reset_index()

            # Create bar chart
            fig_col = px.bar(
                shipment_counts,
                x="Updike Status",
                y="Reference No.",
                title="Shipments Count by Closed Status",
                text_auto=True,  # Auto-display values on bars
                color="Updike Status",
                color_discrete_sequence=px.colors.qualitative.D3,)  # Improve color differentiation

            # Enhance styling
            fig_col.update_traces(
                texttemplate='%{y:,}',  # Format numbers with commas
                textposition='outside',  # Display text above bars
                marker=dict(line=dict(width=1, color='black')),)  # Add bar borders for clarity

            # Improve layout
            fig_col.update_layout(
                xaxis_title=None,
                yaxis_title="Unique Shipment Count",
                xaxis_tickangle=0,  # Rotate x-axis labels for readability
                title_x=0.35,  # Center title
                title_y=0.95,
                margin=dict(l=20, r=20, t=50, b=100),)  # Adjust margins

            # Display the chart in Streamlit with full width
            st.plotly_chart(fig_col, use_container_width=True)            

            st.markdown("---")  # Add a horizontal rule



# __________________________________________________________________________ for Amazon ____________________________________________________________________________________________
    with tab4: # Amazon ( amazon invnetory; Returns, Order report, SKu Trend, Customer Behavior  )
        st.subheader("Amazon🛒🛍 ")
        st.write("Amazon inventory details go here.")

# __________________________________________________________________________ for Retail ____________________________________________________________________________________________
if "page" not in st.session_state:
    st.session_state.page = None

elif main_page == "Retail":
    st.header("Retail Management")
    # Define tabs for navigation
    tab1, tab2, tab3, tab4 = st.tabs(['USA', "India", "Demand & Supply", "Walmart"])

    with tab1: # USA
        st.subheader("Retail USA🛒🛍 ")
    
    # Custom CSS for uniform button width & active button highlighting
        st.markdown(f""" <style>
                    div.stButton > button {{ width: 100px !important;  /* Set button width */
                        height: 40px !important; /* Set button height */
                        font-size: 16px !important; /* Adjust font size */
                        margin: auto !important; /* Center button */
                        display: flex !important; /* Ensure proper alignment */
                        justify-content: center !important;
                        align-items: center !important;
                        border-radius: 20px !important;  /* Rounded corners */
                        border: 2px solid transparent !important; /* Remove default border */  }}

                    /* Active Button Styling */
                    div.stButton > button.active {{background-color:rgb(233, 50, 26) !important; /* Green highlight */
                        color: white !important; font-weight: bold !important; border: 2px solid rgb(11, 155, 44) !important; /* Dark green border */ }}    </style> """, unsafe_allow_html=True)

        # Function to create styled buttons
        def styled_button(label, page_name):
                    if st.session_state.page == page_name:
                        return st.markdown(f"""<script>document.querySelectorAll("button").forEach(btn => {{ if (btn.innerText === "{label}") {{
                                btn.classList.add("active");}} }});</script>""", unsafe_allow_html=True)
        
        # Create columns for horizontal button alignment
        col1, col2, col3, col4, col5 = st.columns([1, 0.7, 1, 1, 1])  # Equal width columns

        with col1:
            if st.button("Overview", key="overview"):
                st.session_state.page = "Retail USA Overview"
            styled_button("Overview", "Retail USA Overview")

        with col2:
            if st.button("SPS", key="sps"):
                st.session_state.page = "SPS"
            styled_button("SPS", "SPS")

        with col3:
            if st.button("Kehe", key="kehe"):
                st.session_state.page = "Kehe"
            styled_button("Kehe", "Kehe")    

        with col4:
            if st.button("Sprouts", key="sprouts"):
                st.session_state.page = "Sprouts"
            styled_button("Sprouts", "Sprouts")

        with col5:
            if st.button("Costco", key="costco"):
                st.session_state.page = "Costco"
            styled_button("Costco", "Costco")      


## Showing respective data based on the button clicked ======================================== USA Overview =======================================================================
    if st.session_state.get('page') == 'Retail USA Overview':
        st.markdown(""" <div style="margin: 20px 0;"> <div class="banner">Retail SPS Overview</div>
            </div> <style> .banner {  background-color: white;  /* White background */
            color: black;  /* Black text */ font-size: 25px;  /* Adjust font size */
            font-weight: bold; text-align: center;  /* Center align */
            padding: 8px;  /* Add padding for better spacing */ border-radius: 5px;  /* Rounded corners */
            border: 1px solid black;  /* Black border for emphasis */ </style> """, unsafe_allow_html=True)

        retail_overview['year_month_PO'] = pd.to_datetime(retail_overview['year_month_PO'], errors='coerce')
        retail_overview['Common_Invoice_Date'] = pd.to_datetime(retail_overview['Common_Invoice_Date'], errors='coerce')

        retail_overview['Year_PO'] = retail_overview['year_month_PO'].dt.strftime('%Y')  # Format as 'DD-MMM-YY'    
        retail_overview['Year_Invoice'] = retail_overview['Common_Invoice_Date'].dt.strftime('%Y')  # Format as 'DD-MMM-YY'    

        # Key Metrics Calculation
        total_unique_po = retail_overview["PO_Number"].nunique()
        total_sku_po_qty = retail_overview["SKU_Qty"].sum()
        total_po_amount = retail_overview["PO_Sales"].sum()
        total_invoice_qty = retail_overview["Invoice_Qty"].sum()
        total_invoice_amount = retail_overview["total_sales"].sum()
        difference_amount = retail_overview['Amt Diff'].sum()

        # Display Key Metrics
        st.subheader("🧐 Key Metrics")
        col1, col2, col3, col4, col5, col6  = st.columns(6)

        # Apply custom styling using HTML inside Markdown
        col1.markdown(f"""<div style="text-align: center; font-weight: bold; background-color:rgb(6, 126, 98); padding: 10px; height: 120px; border-radius: 5px;">
                            <span style="font-size: 16px;">Total PO Served</span><br>
                            <span style="color: white; font-size: 16px;">{total_unique_po}</span></div>""", unsafe_allow_html=True)

        col2.markdown(f"""<div style="text-align: center; font-weight: bold; background-color:rgb(6, 126, 98); padding: 10px; height: 120px; border-radius: 5px;">
                            <span style="font-size: 16px;">PO SKU Qty Asked</span><br>
                            <span style="color: white; font-size: 16px;">{total_sku_po_qty}</span></div>""", unsafe_allow_html=True) 

        col3.markdown(f"""<div style="text-align: center; font-weight: bold; background-color:rgb(6, 126, 98); padding: 10px; height: 120px; border-radius: 5px;">
                            <span style="font-size: 16px;">Invoice Qty Delivered</span><br>
                            <span style="color: white; font-size: 16px;">{total_invoice_qty}</span></div>""", unsafe_allow_html=True)  

        col4.markdown(f"""<div style="text-align: center; font-weight: bold; background-color:rgb(6, 126, 98); padding: 10px; height: 120px; border-radius: 5px;">
                            <span style="font-size: 16px;">Total PO Amount</span><br>
                            <span style="color: white; font-size: 16px;">${total_po_amount:,.2f}</span></div>""", unsafe_allow_html=True)   

        col5.markdown(f"""<div style="text-align: center; font-weight: bold; background-color:rgb(6, 126, 98); padding: 10px; height: 120px; border-radius: 5px;">
                            <span style="font-size: 16px;">Total Invoice Amount</span><br>
                            <span style="color: white; font-size: 16px;">${total_invoice_amount:,.2f}</span></div>""", unsafe_allow_html=True)                                                                                                                                              

        delta_value = round(retail_overview['Qty Diff'].fillna(0).sum(), 2)
        col6.markdown(f""" <div style="text-align: center; font-weight: bold; background-color:rgb(194, 230, 202); padding: 10px; height: 120px; border-radius: 5px;">
                            <span style="font-size: 16px; color: black;">Difference Amount</span><br>
                            <span style="color: red; font-size: 22px;">${difference_amount:,.2f}</span><br>
                            <span style="color: red; font-size: 16px;">🔻 Difference Qty: {delta_value}</span> </div> """, unsafe_allow_html=True )   

        st.markdown("") # Add space between Key Metrics and Charts
        st.markdown("")     

        # Stacked Bar Charts - PO Sales   # Group by 'Year_PO' and sum values for PO_Sales
        figure1 = retail_overview[retail_overview['PO_Status'] != 'Cancelled']
        figure1 = figure1.groupby('Year_PO').agg({'PO_Sales': 'sum'}).reset_index()

        fig1 = px.bar(figure1, x="Year_PO", y="PO_Sales", color="Year_PO", text_auto= True,
                    title="PO Sales by Year-Month", barmode="stack")

        # Stacked Bar Charts - Invoice Sales
        figure2 = retail_overview[retail_overview['Status'] != 'Cancelled']
        figure2 = figure2.groupby('Year_Invoice').agg({'total_sales': 'sum'}).reset_index()

        fig2 = px.bar(figure2, x="Year_Invoice", y="total_sales", color="Year_Invoice",  text_auto= True,
                    title="Invoice Sales by Year-Month", barmode="stack" )

        # Display Side-by-Side Charts
        st.subheader("📊 Sales Analysis")
        col7, col8 = st.columns(2)
        col7.plotly_chart(fig1, use_container_width=True)
        col8.plotly_chart(fig2, use_container_width=True)

        # Column Chart for New_PO_Delivery_Status by Unique PO Count ===============================================================================
        df_status = retail_overview.groupby("New_PO_Delivery_Status")["PO_Number"].nunique().reset_index()
        fig3 = px.bar(df_status, x="New_PO_Delivery_Status", y="PO_Number", color="New_PO_Delivery_Status",
                    title="PO Count by Delivery Status", text_auto=True)
        
        st.plotly_chart(fig3, use_container_width=True)



# __________________________________________________________________________ for Quick Commerce ____________________________________________________________________________________________
elif main_page == "Quick Commerce":
    st.header("Quick Commerce Insights")
    st.write("Details on quick commerce platforms like Blinkit, Flipkart, and Zepto.")

# __________________________________________________________________________ for Zoho ____________________________________________________________________________________________
elif main_page == "Zoho":

        # **Set Style for Headers with White Banner**
        st.markdown("""
            <style>
                .banner {
                    background-color: white;  /* White background */
                    color: black;  /* Black text */
                    font-size: 25px;  /* Adjust font size */
                    font-weight: bold;
                    text-align: center;  /* Center align */
                    padding: 8px;  /* Add padding for better spacing */
                    border-radius: 5px;  /* Rounded corners */
                    border: 1px solid black;  /* Black border for emphasis */
                }
            </style>
        """, unsafe_allow_html=True)
        st.write('<div class="banner">Warehouses Raw Material Stock</div>', unsafe_allow_html=True)

        zoho_pivot = zoho_pivot.drop(columns=['Total'], errors='ignore')
        
        # **Key Metrics Calculation**
        total_banglore = zoho_pivot["Bangalore"].sum() if "Bangalore" in zoho_pivot.columns else 0
        total_muzaf = zoho_pivot["Muzaffarnagar"].sum() if "Muzaffarnagar" in zoho_pivot.columns else 0
        total_noida = zoho_pivot["Noida-63"].sum() if "Noida-63" in zoho_pivot.columns else 0    

        # Display Key Metrics
        st.subheader("🧐 Key Metrics")
        col1, col2, col3 = st.columns(3)
        
        # Apply custom styling using HTML inside Markdown
        col1.markdown(f"""<div style="text-align: center; font-weight: bold; background-color:#003049; padding: 5px; height: 100px; border-radius: 5px;">
                            <span style="font-size: 16px;"> Total RM Bangalore</span><br>
                            <span style="color: white; font-size: 16px;">{total_banglore:,.0f}</span></div>""", unsafe_allow_html=True)
        
        col2.markdown(f"""<div style="text-align: center; font-weight: bold; background-color:#003049; padding: 5px; height: 100px; border-radius: 5px;">
                            <span style="font-size: 16px;">Total RM Noida </span><br>
                            <span style="color: white; font-size: 16px;">{total_noida:,.0f}</span></div>""", unsafe_allow_html=True)      

        col3.markdown(f"""<div style="text-align: center; font-weight: bold; background-color:#003049; padding: 5px; height: 100px; border-radius: 5px;">
                            <span style="font-size: 16px;">Total RM Muzaffarnagar </span><br>
                            <span style="color: white; font-size: 16px;">{total_muzaf:,.0f}</span></div>""", unsafe_allow_html=True)    

        # **Filters in Single Row**
        st.markdown('<p class="header-font">Filters</p>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        # SKU Filter for Parent in both zoho_pivot and zoho_db
        with col1:
            unique_parents = zoho_pivot['Parent'].unique()
            selected_parents = st.multiselect("Select Parent(sku):", options=["All"] + list(unique_parents), default=["All"])  

        # SKU Filter for zoho_db
        with col2:
            unique_skus = zoho_db['SKU'].unique()
            selected_skus = st.multiselect("Select SKU(s):", options=["All"] + list(unique_skus), default=["All"])

        # Warehouse Filter for zoho_db
        with col3:
            unique_warehouses = zoho_db['Warehouse'].unique()
            selected_warehouses = st.multiselect("Select Warehouse:", options=["All"] + list(unique_warehouses), default=["All"])

        # Parent Type Filter for zoho_db
        with col4:
            unique_combination_types = zoho_db['Combination_Type'].unique()
            selected_combination_types = st.multiselect("Select Parent Type:", options=["All"] + list(unique_combination_types), default=["All"])        

        # **Apply Filters to Both DataFrames Based on Relationships**
        if "All" not in selected_parents:
            zoho_pivot = zoho_pivot[zoho_pivot['Parent'].isin(selected_parents)]
            zoho_db = zoho_db[zoho_db['Parent'].isin(selected_parents)]  # Ensure Parent is filtered in zoho_db as well

        if "All" not in selected_skus:
            # Find related Parent(sku) from zoho_db where SKU matches selected SKU
            related_parents = zoho_db[zoho_db['SKU'].isin(selected_skus)]['Parent'].unique()

            # Filter both DataFrames based on related Parent(sku)
            zoho_pivot = zoho_pivot[zoho_pivot['Parent'].isin(related_parents)]
            zoho_db = zoho_db[zoho_db['SKU'].isin(selected_skus)]

        if "All" not in selected_warehouses:
            zoho_db = zoho_db[zoho_db['Warehouse'].isin(selected_warehouses)]

        if "All" not in selected_combination_types:
            zoho_db = zoho_db[zoho_db['Combination_Type'].isin(selected_combination_types)]

        # **Key Metrics Calculation**
        total_banglore = zoho_pivot["Bangalore"].sum() if "Bangalore" in zoho_pivot.columns else 0
        total_muzaf = zoho_pivot["Muzaffarnagar"].sum() if "Muzaffarnagar" in zoho_pivot.columns else 0
        total_noida = zoho_pivot["Noida-63"].sum() if "Noida-63" in zoho_pivot.columns else 0

        # **Data Table for Raw Material as of Today**
        st.markdown("""
            <p style="background-color: #4CAF50; color: white; padding: 10px; border-radius: 50px; text-align: center; font-weight: bold;">
                Raw Material as of Today
            </p>
            """, unsafe_allow_html=True)
        st.dataframe(zoho_pivot, width=2500, height=500, use_container_width=True, hide_index=None)

        st.markdown("---")

        # **Data Table for SKU Associated with Parent**
        st.markdown("""
            <p style="background-color: #4CAF50; color: white; padding: 10px; border-radius: 50px; text-align: center; font-weight: bold;">
                SKU Associated with Parent(sku)
            </p>
            """, unsafe_allow_html=True)
        st.dataframe(zoho_db, width=2500, height=500, use_container_width=True, hide_index=None)


    # __________________________________________________________________________ for Digital Marketing ____________________________________________________________________________________________

elif main_page == "Digital Marketing":
    st.header("Digital Marketing Insights")

    if "page" not in st.session_state:
        st.session_state.page = None

    # Define tabs for navigation
    tab1, tab2, tab3 = st.tabs(['Overview', "Customer Email", "Social Media"])

    with tab1:  # Overview
        st.subheader("Website Traffic Overview 📲")

        # Function to create styled buttons
        def styled_button(label, page_name): 
            if st.session_state.page == page_name:
                return st.markdown(
                    f"""<script>
                    document.querySelectorAll("button").forEach(btn => {{
                        if (btn.innerText === "{label}") {{
                            btn.style.backgroundColor = "#00624E";  /* Active button color */
                            btn.style.color = "white";  /* Active text color */
                        }}
                    }}); </script>""", unsafe_allow_html=True)

        # Create columns for horizontal button alignment
        col1, col2 = st.columns([1, 12])  # Adjust column width

        with col1:
            if st.button("USA", key="USA"):
                st.session_state.page = "USA"
            styled_button("USA", "USA")

        with col2:
            if st.button("India", key="India"):
                st.session_state.page = "India"
            styled_button("India", "India")

        ## Show respective data based on the selected button
        if "page" not in st.session_state:
            st.session_state.page = None
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ USA website email +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        if st.session_state.page == 'USA':
            st.markdown("""
                <div style="margin: 20px 0;"> <div class="banner">USA Website Overview</div>
                </div> <style> .banner {
                        background-color: white;
                        color: black;
                        font-size: 25px;
                        font-weight: bold;
                        text-align: center;
                        padding: 8px;
                        border-radius: 5px;
                        border: 1px solid black; } </style> """, unsafe_allow_html=True)
            
            website_usa = website_customer.copy()
            website_usa = website_usa[website_usa['shipping_country'] != 'India']

            website_usa['month'] = pd.to_datetime(website_usa['month'], errors='coerce')
            website_usa['Year'] = website_usa['month'].dt.strftime('%Y')  # Format as 'DD-MMM-YY'    
            website_usa['Month'] = website_usa['month'].dt.strftime('%b')  # Format as 'DD-MMM-YY'    

            # Key Metrics Calculation
            total_orders = website_usa["order_id"].nunique()
            net_sales = website_usa["net_sales"].sum()
            average_order_value = website_usa["average_order_value"].mean()
            total_customer = website_usa["customer_type"].count()
            return_customer = website_usa[website_usa['customer_type'] == "Returning"].shape[0]
            non_return_customer = website_usa[website_usa['customer_type'] != "Returning"].shape[0]

            # Display Key Metrics
            st.subheader("🧐 Key Metrics")
            col1, col2, col3, col4, col5, col6 = st.columns(6)

            # Apply custom styling using HTML inside Markdown
            col1.markdown(f"""<div style="text-align: center; font-weight: bold; background-color:#003049; padding: 5px; height: 100px; border-radius: 5px;">
                                <span style="font-size: 16px;">Net Sales</span><br>
                                <span style="color: white; font-size: 16px;">${net_sales:,.0f}</span></div>""", unsafe_allow_html=True)

            col2.markdown(f"""<div style="text-align: center; font-weight: bold; background-color:#003049; padding: 5px; height: 100px; border-radius: 5px;">
                                <span style="font-size: 16px;">Avg. Order Value</span><br>
                                <span style="color: white; font-size: 16px;">${average_order_value:,.0f}</span></div>""", unsafe_allow_html=True) 

            col3.markdown(f"""<div style="text-align: center; font-weight: bold; background-color:#003049; padding: 5px; height: 100px; border-radius: 5px;">
                                <span style="font-size: 16px;">Total Orders</span><br>
                                <span style="color: white; font-size: 16px;">{total_orders}</span></div>""", unsafe_allow_html=True)  

            col4.markdown(f"""<div style="text-align: center; font-weight: bold; background-color:#003049; padding: 5px; height: 100px; border-radius: 5px;">
                                <span style="font-size: 16px;">Total Customer Served</span><br>
                                <span style="color: white; font-size: 16px;">{total_customer:,.0f}</span></div>""", unsafe_allow_html=True)   

            col5.markdown(f"""<div style="text-align: center; font-weight: bold; background-color:#003049; padding: 5px; height: 100px; border-radius: 5px;">
                                <span style="font-size: 16px;">Returning Customers</span><br>
                                <span style="color: white; font-size: 16px;">{return_customer:,.0f}</span></div>""", unsafe_allow_html=True)  

            col6.markdown(f"""<div style="text-align: center; font-weight: bold; background-color:#003049; padding: 5px; height: 100px; border-radius: 5px;">
                                <span style="font-size: 16px;">Non-Returning Customers</span><br>
                                <span style="color: white; font-size: 16px;">{non_return_customer:,.0f}</span></div>""", unsafe_allow_html=True)  
            st.markdown("") # Add space between Key Metrics and Charts
            st.markdown("")     

            # Stacked Bar Charts - PO Sales   # Group by 'Year_PO' and sum values for PO_Sales
            figure1 = website_usa.groupby('referring_category').agg({'order_id': 'count'}).reset_index()

            fig1 = px.bar(figure1, x="referring_category", y="order_id", color="referring_category", text_auto= True,
                        title="Referring Category by Order Count", barmode="stack")

            # Stacked Bar Charts - referring_traffic
            #figure2 = retail_overview[retail_overview['Status'] != 'Cancelled']
            figure2 = website_usa.groupby('referring_traffic').agg({'order_id': 'count'}).reset_index()

            fig2 = px.bar(figure2, x="referring_traffic", y="order_id", color="referring_traffic",  text_auto= True,
                        title="Referring Traffic by Order Count", barmode="stack" )

            # Display Side-by-Side Charts
            st.subheader("📊 Analysis")
            col7, col8 = st.columns(2)
            col7.plotly_chart(fig1, use_container_width=True)
            col8.plotly_chart(fig2, use_container_width=True)

            st.markdown("") # Add space between Key Metrics and Charts
            st.markdown("")     

            # Stacked Bar Charts - PO Sales   # Group by 'Year_PO' and sum values for PO_Sales
            figure3 = website_usa.groupby('referrer_source').agg({'order_id': 'count'}).reset_index()

            fig3 = px.bar(figure3, x="referrer_source", y="order_id", color="referrer_source", text_auto= True,
                        title="Referring Source by Order Count", barmode="stack")

            # Stacked Bar Charts - referring_traffic
            #figure2 = retail_overview[retail_overview['Status'] != 'Cancelled']
            figure4 = website_usa.groupby('customer_type').agg({'order_id': 'count'}).reset_index()

            fig4 = px.bar(figure4, x="customer_type", y="order_id", color="customer_type",  text_auto= True,
                        title="Customer Type by Order Count", barmode="stack" )

            # Display Side-by-Side Charts
            col9, col10 = st.columns(2)
            col9.plotly_chart(fig3, use_container_width=True)
            col10.plotly_chart(fig4, use_container_width=True)

            st.markdown("") # Add space between Key Metrics and Charts
            st.markdown("")     

            # Stacked Bar Charts - PO Sales   # Group by 'Year_PO' and sum values for PO_Sales
            figure5 = website_usa.groupby('Year').agg({'order_id': 'count'}).reset_index()

            fig11 = px.bar(figure5, x="Year", y="order_id", color="Year", text_auto= True,
                        title="Total Order Count by Year", barmode="stack")

            # Stacked Bar Charts - referring_traffic
            #figure2 = retail_overview[retail_overview['Status'] != 'Cancelled']
            figure6 = website_usa.groupby('purchase_option').agg({'order_id': 'count'}).reset_index()

            fig12 = px.bar(figure6, x="purchase_option", y="order_id", color="purchase_option",  text_auto= True,
                        title="Purchase Option by Order Count", barmode="stack" )

            # Display Side-by-Side Charts
            col11, col12 = st.columns(2)
            col11.plotly_chart(fig11, use_container_width=True)
            col12.plotly_chart(fig12, use_container_width=True)

            st.markdown("")  # Add space between Key Metrics and Charts
            st.markdown("")

            # 📌 Get Top 6 Referring Channels
            figure7 = website_usa.groupby('referring_channel').agg({'order_id': 'count'}).reset_index()
            figure7 = figure7.nlargest(6, 'order_id')  # Get top 6 referring channels

            # 📊 Bar Chart - Top 6 Referring Channels
            fig13 = px.bar(
                figure7, x="referring_channel", y="order_id", color="referring_channel",
                text_auto=True, title="Referring Channel by Order Count", barmode="stack")

            # 📌 Group Data by Shipping Region
            figure8 = website_usa.groupby('shipping_region').agg({'total_sales': 'sum', 'net_sales': 'sum'}).reset_index()

            # 🏷️ Align Table and Chart Side by Side
            col11, col12 = st.columns(2)  # Define columns

            with col11:
                st.plotly_chart(fig13, use_container_width=True)  # Display bar chart

            with col12:
                st.markdown(""" <p style="background-color: #4CAF50; color: white; padding: 10px; border-radius: 50px; text-align: center; font-weight: bold;">
                    Sales by Region</p> """, unsafe_allow_html=True)
                st.dataframe(figure8, use_container_width=True, hide_index = None)  # Display table

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ India website email +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        elif st.session_state.page == 'India': 
            st.markdown("""
                <div style="margin: 20px 0;"> <div class="banner">India Website Overview</div>
                </div>
                <style> .banner {
                        background-color: white;
                        color: black;
                        font-size: 25px;
                        font-weight: bold;
                        text-align: center;
                        padding: 8px;
                        border-radius: 5px;
                        border: 1px solid black; } </style> """, unsafe_allow_html=True)
            website_india = website_customer.copy()
            website_india = website_india[website_india['shipping_country'] == 'India']

            website_india['month'] = pd.to_datetime(website_india['month'], errors='coerce')
            website_india['Year'] = website_india['month'].dt.strftime('%Y')  # Format as 'DD-MMM-YY'    
            website_india['Month'] = website_india['month'].dt.strftime('%b')  # Format as 'DD-MMM-YY'    

            # Key Metrics Calculation
            total_orders = website_india["order_id"].nunique()
            net_sales = website_india["net_sales"].sum()
            average_order_value = website_india["average_order_value"].mean()
            total_customer = website_india["customer_type"].count()
            return_customer = website_india[website_india['customer_type'] == "Returning"].shape[0]
            non_return_customer = website_india[website_india['customer_type'] != "Returning"].shape[0]

            # Display Key Metrics
            st.subheader("🧐 Key Metrics")
            col1, col2, col3, col4, col5, col6 = st.columns(6)

            # Apply custom styling using HTML inside Markdown
            col1.markdown(f"""<div style="text-align: center; font-weight: bold; background-color:#003049; padding: 5px; height: 100px; border-radius: 5px;">
                                <span style="font-size: 16px;">Net Sales</span><br>
                                <span style="color: white; font-size: 16px;">${net_sales:,.0f}</span></div>""", unsafe_allow_html=True)

            col2.markdown(f"""<div style="text-align: center; font-weight: bold; background-color:#003049; padding: 5px; height: 100px; border-radius: 5px;">
                                <span style="font-size: 16px;">Avg. Order Value</span><br>
                                <span style="color: white; font-size: 16px;">${average_order_value:,.0f}</span></div>""", unsafe_allow_html=True) 

            col3.markdown(f"""<div style="text-align: center; font-weight: bold; background-color:#003049; padding: 5px; height: 100px; border-radius: 5px;">
                                <span style="font-size: 16px;">Total Orders</span><br>
                                <span style="color: white; font-size: 16px;">{total_orders}</span></div>""", unsafe_allow_html=True)  

            col4.markdown(f"""<div style="text-align: center; font-weight: bold; background-color:#003049; padding: 5px; height: 100px; border-radius: 5px;">
                                <span style="font-size: 16px;">Total Customer Served</span><br>
                                <span style="color: white; font-size: 16px;">{total_customer:,.0f}</span></div>""", unsafe_allow_html=True)   

            col5.markdown(f"""<div style="text-align: center; font-weight: bold; background-color:#003049; padding: 5px; height: 100px; border-radius: 5px;">
                                <span style="font-size: 16px;">Returning Customers</span><br>
                                <span style="color: white; font-size: 16px;">{return_customer:,.0f}</span></div>""", unsafe_allow_html=True)  

            col6.markdown(f"""<div style="text-align: center; font-weight: bold; background-color:#003049; padding: 5px; height: 100px; border-radius: 5px;">
                                <span style="font-size: 16px;">Non-Returning Customers</span><br>
                                <span style="color: white; font-size: 16px;">{non_return_customer:,.0f}</span></div>""", unsafe_allow_html=True)  
            st.markdown("") # Add space between Key Metrics and Charts
            st.markdown("")     

            # Stacked Bar Charts - PO Sales   # Group by 'Year_PO' and sum values for PO_Sales
            figure1 = website_india.groupby('referring_category').agg({'order_id': 'count'}).reset_index()

            fig1 = px.bar(figure1, x="referring_category", y="order_id", color="referring_category", text_auto= True,
                        title="Referring Category by Order Count", barmode="stack")

            # Stacked Bar Charts - referring_traffic
            #figure2 = retail_overview[retail_overview['Status'] != 'Cancelled']
            figure2 = website_india.groupby('referring_traffic').agg({'order_id': 'count'}).reset_index()

            fig2 = px.bar(figure2, x="referring_traffic", y="order_id", color="referring_traffic",  text_auto= True,
                        title="Referring Traffic by Order Count", barmode="stack" )

            # Display Side-by-Side Charts
            st.subheader("📊 Analysis")
            col7, col8 = st.columns(2)
            col7.plotly_chart(fig1, use_container_width=True)
            col8.plotly_chart(fig2, use_container_width=True)

            st.markdown("") # Add space between Key Metrics and Charts
            st.markdown("")     

            # Stacked Bar Charts - PO Sales   # Group by 'Year_PO' and sum values for PO_Sales
            figure3 = website_india.groupby('referrer_source').agg({'order_id': 'count'}).reset_index()

            fig3 = px.bar(figure3, x="referrer_source", y="order_id", color="referrer_source", text_auto= True,
                        title="Referring Source by Order Count", barmode="stack")

            # Stacked Bar Charts - referring_traffic
            #figure2 = retail_overview[retail_overview['Status'] != 'Cancelled']
            figure4 = website_india.groupby('customer_type').agg({'order_id': 'count'}).reset_index()

            fig4 = px.bar(figure4, x="customer_type", y="order_id", color="customer_type",  text_auto= True,
                        title="Customer Type by Order Count", barmode="stack" )

            # Display Side-by-Side Charts
            col9, col10 = st.columns(2)
            col9.plotly_chart(fig3, use_container_width=True)
            col10.plotly_chart(fig4, use_container_width=True)

            st.markdown("") # Add space between Key Metrics and Charts
            st.markdown("")     

            # Stacked Bar Charts - PO Sales   # Group by 'Year_PO' and sum values for PO_Sales
            figure5 = website_india.groupby('Year').agg({'order_id': 'count'}).reset_index()

            fig11 = px.bar(figure5, x="Year", y="order_id", color="Year", text_auto= True,
                        title="Total Order Count by Year", barmode="stack")

            # Stacked Bar Charts - referring_traffic
            #figure2 = retail_overview[retail_overview['Status'] != 'Cancelled']
            figure6 = website_india.groupby('purchase_option').agg({'order_id': 'count'}).reset_index()

            fig12 = px.bar(figure6, x="purchase_option", y="order_id", color="purchase_option",  text_auto= True,
                        title="Purchase Option by Order Count", barmode="stack" )

            # Display Side-by-Side Charts
            col11, col12 = st.columns(2)
            col11.plotly_chart(fig11, use_container_width=True)
            col12.plotly_chart(fig12, use_container_width=True)

            st.markdown("")  # Add space between Key Metrics and Charts
            st.markdown("")

            # 📌 Get Top 6 Referring Channels
            figure7 = website_india.groupby('referring_channel').agg({'order_id': 'count'}).reset_index()
            figure7 = figure7.nlargest(6, 'order_id')  # Get top 6 referring channels

            # 📊 Bar Chart - Top 6 Referring Channels
            fig13 = px.bar(
                figure7, x="referring_channel", y="order_id", color="referring_channel",
                text_auto=True, title="Referring Channel by Order Count", barmode="stack")

            # 📌 Group Data by Shipping Region
            figure8 = website_india.groupby('shipping_region').agg({'total_sales': 'sum', 'net_sales': 'sum'}).reset_index()

            # 🏷️ Align Table and Chart Side by Side
            col11, col12 = st.columns(2)  # Define columns

            with col11:
                st.plotly_chart(fig13, use_container_width=True)  # Display bar chart

            with col12:
                st.markdown(""" <p style="background-color: #4CAF50; color: white; padding: 10px; border-radius: 50px; text-align: center; font-weight: bold;">
                    Sales by Region</p> """, unsafe_allow_html=True)
                st.dataframe(figure8, use_container_width=True, hide_index = None)  # Display table


# 📨 Customer Email Tab +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    with tab2:  
        st.subheader("Customer Email 📧")
        st.markdown("USA Customers Email")

        # 📌 Filter out USA  customers once
        cust_email_usa = website_customer[website_customer['shipping_country'] != 'India']
        cust_email_usa['Month'] = pd.to_datetime(cust_email_usa['month'], errors='coerce')
        cust_email_usa['Month'] = cust_email_usa['Month'].dt.strftime('%b-%y')

        # 📌 Fill or drop missing values in the necessary columns (for filters)
        cust_email_usa = cust_email_usa.dropna(subset=['Month'])  # Drop missing order dates
        cust_email_usa['customer_name'] = cust_email_usa['customer_name'].fillna('Unknown')  # Fill missing names
        cust_email_usa['purchase_option'] = cust_email_usa['purchase_option'].fillna('Unknown')  # Fill missing purchase options
        cust_email_usa['customer_type'] = cust_email_usa['customer_type'].fillna('Unknown')  # Fill missing customer types
        cust_email_usa['variant_sku'] = cust_email_usa['variant_sku'].fillna('Unknown')  # Fill missing variant SKU

        # 📌 Create filters in a single row
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            selected_month = st.multiselect("📅 Select Month-Year", options=["All"] + list(cust_email_usa['Month'].unique()), default=["All"],key="month_usa")

        with col2:
            selected_letter = st.multiselect("🔠 First Letter", options=["All"] + list(cust_email_usa['customer_name'].str[0].unique()), default=["All"],key="letter_usa")

        with col3:
            selected_purchase_option = st.multiselect("🛒 Purchase Option", options=["All"] + list(cust_email_usa['purchase_option'].unique()), default=["All"],key="purchase_option_usa")

        with col4:
            selected_customer_type = st.multiselect("👤 Customer Type", options=["All"] + list(cust_email_usa['customer_type'].unique()), default=["All"],key="customer_type_usa")

        with col5:
            selected_sku = st.multiselect("🔢 Variant SKU", options=["All"] + list(cust_email_usa['variant_sku'].unique()), default=["All"],key="sku_usa")

        # 📌 Apply filters to the data
        if "All" not in selected_month:
            cust_email_usa = cust_email_usa[cust_email_usa['Month'].isin(selected_month)]

        if "All" not in selected_letter:
            cust_email_usa = cust_email_usa[cust_email_usa['customer_name'].str[0].isin([letter[0] for letter in selected_letter])]

        if "All" not in selected_purchase_option:
            cust_email_usa = cust_email_usa[cust_email_usa['purchase_option'].isin(selected_purchase_option)]

        if "All" not in selected_customer_type:
            cust_email_usa = cust_email_usa[cust_email_usa['customer_type'].isin(selected_customer_type)]

        if "All" not in selected_sku:
            cust_email_usa = cust_email_usa[cust_email_usa['variant_sku'].isin(selected_sku)]

        # 📌 Create tables
        tables1 = {
            "Customer Orders by Email": cust_email_usa.groupby(['customer_name', 'Email'])[['Total Orders']].sum().reset_index(),
            "Customer Type Orders": cust_email_usa.pivot_table(index='customer_name', columns='customer_type', values='Total Orders', aggfunc='sum', fill_value=0).reset_index(),
            "All Customer Orders": cust_email_usa[['customer_name', 'variant_sku', 'shipping_region', 'orders']].sort_values(by='orders', ascending=False)}

        # 🏷️ Align tables side by side
        cols = st.columns(len(tables1))

        # 📌 Render tables dynamically
        for col, (title, df1) in zip(cols, tables1.items()):
            with col:
                st.markdown(f"""
                    <p style="background-color: #4CAF50; color: white; padding: 10px; border-radius: 50px; text-align: center; font-weight: bold;">
                    {title}</p>""", unsafe_allow_html=True)
                st.dataframe(df1, use_container_width=True, hide_index=True)

     # ____________________________________________________ for India cusotmer data _________________________________________________________
        st.markdown("---") 
        st.markdown("India Customers Email")

        # 📌 Filter out India customers once
        cust_email_india = website_customer[website_customer['shipping_country'] == 'India']
        cust_email_india['Month'] = pd.to_datetime(cust_email_india['month'], errors='coerce')
        cust_email_india['Month'] = cust_email_india['Month'].dt.strftime('%b-%y')

        # 📌 Fill or drop missing values in the necessary columns (for filters)
        cust_email_india = cust_email_india.dropna(subset=['Month'])  # Drop missing order dates
        cust_email_india['customer_name'] = cust_email_india['customer_name'].fillna('Unknown')  # Fill missing names
        cust_email_india['purchase_option'] = cust_email_india['purchase_option'].fillna('Unknown')  # Fill missing purchase options
        cust_email_india['customer_type'] = cust_email_india['customer_type'].fillna('Unknown')  # Fill missing customer types
        cust_email_india['variant_sku'] = cust_email_india['variant_sku'].fillna('Unknown')  # Fill missing variant SKU

        # 📌 Create filters in a single row
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            selected_month = st.multiselect("📅 Select Month-Year", options=["All"] + list(cust_email_india['Month'].unique()), default=["All"])

        with col2:
            selected_letter = st.multiselect("🔠 First Letter", options=["All"] + list(cust_email_india['customer_name'].str[0].unique()), default=["All"])

        with col3:
            selected_purchase_option = st.multiselect("🛒 Purchase Option", options=["All"] + list(cust_email_india['purchase_option'].unique()), default=["All"])

        with col4:
            selected_customer_type = st.multiselect("👤 Customer Type", options=["All"] + list(cust_email_india['customer_type'].unique()), default=["All"])

        with col5:
            selected_sku = st.multiselect("🔢 Variant SKU", options=["All"] + list(cust_email_india['variant_sku'].unique()), default=["All"])

        # 📌 Apply filters to the data
        if "All" not in selected_month:
            cust_email_india = cust_email_india[cust_email_india['Month'].isin(selected_month)]

        if "All" not in selected_letter:
            cust_email_india = cust_email_india[cust_email_india['customer_name'].str[0].isin([letter[0] for letter in selected_letter])]

        if "All" not in selected_purchase_option:
            cust_email_india = cust_email_india[cust_email_india['purchase_option'].isin(selected_purchase_option)]

        if "All" not in selected_customer_type:
            cust_email_india = cust_email_india[cust_email_india['customer_type'].isin(selected_customer_type)]

        if "All" not in selected_sku:
            cust_email_india = cust_email_india[cust_email_india['variant_sku'].isin(selected_sku)]

        # 📌 Create tables
        tables = {
            "Customer Orders by Email": cust_email_india.groupby(['customer_name', 'Email'])[['Total Orders']].sum().reset_index(),
            "Customer Type Orders": cust_email_india.pivot_table(index='customer_name', columns='customer_type', values='Total Orders', aggfunc='sum', fill_value=0).reset_index(),
            "All Customer Orders": cust_email_india[['customer_name', 'variant_sku', 'shipping_region', 'orders']].sort_values(by='orders', ascending=False) }

        # 🏷️ Align tables side by side
        cols = st.columns(len(tables))

        # 📌 Render tables dynamically
        for col, (title, df) in zip(cols, tables.items()):
            with col:
                st.markdown(f"""
                    <p style="background-color: #4CAF50; color: white; padding: 10px; border-radius: 50px; text-align: center; font-weight: bold;">
                    {title}</p>""", unsafe_allow_html=True)
                st.dataframe(df, use_container_width=True, hide_index=True)
            


# 📲 Social Media Tab +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    with tab3:  
        st.subheader("Social Media 🤳")
        st.markdown("Social Media Insights")

       
