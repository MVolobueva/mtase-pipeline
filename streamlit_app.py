import streamlit as st


#st.set_page_config(
#    page_title="DNA-MTases"
#)
#from st_pages import Page, show_pages, add_page_title

# Optional -- adds the title and icon to the current page
#add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles 
# and icons should be

st.write("# Welcome DNA methyltransferase (MTases) site!")

st.markdown(
        """
        These site devoted to prokaryotic DNA Methyltransferases (МТases). 
        ### Site structure

        - Brief overview of MTases structure and classes  
        - Running MTase detection and classification [pipeline](https://mtase-pipeline-6g1yfq9ugw8.streamlit.app/MTase_detection_and_classification)
        - Visualization of pipeline [results](https://mtase-pipeline-6g1yfq9ugw8.streamlit.app/MTase_visualisation)
        ### Overview
        MTases are classified into [6 classes](https://www.biorxiv.org/content/10.1101/2023.12.13.571470v1).
        All class are grouped into 6 groups on sequence similarity of catalytic motif (figure below).
    """
    )

st.image('pipelineFiles/abstract.jpg')
