import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt

import subprocess
import os
import tempfile

from xml.etree.ElementTree import Element, SubElement
import json
from PIL import Image
import base64


def add_think_time_to_sampler(sampler_element, think_time=1000, random_range=500):
    from xml.etree.ElementTree import Element, SubElement
    timer = Element("UniformRandomTimer", {"guiclass": "UniformRandomTimerGui", "testclass": "UniformRandomTimer", "testname": "Think Time", "enabled": "true"})
    string_prop = SubElement(timer, "stringProp", {"name": "ConstantTimer.delay"})
    string_prop.text = str(think_time)
    range_prop = SubElement(timer, "stringProp", {"name": "RandomTimer.range"})
    range_prop.text = str(random_range)
    return timer


# Page configuration
st.set_page_config(page_title="Edith Performance Dashboard", layout="wide")

# Session state for login/logout
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

#edith Title : background: linear-gradient(90deg, #0d6efd, #6610f2);  :- Blue to Purple Colour
# background: liner-gradient(90deg, #EF852E, #FC7400 );  :- Orange Colour
# Load local image and convert to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded}"

# Replace with your path
#img_path = "C:/Users/HP/Downloads/Edith/pwc_logo.png"
img_path = "pwc_logo.png"
background_image = get_base64_image(img_path)

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    html, body {{
        font-family: 'Inter', sans-serif;
        background-color: #fff8f1;
        background-image: url("{background_image}");
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: top right;
        background-size: 150px;
    }}

    .main {{
        background-color: #ffffffcc;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    }}

    .edith-title {{
        font-size: 36px;
        font-weight: 800;
        background: linear-gradient(90deg, #EF852E, #FC7400);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }}

    .topbar {{
        background-color: #fff0e0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}

    .stButton>button {{
        background-color: #EF852E;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1.5em;
        font-weight: 600;
        border: none;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(239, 133, 46, 0.3);
    }}

    .stButton>button:hover {{
        background-color: #FC7400;
    }}

    .stSidebar {{
        background-color: #fff0e0;
    }}

    .block-container {{
        padding-top: 2rem;
    }}

    .stNumberInput input {{
        background-color: #fff !important;
            border: 1px solid #ffa94d;
        border-radius: 8px;
        padding: 6px;
    }}

    .stTextArea textarea {{
        border-radius: 8px;
        padding: 10px;
        border: 1px solid #ffc078;
    }}

    .stFileUploader > div > div {{
        border: 2px dashed #ffa94d;
        border-radius: 10px;
        background-color: #fff3e6;
    }}

    .stMetric {{
        background-color: #ffffff;
        border: 1px solid #ffc078;
        border-radius: 10px;
        padding: 10px;
    }}
    </style>
""", unsafe_allow_html=True)



# Top bar with login/logout and title
with st.container():
    col1, col2 = st.columns([8, 1])
    with col1:
        st.markdown("<div class='edith-title'>Edith Performance Testing Dashboard</div>", unsafe_allow_html=True)
    with col2:
        if st.session_state.logged_in:
            if st.button("Logout"):
                st.session_state.logged_in = False
        else:
            if st.button("Login"):
                st.session_state.logged_in = True

# Require login to access the portal
if not st.session_state.logged_in:
    st.info("🔐 Please login to access the Edith portal features.")
    st.stop()

#logo_path = "C:/Users/HP/Downloads/Edith/pwc_logo.png"
logo_path = "pwc_logo.png"
pwc_logo = Image.open(logo_path)

# Apply full-width logo and navigation
with st.sidebar:
    # Stretch the logo across the sidebar
    st.markdown("""
        <style>
        .sidebar-logo img {
            width: 100%;
            height: auto;
            margin-bottom: 15px;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
    st.image(pwc_logo, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Navigation menu
    selected = option_menu(
        menu_title="Navigation",
        options=[
            "Performance Testing Types",
            "Load Test Calculations",
            "Convert Collection to JMX",
            "Run JMeter Test (Non-GUI)",
            "CSV Results",
            "AI Powered Live Monitoring",
            "Observations"
        ],
        icons=["bar-chart", "calculator", "upload", "terminal", "filetype-csv", "cpu", "journal-text"],
        menu_icon="speedometer",
        default_index=0,
        styles={
            "container": {
                "background-color": "#fff0e0",
                "padding": "0px",
                "border-radius": "10px"
            },
            "icon": {"color": "#EF852E", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "5px",
                "color": "#EF852E",
                "--hover-color": "#ffe0c2"
            },
            "nav-link-selected": {
                "background-color": "#FC7400",
                "color": "white",
                "font-weight": "bold"
            }
        }
    )

# === Tabs Logic ===
if selected == "Performance Testing Types":
    st.header("📊 Performance Testing Types")

    # 🚀 Load Testing
    st.subheader("🚀 Load Testing")
    with st.expander("Show Details and Graph"):
        st.write("""
        **Definition:** Load testing checks how a system performs under an expected number of concurrent users or requests.
        It helps identify response times, bottlenecks, and scalability thresholds under normal usage.
        """)
        fig1, ax1 = plt.subplots(figsize=(6, 3))
        users = [10, 50, 100, 200, 400, 800]
        response_time = [1.2, 1.8, 2.5, 3.1, 4.0, 6.5]
        ax1.plot(users, response_time, marker='o', color='dodgerblue')
        ax1.set_title("Response Time vs Users")
        ax1.set_xlabel("Concurrent Users")
        ax1.set_ylabel("Response Time (s)")
        st.pyplot(fig1)

    # 🔥 Stress Testing
    st.subheader("🔥 Stress Testing")
    with st.expander("Show Details and Graph"):
        st.write("""
        **Definition:** Stress testing evaluates how a system behaves under extreme loads — often beyond its intended capacity — 
        to check for crashing points or performance degradation.
        """)
        fig2, ax2 = plt.subplots(figsize=(6, 3))
        users = [100, 200, 300, 500, 800, 1000]
        response_time = [2.0, 2.8, 3.6, 5.2, 8.0, 15.0]
        ax2.plot(users, response_time, marker='s', color='crimson')
        ax2.set_title("Stress Test: Response Time vs Load")
        ax2.set_xlabel("Concurrent Users")
        ax2.set_ylabel("Response Time (s)")
        st.pyplot(fig2)

    # 📈 Spike Testing
    st.subheader("📈 Spike Testing")
    with st.expander("Show Details and Graph"):
        st.write("""
        **Definition:** Spike testing measures how the system reacts to sudden increases or decreases in load, 
        like flash sales or marketing campaigns.
        """)
        fig3, ax3 = plt.subplots(figsize=(6, 3))
        time = ["T0", "T1", "T2", "T3", "T4"]
        load = [50, 50, 500, 50, 50]
        ax3.plot(time, load, marker='^', color='orange')
        ax3.set_title("Spike Test: User Load Over Time")
        ax3.set_ylabel("Concurrent Users")
        st.pyplot(fig3)

    # ⏳ Endurance Testing
    st.subheader("⏳ Endurance (Soak) Testing")
    with st.expander("Show Details and Graph"):
        st.write("""
        **Definition:** Endurance or soak testing evaluates system performance over a prolonged period to detect memory leaks, slow degradation, or stability issues.
        """)
        fig4, ax4 = plt.subplots(figsize=(6, 3))
        hours = list(range(1, 13))
        memory = [300, 310, 320, 335, 340, 355, 365, 380, 390, 410, 420, 430]
        ax4.plot(hours, memory, marker='d', color='green')
        ax4.set_title("Endurance Test: Memory Usage Over Time")
        ax4.set_xlabel("Test Duration (Hours)")
        ax4.set_ylabel("Memory (MB)")
        st.pyplot(fig4)

    # 🔄 Scalability Testing
    st.subheader("🔄 Scalability Testing")
    with st.expander("Show Details and Graph"):
        st.write("""
        **Definition:** Scalability testing determines how well the system can handle increasing workloads by adding resources (horizontal or vertical scaling).
        """)
        fig5, ax5 = plt.subplots(figsize=(6, 3))
        v_users = [100, 200, 400, 800]
        throughput = [1000, 1900, 3600, 7200]
        ax5.plot(v_users, throughput, marker='o', color='purple')
        ax5.set_title("Scalability: Throughput vs Virtual Users")
        ax5.set_xlabel("Virtual Users")
        ax5.set_ylabel("Requests/sec")
        st.pyplot(fig5)


elif selected == "Load Test Calculations":
    st.header("📈 Load Test Calculations")

    tabs = st.tabs(["📏 Pacing", "👥 VUsers", "⚡ TPS", "📘 Definitions"])

    # ---------------------- TAB 1: PACING ----------------------
    with tabs[0]:
        st.subheader("Calculate Pacing")
        vusers = st.number_input("Enter Virtual Users", min_value=1)
        response_time = st.number_input("Response Time (in seconds)", min_value=0.0, format="%.2f")
        tps = st.number_input("Transactions per Second (TPS)", min_value=0.0, format="%.2f")
        think_time = st.number_input("Think Time (in seconds)", min_value=0.0, format="%.2f")

        if tps > 0:
            pacing = (vusers / tps) - (response_time + think_time)
            pacing = max(pacing, 0)  # avoid negative
            st.success(f"📏 Calculated Pacing: **{round(pacing, 2)} seconds**")
        else:
            st.warning("TPS must be greater than 0 to calculate pacing.")

    # ---------------------- TAB 2: VUSERS ----------------------
    with tabs[1]:
        st.subheader("Calculate Virtual Users")
        pacing = st.number_input("Pacing (in seconds)", min_value=0.0, format="%.2f")
        response_time = st.number_input("Response Time (in seconds)", key="v_resp", min_value=0.0, format="%.2f")
        tps = st.number_input("Transactions per Second (TPS)", key="v_tps", min_value=0.0, format="%.2f")
        think_time = st.number_input("Think Time (in seconds)", key="v_think", min_value=0.0, format="%.2f")

        if tps > 0:
            vusers = tps * (response_time + think_time + pacing)
            st.success(f"👥 Calculated Virtual Users: **{round(vusers)} users**")
        else:
            st.warning("TPS must be greater than 0 to calculate users.")

    # ---------------------- TAB 3: TPS ----------------------
    with tabs[2]:
        st.subheader("Calculate Transactions Per Second (TPS)")
        pacing = st.number_input("Pacing (in seconds)", key="t_pacing", min_value=0.0, format="%.2f")
        response_time = st.number_input("Response Time (in seconds)", key="t_resp", min_value=0.0, format="%.2f")
        vusers = st.number_input("Virtual Users", key="t_vusers", min_value=1)
        think_time = st.number_input("Think Time (in seconds)", key="t_think", min_value=0.0, format="%.2f")

        total_time = response_time + think_time + pacing
        if total_time > 0:
            tps = vusers / total_time
            st.success(f"⚡ Calculated TPS: **{round(tps, 2)} transactions/sec**")
        else:
            st.warning("Total time (RT + TT + Pacing) must be > 0 to calculate TPS.")

    # ---------------------- TAB 4: DEFINITIONS ----------------------
    with tabs[3]:
        st.subheader("📘 Definitions")

        st.markdown("""
        - **🕒 Response Time**: Time taken by the system to respond to a request (excluding think time).
        - **🧠 Think Time**: Time the user waits (reads/analyzes) between two requests.
        - **📏 Pacing**: Delay between the end of one iteration and the start of the next by the same user.
        - **👥 Virtual Users (VUsers)**: Simulated users in a performance test.
        - **⚡ TPS (Transactions Per Second)**: Number of transactions the system processes per second.
        """)


elif selected == "Convert Collection to JMX":
    st.header("🔄 Convert Postman Collection to JMeter (.jmx)")

    postman_file = st.file_uploader("Upload Postman Collection (v2.1)", type=["json"])
    think_time = st.slider("Think Time (ms)", 0, 5000, 1000)
    think_range = st.slider("Random Range (ms)", 0, 3000, 500)

    if postman_file:
        postman_data = json.load(postman_file)

        # Create base JMX structure
        test_plan = Element("jmeterTestPlan", {"version": "1.2", "properties": "5.0", "jmeter": "5.5"})
        hash_tree = SubElement(test_plan, "hashTree")

        # Thread Group
        thread_group = Element("ThreadGroup",
                               {"guiclass": "ThreadGroupGui", "testclass": "ThreadGroup", "testname": "Thread Group",
                                "enabled": "true"})
        SubElement(thread_group, "stringProp", {"name": "ThreadGroup.num_threads"}).text = "1"
        SubElement(thread_group, "stringProp", {"name": "ThreadGroup.ramp_time"}).text = "1"
        SubElement(thread_group, "boolProp", {"name": "ThreadGroup.scheduler"}).text = "false"
        SubElement(thread_group, "stringProp", {"name": "ThreadGroup.duration"}).text = ""

        thread_tree = SubElement(hash_tree, "hashTree")
        thread_tree.append(thread_group)
        sampler_tree = SubElement(thread_tree, "hashTree")

        # Iterate through Postman requests
        for item in postman_data.get("item", []):
            if "request" in item:
                request = item["request"]
                url = request.get("url", {}).get("raw", "")
                method = request.get("method", "GET")

                http_sampler = Element("HTTPSamplerProxy", {
                    "guiclass": "HttpTestSampleGui",
                    "testclass": "HTTPSamplerProxy",
                    "testname": item.get("name", "Request"),
                    "enabled": "true"
                })
                SubElement(http_sampler, "stringProp", {"name": "HTTPSampler.domain"}).text = ""  # Add if parsed
                SubElement(http_sampler, "stringProp", {"name": "HTTPSampler.protocol"}).text = ""
                SubElement(http_sampler, "stringProp", {"name": "HTTPSampler.path"}).text = url
                SubElement(http_sampler, "stringProp", {"name": "HTTPSampler.method"}).text = method

                sampler_tree.append(http_sampler)
                sampler_inner_tree = SubElement(sampler_tree, "hashTree")

                # Add Think Time
                think_timer = add_think_time_to_sampler(http_sampler, think_time, think_range)
                sampler_inner_tree.append(think_timer)
                SubElement(sampler_inner_tree, "hashTree")  # timer's inner tree

        # Export JMX
        jmx_tree = ET.ElementTree(test_plan)
        output_path = os.path.join(tempfile.gettempdir(), "converted_with_thinktime.jmx")
        jmx_tree.write(output_path)

        st.success("✅ Collection converted with Think Time!")
        with open(output_path, "rb") as f:
            st.download_button("📥 Download JMX", f, file_name="converted_collection.jmx")


elif selected == "Run JMeter Test (Non-GUI)":
    st.header("🧪 Run JMeter Test (Non-GUI Mode)")

    jm_tabs = st.tabs(["🔘 Run Direct JMX", "⚙️ Run with Custom Load"])

    # ---------------- TAB 1: Run Existing JMX ----------------
    with jm_tabs[0]:
        st.subheader("🔘 Upload JMX and Run Directly")
        jmx_file = st.file_uploader("Upload JMeter .jmx File", type=["jmx"])

        if jmx_file is not None:
            temp_jmx = tempfile.NamedTemporaryFile(delete=False, suffix=".jmx")
            temp_jmx.write(jmx_file.read())
            temp_jmx.close()

            if st.button("🚀 Run JMeter Test"):
                result_file = os.path.join(tempfile.gettempdir(), "jmeter_results.csv")
                jmeter_command = [
                    "jmeter",
                    "-n",
                    "-t", temp_jmx.name,
                    "-l", result_file
                ]

                with st.spinner("Running JMeter test..."):
                    process = subprocess.run(jmeter_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                st.success("✅ JMeter Test Executed")
                st.text("Command Output:")
                st.code(process.stdout)
                st.text("Command Errors (if any):")
                st.code(process.stderr)

    # ---------------- TAB 2: Custom Load Params --------------
    with jm_tabs[1]:
        st.subheader("⚙️ Upload JMX and Override Load Settings")

        users = st.number_input("Number of Users", min_value=1)
        ramp_up = st.number_input("Ramp-Up Time (seconds)", min_value=1)
        duration = st.number_input("Test Duration (seconds)", min_value=1)
        jmx_file_custom = st.file_uploader("Upload JMeter .jmx File", type=["jmx"], key="jmx_custom")

        if jmx_file_custom is not None:
            temp_jmx_custom = tempfile.NamedTemporaryFile(delete=False, suffix=".jmx")
            temp_jmx_custom.write(jmx_file_custom.read())
            temp_jmx_custom.close()

            if st.button("🚀 Run Test with Custom Load"):
                try:
                    # Modify the JMX file using sed or ElementTree (simple replacement)
                    import xml.etree.ElementTree as ET

                    tree = ET.parse(temp_jmx_custom.name)
                    root = tree.getroot()

                    for elem in root.iter():
                        if elem.tag == 'stringProp' and 'ThreadGroup.num_threads' in elem.attrib.get('name', ''):
                            elem.text = str(users)
                        if elem.tag == 'stringProp' and 'ThreadGroup.ramp_time' in elem.attrib.get('name', ''):
                            elem.text = str(ramp_up)
                        if elem.tag == 'stringProp' and 'ThreadGroup.duration' in elem.attrib.get('name', ''):
                            elem.text = str(duration)
                        if elem.tag == 'boolProp' and 'ThreadGroup.scheduler' in elem.attrib.get('name', ''):
                            elem.text = 'true'

                    updated_jmx_path = os.path.join(tempfile.gettempdir(), "updated_test.jmx")
                    tree.write(updated_jmx_path)

                    result_file_custom = os.path.join(tempfile.gettempdir(), "custom_results.csv")
                    jmeter_cmd = [
                        "jmeter",
                        "-n",
                        "-t", updated_jmx_path,
                        "-l", result_file_custom
                    ]

                    with st.spinner("Running JMeter test with custom settings..."):
                        result = subprocess.run(jmeter_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                    st.success("✅ JMeter Test Completed with Custom Load")
                    st.text("Command Output:")
                    st.code(result.stdout)
                    st.text("Command Errors (if any):")
                    st.code(result.stderr)

                except Exception as e:
                    st.error(f"❌ Error running test: {e}")


elif selected == "CSV Results":
    st.header("📄 Analyze CSV Test Results")
    csv_file = st.file_uploader("Upload CSV results file:", type=["csv"])
    if csv_file:
        df = pd.read_csv(csv_file)
        st.dataframe(df)
        st.metric("Samples Run", len(df))
        st.metric("Avg Response Time (ms)", round(df['elapsed'].mean(), 2))

elif selected == "AI Powered Live Monitoring":
    st.header("🤖 AI Powered Live Monitoring")
    st.info("🔬 Real-time AI insights and predictive analytics coming soon...")

elif selected == "Observations":
    st.header("📝 Test Observations")
    notes = st.text_area("Enter notes or findings:", height=200)
    if st.button("Save Note"):
        st.success("🗒️ Observation saved successfully!")
