import streamlit as st  # Import streamlit module
import pandas as pd
import pickle

# Load the pickle file containing recommendations
with open("most_recommended_mobile_phones.pkl", 'rb') as f:
    recommended_df = pickle.load(f)

# List of Mobile_data to choose from - mobile prices, brands, ratings, and images
Mobile_data = {
    'Mobile_Brand': ["SAMSUNG", "OnePlus", "POCO", "Motorola", "realme"],  # brand information
    'Model':["SAMSUNG Galaxy A14 5G", "OnePlus Nord CE 3 Lite 5G", "POCO M6 Plus 5G", "Motorola g45 5G", "realme P1 5G"],
    'Price': ['₹11,499', '₹14,888', '₹11,499', '₹10,999', '₹14,999'],  # price in INR
    'Rating': [4.2, 4.4, 4.2, 4.3, 4.4],
    'image': [
        'https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/2/y/c/-original-imah4sssdf9pgz3e.jpeg?q=70',
        'https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/p/r/b/nord-ce-3-lite-5g-ce2099-oneplus-original-imagzj42cctpjjze.jpeg?q=70',
        'https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/9/b/n/-original-imah3afnqj84usyy.jpeg?q=70',
        'https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/b/y/x/-original-imah3xk8crpgrg9y.jpeg?q=70',
        'https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/j/b/n/-original-imahyuhfzvybhaat.jpeg?q=70']
     # image URLs
}

# Create a DataFrame for visualization
df = pd.DataFrame(Mobile_data)

# Remove '₹' symbol and commas from the 'Price' column and convert it to integer
df['Price'] = df['Price'].replace({'₹': '', ',': ''}, regex=True).astype(int)

# Merge df1 with recommended_df (assuming 'Model' is the key column)
df = pd.merge(df, recommended_df, left_on='Model', right_on='Product_name', how='inner')

# Streamlit Title of the app
st.title('Mobile Product Recommendations')
st.write("### Based on sentiment analysis from Reviews and Recommendations:")

# Sidebar for filtering options
st.sidebar.header('Filter Options')

# Multiselect for multiple Brand selection
brand_options = df['Model'].unique().tolist()
selected_brands = st.sidebar.multiselect("Select Brands:", options=brand_options)

# Price filter slider
min_price, max_price = st.sidebar.slider('Select price range (in INR):', min_value=11000, max_value=15000, value=(11000, 15000))

# Rating filter slider
min_rating = st.sidebar.slider('Select minimum rating', min_value=0.0, max_value=5.0, value=3.0)

# Filter data based on user input
if selected_brands:
    filtered_data = df[(df['Price'] >= min_price) & (df['Price'] <= max_price) & (df['Rating'] >= min_rating)]
    filtered_data = filtered_data[filtered_data['Model'].isin(selected_brands)]
    st.write(f'Showing results for products priced between ₹{min_price} and ₹{max_price} with rating above {min_rating}')

    if filtered_data.empty:
        st.write("No products found matching the selected criteria.")
    else:
        st.subheader(f"You Selected : {', '.join(selected_brands)}")

        # Display individual recommendations
        for i, row in filtered_data.iterrows():
            st.subheader(f"**{row['Model']}**")
            st.image(row['image'], width=150)
            st.write(f"Price: ₹{row['Price']}")
            st.write(f"Rating: {row['Rating']} ⭐")

            # Create a prompt using the loaded recommendation template
            prompt = f"""

            **Based on sentiment analysis, we recommend the following mobile phone:**

            **Model**: {row['Product_name']}
            - **Positive review score**: {row['average_compound_score']:.2f}
            - **Positive Sentiment score**: {row['average_compound_sentiment']}
            """

            st.write(prompt)
            st.write("---")
else:
    st.write("No brand selected yet.")
# streamlit Flipkart_streamlit.py
