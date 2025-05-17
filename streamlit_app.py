import streamlit as st
import numpy as np

st.set_page_config(page_title="SW Damage Calculator", layout="centered")
st.title("Summoners War Expected Damage Calculator")

# --- State Toggle ---
lock = st.checkbox("🔒 Lock to 6000 damage", value=True)

# --- Inputs ---
fight_sets = st.slider("Number of Fight Sets", min_value=0, max_value=6, step=1, value=0)
atk_bonus = 1 + 0.08 * fight_sets
benchmark = 6000

if lock:
    col1, col2 = st.columns(2)
    with col1:
        atk = st.slider("Total ATK", min_value=2000, max_value=4000, step=10, value=3000, key="locked_atk")
    with col2:
        cd = st.slider("Crit Damage (%)", min_value=120, max_value=300, step=5, value=200, key="locked_cd")

    # Decide which slider changed by tracking session state
    if "last_atk" not in st.session_state:
        st.session_state.last_atk = atk
    if "last_cd" not in st.session_state:
        st.session_state.last_cd = cd

    if atk != st.session_state.last_atk:
        # ATK was changed → update CD
        cd = 100 + 100 * (benchmark / (atk * atk_bonus) - 1)
        cd = round(cd)
        st.session_state.locked_cd = cd
    elif cd != st.session_state.last_cd:
        # CD was changed → update ATK
        crit_multiplier = 1 + (cd - 100) / 100
        atk = benchmark / (atk_bonus * crit_multiplier)
        atk = round(atk)
        st.session_state.locked_atk = atk

    # Save last values
    st.session_state.last_atk = atk
    st.session_state.last_cd = cd
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
