# investment_game.py
import streamlit as st
import numpy as np
import pandas as pd

# -------------------- CONFIG --------------------
MONTHS = 12
INITIAL_PRICE = 100
MU_ANNUAL = 0.12
SIGMA_ANNUAL = 0.25

# -------------------- FUNCTIONS --------------------
def generate_returns(seed):
    np.random.seed(seed)
    mu_monthly = (1 + MU_ANNUAL)**(1/12) - 1
    sigma_monthly = SIGMA_ANNUAL / np.sqrt(12)
    returns = np.random.normal(loc=mu_monthly, scale=sigma_monthly, size=MONTHS)
    prices = [INITIAL_PRICE]
    for r in returns:
        prices.append(prices[-1] * (1 + r))
    return prices, returns



# -------------------- GAME DISPLAY --------------------
st.title("InvestmentgameBypae")
    # regiser part 
st.title("register")
player_name = st.text_input("ชื่อผู้เล่น")
shared_seed = st.text_input("รหัสเกม (seed)", )

if not shared_seed.isnumeric():
    st.warning("กรุณากรอก seed เป็นตัวเลขเท่านั้น")
    st.stop()

seed = int(shared_seed)
    




if player_name:
    st.success(f"ยินดีต้อนรับ {player_name}")
    prices, returns = generate_returns(seed)

    df = pd.DataFrame({
        "เดือน": ["เริ่มต้น"] + [f"เดือน {i+1}" for i in range(MONTHS)],
        "ราคาหุ้น": prices,
        "ผลตอบแทน": [None] + list(np.round(returns * 100, 2))
    })

    st.line_chart(df.set_index("เดือน")["ราคาหุ้น"])
    with st.expander("ดูรายละเอียดรายเดือน"):
        st.dataframe(df, use_container_width=True)
else:
    st.info("กรุณาใส่ชื่อผู้เล่นก่อนเริ่มเกม")


