import streamlit as st
import numpy as np

st.set_page_config(page_title="SW Damage Calculator", layout="centered")
st.title("Summoners War Expected Damage Calculator")

# --- State Toggle ---
lock = st.checkbox("🔒 Lock to 6000 damage", value=True)

# --- Inputs ---
benchmark = st.number_input("Target Damage Benchmark", min_value=1000, max_value=10000, step=100, value=6000)
fight_sets = st.slider("Number of Fight Sets", min_value=0, max_value=6, step=1, value=0)
atk_bonus = 1 + 0.08 * fight_sets

# --- Initialize session state for ATK and CD ---
if "atk" not in st.session_state:
    st.session_state.atk = 3000
if "cd" not in st.session_state:
    st.session_state.cd = 200
if "last_changed" not in st.session_state:
    st.session_state.last_changed = "cd"

if lock:
    col1, col2 = st.columns(2)
    with col1:
        atk_input = st.slider("Total ATK", min_value=2000, max_value=4000, step=10, value=st.session_state.atk, key="atk_slider")
    with col2:
        cd_input = st.slider("Crit Damage (%)", min_value=120, max_value=300, step=5, value=st.session_state.cd, key="cd_slider")

    # Detect which changed
    if atk_input != st.session_state.atk:
        st.session_state.last_changed = "atk"
    elif cd_input != st.session_state.cd:
        st.session_state.last_changed = "cd"

    if st.session_state.last_changed == "atk":
        st.session_state.atk = atk_input
        st.session_state.cd = round(100 + 100 * (benchmark / (st.session_state.atk * atk_bonus) - 1))
    else:
        st.session_state.cd = cd_input
        crit_multiplier = 1 + (st.session_state.cd - 100) / 100
        st.session_state.atk = round(benchmark / (atk_bonus * crit_multiplier))

    atk = st.session_state.atk
    cd = st.session_state.cd
else:
    atk = st.slider("Total ATK", min_value=2000, max_value=4000, step=10, value=3000)
    cd = st.slider("Crit Damage (%)", min_value=120, max_value=300, step=5, value=200)

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
