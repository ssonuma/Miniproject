import streamlit as st


st.set_page_config(
    page_title="Energy Bill Optimization",
    layout="wide"
)


st.markdown("""
<style>
.stApp {
    background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #1c1c1c);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

h1, h2, h3 {
    color: white;
    text-align: center;
}

p, label {
    color: #e0e0e0;
    font-size: 16px;
}

.card {
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(14px);
    border-radius: 20px;
    padding: 25px;
    margin: 15px 0px;
    box-shadow: 0 0 30px rgba(0,0,0,0.4);
    transition: 0.4s;
}

.card:hover {
    transform: translateY(-10px) scale(1.02);
}

.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 30px;
    padding: 12px 30px;
    font-size: 16px;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.08);
    box-shadow: 0 0 20px #00c6ff;
}
</style>
""", unsafe_allow_html=True)


if "step" not in st.session_state:
    st.session_state.step = 1


st.markdown("""
<h1>⚡ Energy Bill Optimization Platform</h1>
<p style="text-align:center;">
Predict your next electricity bill • Identify high energy appliances • Save money smartly
</p>
""", unsafe_allow_html=True)

st.progress(st.session_state.step / 4)


if st.session_state.step == 1:
    st.markdown("""<div class="card">
    <h3>🏠 Home & Tariff Details</h3>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        home_size = st.selectbox("Home Size", ["1BHK", "2BHK", "3BHK"])
    with col2:
        people = st.number_input("No. of People", 1, 10, 2)
    with col3:
        tariff = st.selectbox("Tariff Type", ["Domestic", "Commercial"])

    last_bill = st.number_input("Last Month Bill (₹)", min_value=0, value=2000)

    if st.button("Next → Appliance Usage"):
        st.session_state.home = home_size
        st.session_state.people = people
        st.session_state.tariff = tariff
        st.session_state.last_bill = last_bill
        st.session_state.step = 2


if st.session_state.step == 2:
    st.markdown("""<div class="card">
    <h3>🔌 Appliance Usage (Hours per day)</h3>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        ac = st.slider("AC", 0, 12, 4)
        tv = st.slider("TV", 0, 10, 4)
    with col2:
        geyser = st.slider("Water Heater", 0, 5, 1)
        wm = st.slider("Washing Machine", 0, 3, 1)
    with col3:
        fridge = st.slider("Refrigerator", 0, 24, 24)
        router = st.slider("WiFi Router", 0, 24, 24)

    fans = st.slider("Fans & Lights", 0, 12, 6)

    if st.button("Next → Prediction"):
        st.session_state.appliances = {
            "AC": ac,
            "TV": tv,
            "Water Heater": geyser,
            "Washing Machine": wm,
            "Refrigerator": fridge,
            "Router": router,
            "Fans/Lights": fans
        }
        st.session_state.step = 3


if st.session_state.step == 3:
    rates = {
        "AC": 10,
        "TV": 3,
        "Water Heater": 15,
        "Washing Machine": 8,
        "Refrigerator": 5,
        "Router": 1,
        "Fans/Lights": 2
    }

    appliances = st.session_state.appliances

    predicted_bill = sum(
        appliances[a] * rates[a] * 30 for a in appliances
    )

    st.markdown(f"""
    <div class="card" style="text-align:center;">
        <h2>💰 Predicted Next Month Bill</h2>
        <h1 style="color:#00ffcc;">₹ {predicted_bill}</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div class="card">
    <h3>🚨 High Energy Appliances</h3>
    </div>""", unsafe_allow_html=True)

    sorted_apps = sorted(
        appliances.items(),
        key=lambda x: x[1] * rates[x[0]],
        reverse=True
    )

    for app, hrs in sorted_apps[:3]:
        cost = hrs * rates[app] * 30
        st.error(f"{app} → ₹{cost} / month")

    if st.button("Next → Savings Tips"):
        st.session_state.step = 4


if st.session_state.step == 4:
    st.markdown("""<div class="card">
    <h3>💡 Personalized Cost-Saving Tips</h3>
    </div>""", unsafe_allow_html=True)

    total_savings = 0

    for app, hrs in st.session_state.appliances.items():
        saving = int(hrs * rates[app] * 0.2 * 30)
        total_savings += saving
        if saving > 0:
            st.success(f"Reduce {app} usage → Save ₹{saving}/month")

    st.markdown(f"""
    <div class="card" style="text-align:center;">
        <h2>✅ Total Possible Savings</h2>
        <h1 style="color:#00ff99;">₹ {total_savings} / month</h1>
    </div>
    """, unsafe_allow_html=True)

    st.info("📈 Annual Savings Potential: ₹ " + str(total_savings * 12))
