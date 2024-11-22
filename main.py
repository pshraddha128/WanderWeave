import streamlit as st
import pickle
from poi_trialmerged import FINAL
import pandas as pd
import streamlit.components.v1 as components
import folium

st.set_page_config(
    page_title="Personalized Travel Recommendation",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
    
)

# Custom styles
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    .stApp {
        background-color: #c4dec4;
        font-family: 'Poppins', sans-serif;
        
        
    }
    
    .output-font{
        
        font-size: 21px;
        background-color: #c4dec4 !important;
    }
    .selectbox{
      font-size: 30px;
      background-color: #c4dec4 !important;
    }
    .form{
      font-family: 'Poppins', sans-serif;
      background-color: #c4dec4 !important;
    }
    .cheader {
        font-size:40px;
        background-color: #c4dec4 !important;
        
    }
    .hotel-bold {
        font-bold;
    }
    .hotel-font {
        font-size:30px
    }
    .button {
        background-color: #c4dec4;
        text-white rounded-md px-8 py-4 cursor-pointer transition-colors duration-300 hover:bg-blue-600 font-semibold text-4xl;
    }
    .input-label {
      background-color: #c4dec4;
      font-size: 30px;
    }
    .multiselect{
      font-size: 30px;
    }
    .error {
      text-red-600 font-medium;
    }
    .form{p
        background-color: #ffffff !important; 
        padding: 20px; 
        border-radius: 10px;
        border: 5px solid black;
    }
    .container{
      background-color: #c4dec4 !important;
      border: 2px solid black !important;
    }
      
    
        /* Navbar container */
    .navbar {
        display: flex;
        justify-content: center;
        background-color: #c4dec4;
        font-size: 40px;
        padding: 14px 0;
        border-bottom: 2px solid black;
        border-top: 2px solid black;
    }

    /* Navbar links */
    .navbar a {
        color: black;
        padding: 14px 20px;
        text-decoration: none;
        font-size: 27px;
        font-family: 'Poppins', sans-serif;
    }

    /* Change color on hover */
    .navbar a:hover {
        color: #86AB89;
    }
    
    /* Active/current link */
    .navbar a.active {
        color: #86AB89;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
col1, col2 = st.columns([1, 3])  # Adjust the width ratio as needed

# Place the image in the first column
with col1:
    st.image("hot-air-balloon.png", width=230)  # Adjust width as needed

# Place the navigation bar in the second column
with col2:
#st.image('hot-air-balloon.png',width=250)
# HTML for the navbar links
    st.markdown(
        """
        <div class="navbar">
            <a  href="#home" target="_self">Home</a>
            <a href="#Blogs" target="_self">Blogs</a>
            <a href="#Contact" target="_self">Contact</a>
        </div>
        """,
        unsafe_allow_html=True
    )


pickle_in = open("lol.pkl", "rb")
load_lol = pickle.load(pickle_in)

def welcome():
    return "Welcome All"

def output_main(Type, Duration, Budget, TYPE, Ques):
    output, info = FINAL(Type, Duration, Budget, TYPE, Ques)
    return [output, info]

def main():
    @st.cache_data
    def get_data():
        return []

    lis1 = ['Adventure and Outdoors', 'Spiritual', 'City Life', 'Cultural', 'Relaxing']
    lis2 = ['Family', 'Friends', 'Individual']
    with st.container():
      with st.form(key='travel_recommendation_form',border=True):
          st.markdown('<div class="form-container">', unsafe_allow_html=True)  # Start of form container

          st.markdown('<p class="input-label">Vacation type according to priority:</p>', unsafe_allow_html=True)
          Type = st.multiselect("", lis1)

          st.markdown('<p class="input-label">Duration (days):</p>', unsafe_allow_html=True)
          Duration = st.slider("", min_value=1, max_value=15, value=1)

          st.markdown('<p class="input-label">Budget (INR):</p>', unsafe_allow_html=True)
          Budget = st.slider("", min_value=200, max_value=25000, step=500, value=200)

          col1, col2 = st.columns(2)
          with col1:
              st.markdown('<p class="input-label">Who are you travelling with?</p>', unsafe_allow_html=True)
              TYPE = st.selectbox("", lis2)
          with col2:
              st.markdown('<p class="input-label">Is covering maximum places a priority?</p>', unsafe_allow_html=True)
              Ques = st.radio("", ['Yes', "No"])

          submit_button = st.form_submit_button(label='What do you recommend?', use_container_width=True)
   
    if submit_button:
        if not Type:
            st.error("Please select at least one vacation type.")
            return

        cutoff = Budget / Duration
        if cutoff < 260:
            st.subheader("Irrational. Try increasing your Budget or scaling down the Duration")
            return

        try:
            RESULT = output_main(Type, Duration, Budget, TYPE, Ques)
            get_data().append({"Type": Type, "Duration": Duration, "Budget": Budget, "TYPE": TYPE, "Ques": Ques})
            FINAL_DATA = pd.DataFrame(get_data())
            FINAL_DATA.to_csv('data/FinalData.csv')

            Output = RESULT[0]
            Info = RESULT[1]

            #st.subheader('Your Inputs', anchor="your-inputs")
            #st.write('{}'.format(Info[0]))
            #col3, col4 = st.columns(2)
            #for i in range(1, len(Info) - 5):
             #   try:
              #      col3.write('{}'.format(Info[i]))
               ##    continue
            #for i in range(4, len(Info) - 2):
             #   try:
              #      col4.write('{}'.format(Info[i]))
               # except:
                #    continue
            #st.write('{}'.format(Info[-2]))
            st.markdown('<h1 class="cheader">Suggested Itinerary</h1>', unsafe_allow_html=True)

            st.header('', anchor="suggested-itinerary")
            st.markdown(
                '<p class="hotel-font"><span class="hotel-bold">Suggested Hotel/Accommodation:</span> {}<p>'.format(
                    Info[-1]), unsafe_allow_html=True)
            st.write(' ')
            for i in range(0, len(Output)):
                st.markdown('<p class="output-font">{}</p>'.format(Output[i]), unsafe_allow_html=True)
            
        except Exception as e:
            
            st.error("Please check your inputs and try again.")
            
    st.markdown(
                """
                <div class="contact-info">
                    <h2>Contact Us</h2>
                    <p>If you have any questions, feel free to reach out!</p>
                    <p><strong>Email:</strong> support@example.com</p>
                    <p><strong>Phone:</strong> +1234567890</p>
                </div>
                """,
                unsafe_allow_html=True,
            )         

if __name__ == '__main__':
    main()