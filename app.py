import re
import streamlit as st
from fuzzywuzzy import fuzz, process

# Preprocess a single string by removing noise and normalizing
def preprocess_string(s):
    s = s.lower()  # Convert to lowercase
    noise_words = [
        'pvt', 'ltd', 'india', 'motor', 'company', 'co', 'mt', 'petrol', 'diesel', 'tdci', 'bs', 'iv', 'o', 'trend',
        'kappa', 'sx', 'crdi', 'amt', 'titanium', 'ambient'
    ]
    for word in noise_words:
        s = s.replace(word, '')
    s = re.sub(r'[^a-z0-9]', ' ', s)  # Replace non-alphanumeric characters with space
    s = re.sub(r'\s+', ' ', s)  # Replace multiple spaces with single space
    return s.strip()


# Find the best match for a given user input from the database names
def find_best_match(user_input, database_names):
    processed_input = preprocess_string(user_input)  # Preprocess the user input
    processed_database = [preprocess_string(name.replace('_', ' ')) for name in database_names]  # Preprocess database names

    best_match_token_set, score_token_set = process.extractOne(processed_input, processed_database, scorer=fuzz.token_set_ratio)
    best_match_ratio, score_ratio = process.extractOne(processed_input, processed_database, scorer=fuzz.ratio)

    if score_token_set > score_ratio:
        best_match = best_match_token_set
        score = score_token_set
    else:
        best_match = best_match_ratio
        score = score_ratio

    original_name = database_names[processed_database.index(best_match)]

    return original_name, score

# Main function to handle user inputs and find best matches
def main():
    st.title("Vehicle Model Name Matcher")
    
    database_names = [
        "ford_aspire", "ford_ecosport", "ford_endeavour", "ford_figo",
        "honda_amaze", "honda_city", "honda_wr_v", "hyundai_aura",
        "hyundai_grand_i10", "hyundai_i10", "jeep_compass", "jeep_meridian",
        "kia_carens", "kia_seltos", "kia_sonet", "land_rover_defender",
        "mahindra_scorpio", "mahindra_thar", "mahindra_xuv300", "mahindra_xuv400",
        "mahindra_xuv700", "maruti_celerio", "maruti_suzuki_brezza", "maruti_suzuki_s_presso",
        "maruti_suzuki_swift", "maruti_suzuki_wagonr", "maruti_suzuki_xl6", "mg_astor",
        "mg_gloster", "mg_hector", "mg_zs_ev", "renault_kiger", "renault_triber",
        "skoda_kushaq", "skoda_slavia", "tata_harrier", "tata_punch", "tata_tiago",
        "toyota_camry", "toyota_fortuner", "toyota_fortuner_legender", "toyota_glanza",
        "toyota_innova_crysta"
    ]

    num_inputs = st.number_input("Enter the number of user inputs:", min_value=1, step=1, value=1)

    user_inputs = []
    for i in range(num_inputs):
        user_input = st.text_input(f"Enter user input {i + 1}:")
        user_inputs.append(user_input)

    for user_input in user_inputs:
        if user_input:
            best_match, confidence = find_best_match(user_input, database_names)
            st.write(f"User Input: {user_input}")
            st.write(f"Best Match: {best_match} - Confidence: {confidence:.2f}%")

if __name__ == "__main__":
    main()
