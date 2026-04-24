import streamlit as st 

st.title("Snake Economy")

# Initialize Variables
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
action = st.radio('Choose your action: ', ['Breed', 'Sell']) 

# --- Resolve --- 
if st.button('Decide'): 
    snakes = st.session_state.snakes 
    money = st.session_state.money 

    if action == 'Breed':
        snakes += snakes // 2
    elif action == 'Sell': 
        money += snakes * 10    # Sell ALL for $10 each 
        snakes = 0  

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
if st.session_state.round > 10: 
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
