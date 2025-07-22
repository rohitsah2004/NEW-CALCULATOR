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
    total_dose = int(weight * dose_per_kg)
    volume_required = int(total_dose / 47.6)
    vials_needed = math.ceil(total_dose / 500)
    iv_bag_size = "100 mL" if total_dose <= 1800 else "250 mL"
    ns_bag_volume = 100 if total_dose <= 1800 else 250
    remaining_ns = int(ns_bag_volume - volume_required)

    return f"""
📊 **PATIENT INFORMATION**  
• Weight: {int(weight)} kg  
• Prescribed Dose: {int(dose_per_kg)} mg/kg  

💊 **DOSAGE CALCULATIONS**  
• Total Dose: {total_dose} mg  
• Volume Required: {volume_required} mL  
• Vials Needed: {vials_needed}  
• IV Bag Size: {iv_bag_size}  

🧪 **PREPARATION STEPS**  
1. Use a {iv_bag_size} 0.9% Sodium Chloride bag  
2. Withdraw {volume_required} mL from the bag  
3. Inject 10 mL of SWFI into each of the {vials_needed} vial(s)  
4. Return {volume_required} mL to the remaining {remaining_ns} mL in the NS bag  

⚠️ **NOTES**  
• Concentration: 47.6 mg/mL  
• Stability: Use within 24 hours or refrigerate  
• Administer over 90 mins (1–2 infusions), then 60 mins (3–8 infusions)  
"""

def calculate_remicade(weight, dose_per_kg, infusion_type):
    total_dose = int(weight * dose_per_kg)
    volume_required = int(total_dose / 10)
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

    remaining_volume = int(bag_volume - volume_required)

    if infusion_type == "Induction":
        if bag_volume == 250:
            rate_info = """
Start at 10 mL/hr for 15 min  
Titrate to 20 mL/hr for 15 min  
Titrate to 40 mL/hr for 15 min  
Titrate to 80 mL/hr for 15 min  
Titrate to 150 mL/hr for 30 min  
Titrate to 250 mL/hr for the remainder
"""
        else:
            rate_info = """
Start at 20 mL/hr for 15 min  
Titrate to 40 mL/hr for 15 min  
Titrate to 80 mL/hr for 15 min  
Titrate to 160 mL/hr for 15 min  
Titrate to 300 mL/hr for 30 min  
Titrate to 500 mL/hr for the remainder
"""
    elif infusion_type == "Enhanced":
        if bag_volume == 250:
            rate_info = """
100 mL/hr for 15 min  
Then increase to 300 mL/hr for remainder
"""
        else:
            rate_info = """
200 mL/hr for 15 min  
Then increase to 600 mL/hr for remainder
"""
    elif infusion_type == "Standard":
        rate_info = "Infuse over 2 hours at 125 mL/hr"
    else:
        rate_info = "Please select a valid infusion type."

    return f"""
📊 **PATIENT INFORMATION**  
• Weight: {int(weight)} kg  
• Prescribed Dose: {int(dose_per_kg)} mg/kg  
• Infusion Type: {infusion_type}  

💉 **DOSAGE CALCULATIONS**  
• Total Dose: {total_dose} mg  
• Volume Required: {volume_required} mL  
• Vials Needed: {vials_needed}  
• IV Bag Size: {iv_bag_size}  

🧪 **PREPARATION STEPS**  
1. Use a {iv_bag_size} 0.9% Sodium Chloride bag  
2. Withdraw {volume_required} mL using 21g needle  
3. Inject 10 mL NS into each of the {vials_needed} vial(s)  
4. Return {volume_required} mL to the remaining {remaining_volume} mL in the NS bag  
5. Attach 0.2-micron filtered tubing  

⚠️ **INFUSION INSTRUCTIONS**  
{rate_info}  

⚠️ **NOTES**  
• Concentration: 10 mg/mL  
• Final infusion concentration: 0.4–4.0 mg/mL  
• Use immediately or refrigerate up to 24 hours  
"""

def calculate_benlysta(weight):
    dose = int(weight * 10)
    v400 = int(dose // 400)
    remaining = dose - (v400 * 400)
    v120 = math.ceil(remaining / 120) if remaining > 0 else 0
    total_mg = (v400 * 400) + (v120 * 120)
    waste = total_mg - dose
    total_volume = int((v400 * 5) + (v120 * 1.5))

    bag_size = 250 if weight > 40 else 100
    remaining_ns = int(bag_size - total_volume)

    return f"""
📊 **PATIENT INFORMATION**  
• Weight: {int(weight)} kg  
• Prescribed Dose: 10 mg/kg  

💊 **DOSAGE CALCULATIONS**  
• Total Dose: {dose} mg  
• Vials Needed: {v400} x 400 mg and {v120} x 120 mg  
• Total Volume: {total_volume} mL  
• Waste: {waste} mg  
• NS Bag: {bag_size} mL  

🧪 **PREPARATION STEPS**  
1. Use a {bag_size} mL 0.9% Sodium Chloride bag  
2. Withdraw and discard {total_volume} mL from NS bag  
3. Reconstitute each 400 mg vial with 4.8 mL SWFI (final = 5 mL)  
4. Reconstitute each 120 mg vial with 1.5 mL SWFI (final = 1.5 mL)  
5. Withdraw {total_volume} mL from vials and add to remaining {remaining_ns} mL NS  
6. ✅ **Protect from light with an amber IV cover bag**  
7. Attach non-filtered tubing  
8. Infuse over 1 hour at a rate of {bag_size} mL/hr  
"""

with st.form("dose_form"):
    weight = st.number_input("Patient Weight (kg)", min_value=0.0, format="%.0f")
    dose = 0
    infusion_type = ""

    if tab == "Tepezza":
        dose = st.number_input("Prescribed Dose (mg/kg)", min_value=0.0, format="%.0f")
    elif tab == "Remicade":
        dose = st.number_input("Prescribed Dose (mg/kg)", min_value=0.0, format="%.0f")
        infusion_type = st.selectbox("Select Infusion Type", ["", "Induction", "Standard", "Enhanced"])

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
                if infusion_type == "":
                    st.error("⚠️ Please select an infusion type for Remicade.")
                else:
                    st.markdown(calculate_remicade(weight, dose, infusion_type))

st.markdown("---")
st.caption("For healthcare use only. Always verify clinical decisions independently.")
