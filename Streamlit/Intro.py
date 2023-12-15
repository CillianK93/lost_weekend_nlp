import streamlit as st

import streamlit as st


def main():
    # Layout settings
    st.set_page_config(layout="wide")

    # Create columns for better layout. Adjust the widths as needed.
    col1, col2 = st.columns([1, 2])

    with col1:
        st.write("# Lost Weekend")
        st.write("### Sentiment Analysis vs Local Competitors.")
        st.write("""
                **Lost Weekend** is centrally located in the university area, providing great coffee and
                a relaxing atmosphere during the day. At night, we host exciting events to keep you entertained.
                """)
        st.write("Using Google reviews from us and our competitors, we aim to understand public opinions"
                 " highlighting our strengths and areas of improvement based on sentiment and topics from"
                 " our analysis.")

    with col2:
        st.write("## Gallery")
        st.write("Get a glimpse of what we offer:")

        # List of images with descriptions as tuples (description, path)
        images = [
            ("Lost", "images/lost_logo.png"),
            ("Theke", "images/theke.jpeg"),
            ("Music Night", "images/music.jpeg"),
            ("Coffee and Treats", "images/coffee.jpeg"),
            ("This Week's Events", "images/this_week.png")
        ]

        # Sidebar enhancements
        st.sidebar.header("Image Selector")
        st.sidebar.write("Choose an image from our gallery:")

        # Extract image descriptions for the radio selector
        image_descriptions = [img[0] for img in images]
        selected_description = st.sidebar.radio("", image_descriptions)

        # Fetch the corresponding image path for the selected description
        selected_image_path = next((img[1] for img in images if img[0] == selected_description), None)

        if selected_image_path:
            # Display the selected image with caption and adjusted width
            st.image(selected_image_path, caption=selected_description, width=600)
        else:
            st.warning("The selected image is missing. Please check the image path.")


if __name__ == "__main__":
    main()
