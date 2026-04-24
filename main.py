import streamlit as st 

# Game Parameters 
SNAKE_SELL_PRICE = 10
NUM_SNAKE_BABIES = 10   # Per pair
NEW_SNAKES_PER_ROUND = 4 
NUM_ROUNDS = 5

st.title("Snakes at the Biltmore!")

# Initialize Variables (Only done at start of game)
if "snakes" not in st.session_state:
    st.session_state.snakes = 5 
    st.session_state.money = 100 
    st.session_state.round = 1 
    st.session_state.history = []

    

# --- Display --- 
st.header(f'Round {st.session_state.round}')
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
if st.button('Decide'): 
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
