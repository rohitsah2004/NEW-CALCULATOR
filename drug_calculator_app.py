import streamlit as st
import math

st.set_page_config(page_title="Medical Drug Calculator", layout="centered")
st.title("💊 Medical Drug Calculator")
st.subheader("Professional Dosing Calculator for Tepezza, Remicade, and Benlysta")
st.markdown("---")

tab = st.radio("Select Drug", ["Tepezza", "Remicade", "Benlysta"])

def validate_input(weight, dose):
    if weight <= 0 or dose <= 0:
        st.error("⚠️ Weight and dose must be greater than 0.")
        return False
    if weight > 500:
        st.warning("Weight seems unusually high. Please verify.")
    return True

def calculate_tepezza(weight, dose_per_kg):
    total_dose = weight * dose_per_kg
    volume_required = total_dose / 47.6
    vials_needed = math.ceil(total_dose / 500)
    iv_bag_size = "100 mL" if total_dose <= 1800 else "250 mL"
    ns_bag_volume = 100 if total_dose <= 1800 else 250
    remaining_ns = ns_bag_volume - volume_required

    return f"""
📊 **PATIENT INFORMATION**  
• Weight: {weight:.1f} kg  
• Prescribed Dose: {dose_per_kg:.1f} mg/kg  

💊 **DOSAGE CALCULATIONS**  
• Total Dose: {total_dose:.1f} mg  
• Volume Required: {volume_required:.1f} mL  
• Vials Needed: {vials_needed}  
• IV Bag Size: {iv_bag_size}  

🧪 **PREPARATION STEPS**  
1. Use a {iv_bag_size} 0.9% Sodium Chloride bag  
2. Withdraw {volume_required:.1f} mL from the bag  
3. Inject 10 mL of SWFI into each of the {vials_needed} vial(s)  
4. Return {volume_required:.1f} mL to the remaining {remaining_ns:.1f} mL in the NS bag  

⚠️ **NOTES**  
• Concentration: 47.6 mg/mL  
• Stability: Use within 24 hours or refrigerate  
• Administer over 90 mins (1–2 infusions), then 60 mins (3–8 infusions)  
"""

def calculate_remicade(weight, dose_per_kg, infusion_type):
    total_dose = weight * dose_per_kg
    volume_required = total_dose / 10
    vials_needed = math.ceil(total_dose / 100)

    if total_dose > 2000:
        iv_bag_size = "two 500 mL bags"
        bag_volume = 1000
    elif total_dose > 1000:
        iv_bag_size = "500 mL"
        bag_volume = 500
    else:
        iv_bag_size = "250 mL"
        bag_volume = 250

    remaining_volume = bag_volume - volume_required

    rates = {
        "Induction": "Infuse over 2+ hours at 250 mL/hr",
        "Standard": "Infuse over 2 hours at 125 mL/hr",
        "Enhanced": "Infuse over 1 hour at 250 mL/hr"
    }

    return f"""
📊 **PATIENT INFORMATION**  
• Weight: {weight:.1f} kg  
• Prescribed Dose: {dose_per_kg:.1f} mg/kg  
• Infusion Type: {infusion_type}  

💉 **DOSAGE CALCULATIONS**  
• Total Dose: {total_dose:.1f} mg  
• Volume Required: {volume_required:.1f} mL  
• Vials Needed: {vials_needed}  
• IV Bag Size: {iv_bag_size}  

🧪 **PREPARATION STEPS**  
1. Use a {iv_bag_size} 0.9% Sodium Chloride bag  
2. Withdraw {volume_required:.1f} mL using 21g needle  
3. Inject 10 mL NS into each of the {vials_needed} vial(s)  
4. Return {volume_required:.1f} mL to the remaining {remaining_volume:.1f} mL in the NS bag  
5. Attach 0.2-micron filtered tubing  

⚠️ **NOTES**  
• Concentration: 10 mg/mL  
• Final infusion concentration: 0.4–4.0 mg/mL  
• Use immediately or refrigerate (good for 24 hrs)  
• {rates[infusion_type]}  
"""

def calculate_benlysta(weight):
    dose = weight * 10
    v400 = int(dose // 400)
    remaining = dose - (v400 * 400)
    v120 = math.ceil(remaining / 120) if remaining > 0 else 0
    total_mg = (v400 * 400) + (v120 * 120)
    waste = total_mg - dose
    total_volume = (v400 * 5) + (v120 * 1.5)

    bag_size = 250 if weight > 40 else 100
    remaining_ns = bag_size - total_volume

    return f"""
📊 **PATIENT INFORMATION**  
• Weight: {weight:.1f} kg  
• Prescribed Dose: 10 mg/kg  

💊 **DOSAGE CALCULATIONS**  
• Total Dose: {dose:.1f} mg  
• Vials Needed: {v400} x 400 mg and {v120} x 120 mg  
• Total Volume: {total_volume:.2f} mL  
• Waste: {waste:.1f} mg  
• NS Bag: {bag_size} mL  

🧪 **PREPARATION STEPS**  
1. Use a {bag_size} mL 0.9% Sodium Chloride bag  
2. Withdraw and discard {total_volume:.2f} mL from NS bag  
3. Reconstitute each 400 mg vial with 4.8 mL SWFI (final = 5 mL)  
4. Reconstitute each 120 mg vial with 1.5 mL SWFI (final = 1.5 mL)  
5. Withdraw {total_volume:.2f} mL from vials and add to remaining {remaining_ns:.2f} mL NS  
6. ✅ **Protect from light with an amber IV cover bag**  
7. Attach non-filtered tubing  
8. Infuse over 1 hour at a rate of {bag_size} mL/hr  
"""

with st.form("dose_form"):
    weight = st.number_input("Patient Weight (kg)", min_value=0.0, format="%.1f")
    dose = 0
    infusion_type = ""

    if tab == "Tepezza":
        dose = st.number_input("Prescribed Dose (mg/kg)", min_value=0.0, format="%.1f")
    elif tab == "Remicade":
        dose = st.number_input("Prescribed Dose (mg/kg)", min_value=0.0, format="%.1f")
        infusion_type = st.selectbox("Infusion Type", ["Induction", "Standard", "Enhanced"])

    submitted = st.form_submit_button("🧮 Calculate")

if submitted:
    if tab == "Benlysta":
        if validate_input(weight, 10):
            result = calculate_benlysta(weight)
            st.markdown(result)
    else:
        if validate_input(weight, dose):
            if tab == "Tepezza":
                st.markdown(calculate_tepezza(weight, dose))
            elif tab == "Remicade":
                st.markdown(calculate_remicade(weight, dose, infusion_type))

st.markdown("---")
st.caption("For healthcare use only. Always verify clinical decisions independently.")
