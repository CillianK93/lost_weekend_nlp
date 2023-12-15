import streamlit as st


import streamlit as st

def main():
    st.set_page_config(layout="wide")

    # Title
    st.title("Results and Recommendations from Overall Analysis")

    # Introduction or Context
    st.write("""
    Based on our analysis of word clouds, topic modeling, and feedback from customers, here are the major takeaways:
    """)

    # Positive Points for Your Business
    st.subheader("Positive Points for Our Business")
    st.write("""
    - **Cool Atmosphere**: Our ambiance is appreciated by many customers.
    - **Friendly Staff**: Our team's warmth and professionalism stand out.
    - **Nice Events**: Our events, especially the open stage, are well-received.
    """)

    # Negative Points for Your Business
    st.subheader("Areas of Improvement for Our Business")
    st.write("""
    - **Long Waiting Lines**: Some customers have pointed out the long wait times during peak hours.
    - **Wi-Fi Issues**: The Wi-Fi quality might not be suitable for study during the daytime.
    - **Inconsistency During Busy Times**: We need to maintain a consistent quality of service even during busy hours.
    """)

    # Positive Points for Competitors
    st.subheader("Strengths of Local Competitors")
    st.write("""
    - **Good Food**: Competitors are getting positive feedback on their food.
    - **Nice Service**: Friendly and efficient service seems to be a common trait.
    - **Nice Atmosphere**: Competitors also offer a pleasing environment, similar to ours.
    """)

    # Negative Points for Competitors
    st.subheader("Weaknesses of Local Competitors")
    st.write("""
    - **Rude Service**: Some competitors have instances of rude service.
    - **Unpleasant Door Security**: Feedback points to rude security personnel at entrances.
    - **Bad Drinks Quality**: Drink quality is an area where competitors can improve.
    """)

    # Recommendations or Next Steps
    st.subheader("Recommendations")
    st.write("""
    1. **Sort that Wifi out!**: Invest in better Wi-Fi infrastructure to cater to those who wish to study or work.
    2. **Streamline Workflow During Peak Hours**: Maybe introduce a more efficient queue management system.
    3. **Consistent Service Training**: Ensure all staff are trained to handle the rush during busy hours.
    4. **Monitor Competitor Strengths**: Keep an eye on the food and service quality of competitors to stay ahead.
    """)

if __name__ == "__main__":
    main()