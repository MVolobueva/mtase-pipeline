import streamlit as st


st.set_page_config(
    page_title="Main Page",  # Вкладка в браузере
    page_icon=":guardsman:",
)


st.write("# Welcome DNA methyltransferase (MTases) site!")

st.markdown(
        """
        These site devoted to prokaryotic DNA Methyltransferases (МТases). 
        ### Site structure

        - Brief overview of MTases structure and classes  
        - Running MTase detection and classification [pipeline](https://mtase-pipeline.streamlit.app/MTase_detection_and_classification)
        - Visualization of pipeline [results](https://mtase-pipeline.streamlit.app/MTase_visualisation)
        ### Overview
        MTases are classified into [6 classes](https://www.biorxiv.org/content/10.1101/2023.12.13.571470v1).
        All class are grouped into 6 groups on sequence similarity of catalytic motif (figure below).
    """
    )

st.image('pipelineFiles/abstract.jpg')
