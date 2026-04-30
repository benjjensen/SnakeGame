import streamlit as st 
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Game Parameters 
SNAKE_SELL_PRICE = 10
NUM_SNAKE_BABIES = 10   # Per pair
NEW_SNAKES_PER_ROUND = 4 
NUM_ROUNDS = 5


# Submits results to Google Sheets
def submit_results(team, cash, snakes):
    scope = ["https://www.googleapis.com/auth/spreadsheets"]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    client = gspread.authorize(creds)

    sheet = client.open_by_key("1lLNjuurhJtrafjrAT95_85JFBMu-UVHBNvbOtsnjcmk").sheet1

    # Team Name  |  Final Cash  |  Final Snake Count  |  Timestamp
    sheet.append_row([
        team, 
        cash,
        snakes,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ])


st.title("Snakes at the Biltmore!")

# Initialize Variables (Only done at start of game)
if "snakes" not in st.session_state:
    st.session_state.snakes = 5 
    st.session_state.money = 0 
    st.session_state.round = 1 
    st.session_state.history = []
    st.session_state.submitted = False


# --- Display --- 
st.header(f'Round {st.session_state.round}' if st.session_state.round <= NUM_ROUNDS else f'GAME OVER!')
st.metric('  Snakes: ', st.session_state.snakes) 
st.metric('  Money: ', st.session_state.money) 

# --- Action --- 
num_to_sell = st.slider(
    "How many snakes do you want to sell?", 
    min_value = 0, 
    max_value = st.session_state.snakes, 
    value = 0
)

st.write(f'Keeping {st.session_state.snakes - num_to_sell} snakes to breed')

# --- Resolve --- 
if st.session_state.round <= NUM_ROUNDS and st.button('Decide'): 
    snakes = st.session_state.snakes 
    money = st.session_state.money 

    # Sell snakes FIRST 
    money += (SNAKE_SELL_PRICE * num_to_sell)
    snakes -= num_to_sell 

    # Breed snakes 
    snakes += NUM_SNAKE_BABIES * (snakes // 2)  # 10 new snakes for every pair, rounding DOWN because they dont reproduce asexually
    snakes += NEW_SNAKES_PER_ROUND   # Get 4 new snakes each round

    # Save history 
    st.session_state.history.append( {
        'round': st.session_state.round, 
        'snakes': st.session_state.snakes, 
        'money': money
    })

    # Update State 
    st.session_state.snakes = snakes 
    st.session_state.money = money 
    st.session_state.round += 1

    st.rerun()


# --- End game --- 
if st.session_state.round > NUM_ROUNDS: 
    st.success(f'Final Score: {st.session_state.money}') 

    team = st.text_input("Team Name")

    if st.button("📤 Submit Score"):
        if not st.session_state.submitted:
            submit_results(team, st.session_state.money, st.session_state.snakes)
            st.session_state.submitted = True
            st.success("Score submitted!")
        else:
            st.info("You already submitted your score!")


# --- Chart --- 
if st.session_state.history: 
    st.line_chart({
        'Snakes': [h['snakes'] for h in st.session_state.history],
        'Money': [h['money'] for h in st.session_state.history],
    })


# --- Reset --- 
if st.button('Restart'): 
    st.session_state.clear() 
    st.rerun()


