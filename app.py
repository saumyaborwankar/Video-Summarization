import streamlit as st
from streamlit_func import ShowVideo, VideoToAudio, ShowAudio, Generate_summary, clear_file
import io
page = st.sidebar.selectbox("Select a page", ["App"])
#page = st.sidebar.selectbox("Select a page", ["App"])
st.set_option('deprecation.showfileUploaderEncoding', False)


if page == "App":
    
    st.title('App')
    st.markdown('<h1> Upload your video here to create summary </h1>',unsafe_allow_html=True)
    uploaded_file = None

    uploaded_file = st.file_uploader("Choose your video file...")
    temporary_location = False
    
    if uploaded_file is not None:
        g = io.BytesIO(uploaded_file.read())  ## BytesIO Object
        #clear_file('streamlit/data/videos')
        temporary_location = "data/videos/sample.mp4"
        
        with open(temporary_location, 'wb') as out:  ## Open temporary file as bytes
            out.write(g.read())  ## Read bytes into file

        # close file
        out.close()
        ShowVideo(temporary_location)
    
    #check_data = st.checkbox("See the sample video")
    

    st.markdown('<h1> To generate the summary click the below button </h1>',unsafe_allow_html=True)
    sumOption=st.radio("Generate summary?", ('No', 'Yes'))
    if sumOption=='Yes':
    #check_data = st.checkbox("Generate summary")
        VideoToAudio(temporary_location)
        ShowAudio('output/sample.wav')
        #Generate_summary()
        #ShowVideo("output/video/final_video.mp4")

        
