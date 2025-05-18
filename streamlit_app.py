import streamlit as st
import numpy as np

st.set_page_config(page_title="SW Damage Calculator", layout="centered")
st.title("Summoners War Expected Damage Calculator")

# --- State Toggle ---
lock = st.checkbox("🔒 Lock to 6000 damage", value=True)

# --- Inputs ---
benchmark = st.number_input("Target Damage Benchmark", min_value=1000, max_value=10000, step=100, value=6000)

# --- Placeholder until defined below ---
fight_sets = 0

# --- Initialize session state for ATK and CD ---
if "atk" not in st.session_state:
    st.session_state.atk = 3000
if "cd" not in st.session_state:
    st.session_state.cd = 200
if "last_changed" not in st.session_state:
    st.session_state.last_changed = "cd"

if lock:
    # Track previous values to detect slider activity
    previous_atk = st.session_state.atk
    previous_cd = st.session_state.cd
    previous_fight = st.session_state.get("fight_sets", 0)

    atk = st.slider("Total ATK", min_value=2000, max_value=4000, step=10, value=previous_atk, key="atk_slider")
    cd = st.slider("Crit Damage (%)", min_value=120, max_value=300, step=5, value=previous_cd, key="cd_slider")
    fight_sets = st.slider("Number of Fight Sets", min_value=0, max_value=6, step=1, value=previous_fight, key="fight_sets")
    atk_bonus = 1 + 0.08 * fight_sets

    if fight_sets != previous_fight:
        st.session_state.fight_sets = fight_sets
        atk_bonus = 1 + 0.08 * fight_sets
        crit_multiplier = 1 + (cd - 100) / 100
        atk = round(benchmark / (atk_bonus * crit_multiplier))
        st.session_state.atk = atk
    elif atk != previous_atk:
        st.session_state.atk = atk
        crit_multiplier = benchmark / (st.session_state.atk * atk_bonus)
        st.session_state.cd = round((crit_multiplier - 1) * 100 + 100)
    elif cd != previous_cd:
        st.session_state.cd = cd
        crit_multiplier = 1 + (st.session_state.cd - 100) / 100
        st.session_state.atk = round(benchmark / (atk_bonus * crit_multiplier))

    atk = st.session_state.atk
    cd = st.session_state.cd
    fight_sets = st.session_state.fight_sets
    atk_bonus = 1 + 0.08 * fight_sets
atk_bonus = 1 + 0.08 * fight_sets


    
# --- Unlocked Mode ---
else:
    atk = st.slider("Total ATK", min_value=2000, max_value=4000, step=10, value=3000, key="atk_unlocked")
    cd = st.slider("Crit Damage (%)", min_value=120, max_value=300, step=5, value=200, key="cd_unlocked")
    fight_sets = st.slider("Number of Fight Sets", min_value=0, max_value=6, step=1, value=0, key="fight_unlocked")
    atk_bonus = 1 + 0.08 * fight_sets

# --- Calculation ---
crit_multiplier = 1 + (cd - 100) / 100
expected_damage = atk * atk_bonus * crit_multiplier

# --- Output ---
st.markdown("---")
st.subheader("Results")
st.write(f"**Expected Damage:** `{expected_damage:,.0f}`")

# Benchmark comparison
pct = expected_damage / benchmark * 100
if expected_damage >= benchmark:
    st.success(f"✅ You exceed the 6000 damage benchmark ({pct:.1f}%)")
else:
    st.warning(f"⚠️ You are at {pct:.1f}% of the 6000 damage benchmark")

# --- Explanation ---
st.markdown("""
---
#### How it Works
- Assumes 100% Crit Rate
- Formula: `ATK * (1 + 0.08 × Fight Sets) × (1 + (CD - 100)/100)`
- 6000 damage benchmark = 3000 ATK + 200% CD (no Fight sets)

When locked, adjusting ATK or CD will auto-calculate the other to match 6000 expected damage.
""")
