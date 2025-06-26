# investment_game.py
import streamlit as st
import numpy as np
import pandas as pd
import random

# -------------------- CONFIG --------------------
STOCKS = {
    "LTECH":     {"mu": 0.15, "sigma": 0.30, "sector": "เทคโนโลยี"},
    "MEDIHOS":  {"mu": 0.10, "sigma": 0.15, "sector": "สุขภาพ"},
    "DOOF":   {"mu": 0.08, "sigma": 0.10, "sector": "อาหาร"},
    "OILMAX":    {"mu": 0.12, "sigma": 0.25, "sector": "พลังงาน"},
    "SHOUSE":  {"mu": 0.09, "sigma": 0.20, "sector": "อสังหาฯ"},
}
MONTHS = 12
INITIAL_PRICE = 100
MU_ANNUAL = 0.12
SIGMA_ANNUAL = 0.25
# สุ่มรายการข่าว
news_pool = [
    {"text": "ความก้าวหน้า AI ", "impact": {"TECHX": 0.22, "MEDIHOS": -0.04}},
    {"text": "โรคระบาดรอบใหม่ ", "impact": {"MEDIHOS": 0.28, "DOOF": -0.08}},
    {"text": "สินค้าแพงขึ้น ", "impact":  {"DOOF": -0.10, "SHOUSE": -0.03}},
    {"text": "น้ำมันพุ่ง ", "impact": {"OILMAX": 0.20, "TECHX": -0.10}},
    {"text": "ภาษีอสังหาฯ ", "impact": {"SHOUSE": -0.15, "MEDIHOS": -0.02}},
    {"text": "ตลาดหุ้นผันผวน ", "impact": {"TECHX": -0.08, "DOOF": 0.04, "OILMAX": -0.04}},
    {"text": "นโยบายรัฐสนับสนุนพลังงาน ", "impact": {"OILMAX": 0.20, "SHOUSE": -0.04}},
    {"text": "ความก้าวหน้าทางการแพทย์ ", "impact": {"MEDIHOS": 0.20, "TECHX": -0.06}},
    {"text": "ราคาวัตถุดิบขึ้น ", "impact": {"DOOF": -0.09, "OILMAX": 0.05}},
    {"text": "สงครามการค้า ", "impact": {"TECHX": -0.10, "SHOUSE": -0.05, "DOOF": -0.03}},
    {"text": "ภาวะเศรษฐกิจดีขึ้น ", "impact": {"SHOUSE": 0.08, "TECHX": 0.10, "DOOF": 0.08}},
    {"text": "นโยบายลดมลพิษ ", "impact": {"OILMAX": -0.17, "MEDIHOS": 0.08}},
    {"text": "วิกฤตโภคภัณฑ์ ", "impact": {"DOOF": -0.11, "OILMAX": -0.09}},
    {"text": "การขยายตลาดใหม่ ", "impact": {"TECHX": 0.14, "SHOUSE": 0.08}},
    {"text": "มาตรการกระตุ้นเศรษฐกิจ ", "impact": {"SHOUSE": 0.12, "DOOF": 0.11}},
    {"text": "เทคโนโลยีล้ำสมัย ", "impact": {"TECHX": 0.21, "MEDIHOS": 0.09}},
    {"text": "ราคาน้ำมันลด ", "impact": {"OILMAX": -0.11, "DOOF": 0.06}},
    {"text": "การประท้วงแรงงาน ", "impact": {"SHOUSE": -0.12, "TECHX": -0.09}},
    {"text": "การวิจัยวัคซีนสำเร็จ ", "impact": {"MEDIHOS": 0.33, "DOOF": -0.05}},
    {"text": "ปัญหาซัพพลายเชน ", "impact": {"DOOF": -0.15, "TECHX": -0.13, "OILMAX": -0.07}},
]

# -------------------- FUNCTIONS --------------------
def generate_returns(seed, mu_annual, sigma_annual, impact_pct=0.0, start_price=100):
    np.random.seed(seed)
    mu_monthly = (1 + mu_annual)**(1/12) - 1
    sigma_monthly = sigma_annual / np.sqrt(12)
    returns = np.random.normal(loc=mu_monthly, scale=sigma_monthly, size=MONTHS)
    returns += (impact_pct / 12)
    prices = [start_price]
    for r in returns:
        prices.append(prices[-1] * (1 + r))
    return prices, returns


# -------------------- SESSION INIT --------------------
if "turn" not in st.session_state:
    st.session_state.turn = 1
if "last_prices" not in st.session_state:
    st.session_state.last_prices = {stock: INITIAL_PRICE for stock in STOCKS}
if "page" not in st.session_state:
    st.session_state.page = "page_1"

if "turn_news" not in st.session_state:
    st.session_state.turn_news = {}
    for y in range(1, 11):
        st.session_state.turn_news[y] = random.choice(news_pool)

if "news_bought_in_turn" not in st.session_state:
    st.session_state.news_bought_in_turn = {}

if "impact_next_turn" not in st.session_state:
    st.session_state.impact_next_turn = {}
if "stock_prices_by_turn" not in st.session_state:
    st.session_state.stock_prices_by_turn = {}


# -------------------- GAME DISPLAY --------------------
#page_1
if st.session_state.page == "page_1":
    st.title('INVESTMENTGAME')
    # how to play
    st.header('How To Play')
    st.text("เริ่มต้นผู้เล่นจะได้รับเงินเริ่มต้น 10,000 และ ข้อมูลของหุ้นแต่ละตัว เพื่อวิเคราะห๋และเลือกลงทุน\nโดยสามารถ ซื้อข้อมูลได้ ซึ่งข้อมูลอาจบอกแนวโน้มหุ้นได้ ใครที่มีเงินเยอะที่สุดใน 10 ปี เป๋นผู้ขนะ")

    if st.button("Register") :
        st.session_state.page = "page_2"
#page_2
elif st.session_state.page == "page_2":
    st.title('INVESTMENTGAME')
    st.header('Register')
    player_name = st.text_input("ชื่อผู้เล่น", key="name_input")
    shared_seed = st.text_input("รหัสเกม (seed)", key="seed_input")

    if not shared_seed.isnumeric():
        st.warning("กรุณากรอก seed เป็นตัวเลขเท่านั้น")
        st.stop()

    if player_name:
        
        st.session_state.page = "page_3"
        st.session_state.player_name = player_name
        st.session_state.seed = int(shared_seed)
        st.rerun()  # รีเฟรชเพื่อโหลดหน้าเกม

    else:
        st.info("กรุณาใส่ชื่อผู้เล่นก่อนเริ่มเกม")
#page_3
elif st.session_state.page == "page_3":
    current_turn = st.session_state.turn

    # ถ้ายังไม่เคยสร้างราคาหุ้นในเทิร์นนี้มาก่อน
    if current_turn not in st.session_state.stock_prices_by_turn:
        st.session_state.stock_prices_by_turn[current_turn] = {}

        for stock, info in STOCKS.items():
            # ผลกระทบข่าวของเทิร์นนี้ (จาก turn-1)
            impact_pct = st.session_state.impact_next_turn.get(current_turn, {}).get(stock, 0.0)

            # เริ่มต้นจากราคาปิดของเทิร์นก่อนหน้า
            start_price = st.session_state.last_prices.get(stock, INITIAL_PRICE)

            # สุ่มราคาหุ้น 12 เดือน
            prices, returns = generate_returns(
                seed=st.session_state.seed + current_turn,
                mu_annual=info["mu"],
                sigma_annual=info["sigma"],
                impact_pct=impact_pct,
                start_price=start_price
            )

            # เก็บผลลัพธ์ไว้ใน session_state
            st.session_state.stock_prices_by_turn[current_turn][stock] = {
                "prices": prices,
                "returns": returns
            }

            # บันทึกราคาสิ้นสุดเทิร์นนี้ (ไว้ใช้ในเทิร์นถัดไป)
            st.session_state.last_prices[stock] = prices[-1]





    st.title('INVESTMENTGAME')
    st.header(f"TURN {st.session_state.turn}")
    
    #data 

    
    st.subheader("เลือกหุ้นที่ต้องการดู")
    selected_stock = st.selectbox("เลือกหุ้น", list(STOCKS.keys()))

    info = STOCKS[selected_stock]
    mu = info["mu"]
    sigma = info["sigma"]

    st.info(f"หุ้น {selected_stock} ({info['sector']})")

    prices = st.session_state.stock_prices_by_turn[current_turn][selected_stock]["prices"]
    returns = st.session_state.stock_prices_by_turn[current_turn][selected_stock]["returns"]
    current_price = prices[-1]

    # เก็บราคาปิดของ turn นี้ไว้สำหรับ turn ถัดไป
    st.session_state.last_prices[selected_stock] = prices[-1]

    months = ["เริ่มต้น"] + [f"เดือน {i+1}" for i in range(MONTHS)]


    df = pd.DataFrame({
        "เดือน": months,
        "ราคาหุ้น": prices,
        "ผล(%)": [None] + list(np.round(returns * 100, 2))
    })
    df["เดือน"] = pd.Categorical(df["เดือน"], categories=months, ordered=True)
    


    

    # แสดงกราฟและตาราง
    df_chart = pd.DataFrame({"เดือน": months, "ราคา": prices})
    df_chart["เดือน"] = pd.Categorical(df_chart["เดือน"], categories=months, ordered=True)
    df_chart = df_chart.sort_values("เดือน")  # <-- เรียงลำดับเดือนให้ถูกต้อง
    st.line_chart(df_chart.set_index("เดือน"))
    






# -------------------- ซื้อขายหุ้น --------------------
    # เตรียม state
    if "cash" not in st.session_state:
        st.session_state.cash = 10000
    if "portfolio" not in st.session_state:
        st.session_state.portfolio = {}

    current_price = prices[-1]  # ใช้ราคาที่ได้จาก session ไม่ต้องคำนวณใหม่



    col1, col2 = st.columns(2)
    with col1:
        st.subheader("ซื้อ-ขายหุ้น")
        st.markdown(f"💰 เงินสด: **{st.session_state.cash:,.2f}** บาท")
        st.markdown(f"📈 ราคาหุ้น {selected_stock} ปัจจุบัน: **{current_price:.2f}** บาท")

        # พอร์ตหุ้นตัวนี้
        stock_data = st.session_state.portfolio.get(selected_stock, {"จำนวน": 0, "ต้นทุนเฉลี่ย": 0.0})
        holding = stock_data["จำนวน"]
        avg_cost = stock_data["ต้นทุนเฉลี่ย"]

        st.markdown(f"📦 คุณถือหุ้น {selected_stock} จำนวน **{holding}** หุ้น (ต้นทุนเฉลี่ย {avg_cost:.2f})")
    with col2:
        st.subheader("📊 พอร์ตการลงทุน")
        total_value = 0
        port_data = []
        for stock, data in st.session_state.portfolio.items():
            qty = data["จำนวน"]
            avg_cost = data["ต้นทุนเฉลี่ย"]
            current = st.session_state.last_prices.get(stock, INITIAL_PRICE)
            total = current * qty
            total_value += total
            port_data.append({
                "หุ้น": stock,
                "จำนวน": qty,
                "ราคาปัจจุบัน": f"{current:.2f}",
                "มูลค่ารวม": f"{total:,.2f}"
            })

        df_port = pd.DataFrame(port_data)
        st.dataframe(df_port, use_container_width=True)
        st.markdown(f"💼 **มูลค่าทรัพย์สินรวม:** {total_value + st.session_state.cash:,.2f} บาท")


    # ฟอร์มซื้อขาย
    col1, col2, col3 = st.columns(3)
    with col1:
        buy_qty = st.number_input("จำนวนที่ต้องการซื้อ", min_value=0, step=1, key="buy_qty")
        if st.button("ซื้อหุ้น"):
            cost = buy_qty * current_price
            if cost > st.session_state.cash:
                st.warning("❌ เงินสดไม่พอสำหรับการซื้อ")
            elif buy_qty > 0:
                total_cost = holding * avg_cost + cost
                total_qty = holding + buy_qty
                avg_cost_new = total_cost / total_qty

                # อัปเดตพอร์ต
                st.session_state.portfolio[selected_stock] = {
                    "จำนวน": total_qty,
                    "ต้นทุนเฉลี่ย": avg_cost_new
                }
                st.session_state.cash -= cost
                st.success(f"✅ ซื้อ {buy_qty} หุ้น {selected_stock} แล้ว")
                st.rerun()

    with col2:
        sell_qty = st.number_input("จำนวนที่ต้องการขาย", min_value=0, max_value=holding, step=1, key="sell_qty")
        if st.button("ขายหุ้น"):
            if sell_qty > 0:
                revenue = sell_qty * current_price
                remaining_qty = holding - sell_qty
                st.session_state.cash += revenue

                # อัปเดตพอร์ต
                if remaining_qty > 0:
                    st.session_state.portfolio[selected_stock] = {
                        "จำนวน": remaining_qty,
                        "ต้นทุนเฉลี่ย": avg_cost
                    }
                else:
                    del st.session_state.portfolio[selected_stock]

            
                st.success(f"✅ ขาย {sell_qty} หุ้น {selected_stock} แล้ว ได้รับ {revenue:,.2f} บาท")
                st.rerun()




    # -------------------- ข่าว / การซื้อข่าว --------------------
    #ข่าวปีนี้
    with col3:
        st.subheader("📰 ข่าวสารประจำปี")

        current_turn = st.session_state.turn
        current_news = st.session_state.turn_news[current_turn]

        if st.session_state.news_bought_in_turn.get(current_turn, False):
            st.info(f"📌 ข่าวที่คุณซื้อสำหรับปีนี้: {current_news['text']}")
        else:
            if st.button("📩 ซื้อข่าว (500 บาท)"):
                if st.session_state.cash >= 500:
                    st.session_state.cash -= 500
                    st.session_state.news_bought_in_turn[current_turn] = True
                    st.success("✅ คุณซื้อข่าวสำเร็จ!")
                    st.rerun()
                else:
                    st.warning("❌ เงินไม่พอสำหรับซื้อข่าว")

    # -------------------- จบเทิร์น --------------------
    st.markdown("---")
    if st.button("➡️ จบเทิร์น"):
        current_turn = st.session_state.turn

        # ดึงข่าวของเทิร์นนี้ (ถ้าซื้อ) เพื่อส่งผลในเทิร์นถัดไป
        if st.session_state.news_bought_in_turn.get(current_turn, False):
            impact = st.session_state.turn_news[current_turn]["impact"]
            st.session_state.impact_next_turn[current_turn + 1] = impact
        else:
            st.session_state.impact_next_turn[current_turn + 1] = {}

        # เพิ่มเทิร์น
        st.session_state.turn += 1

        # ล้างค่าสำหรับเทิร์นถัดไป (ไม่ล้างข่าวที่สุ่มไว้นะ)
        st.session_state.news_bought_in_turn[st.session_state.turn] = False

        st.rerun()