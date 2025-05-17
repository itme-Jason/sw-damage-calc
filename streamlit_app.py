
import streamlit as st
import numpy as np

st.set_page_config(page_title="SW Damage Calculator", layout="centered")
st.title("Summoners War Expected Damage Calculator")

# --- Inputs ---
atk = st.slider("Total ATK", min_value=2000, max_value=4000, step=10, value=3000)
cd = st.slider("Crit Damage (%)", min_value=120, max_value=300, step=5, value=200)
fight_sets = st.slider("Number of Fight Sets", min_value=0, max_value=6, step=1, value=0)

# --- Calculation ---
atk_bonus = 1 + 0.08 * fight_sets
crit_multiplier = 1 + (cd - 100) / 100
expected_damage = atk * atk_bonus * crit_multiplier

# --- Output ---
st.markdown("---")
st.subheader("Results")
st.write(f"**Expected Damage:** `{expected_damage:,.0f}`")

# Benchmark comparison
benchmark = 6000
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
- Uses formula: `ATK * (1 + 0.08 × Fight Sets) × (1 + (CD - 100)/100)`
- 6000 damage benchmark is based on 3000 ATK and 200% CD with no Fight sets

You can drag the sliders above to test different builds.
""")
