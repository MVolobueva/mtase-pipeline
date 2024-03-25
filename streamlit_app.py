import streamlit as st
import pandas as pd
import os
import etsv

##step 1
st.write(os.system('git clone https://github.com/isrusin/etsv'))
st.write(os.system('python3 -m pip install -e etsv'))
st.write('# MTase detection and classification pipeline')
st.sidebar.title("Pipeline steps")
st.sidebar.write('## Step 1')
uploaded_file = st.sidebar.file_uploader("Load sequences in fasta format")
if uploaded_file is not None:
    with open(os.path.join(".",uploaded_file.name),"wb") as f:
         f.write(uploaded_file.getbuffer())
    print(os.path.join(".",uploaded_file.name))                                
    os.system('hmmsearch --cpu 3 -E 0.01 --domE 0.01 --incE 0.01 --incdomE 0.01 \
        -o /dev/null --noali -A ./pipelineFiles/file.stk\
        ./pipelineFiles/selected_profiles.hmm ' + os.path.join(".",uploaded_file.name))
    st.sidebar.write('Step 1 finished')
    st.sidebar.write('## Step 2')
    os.system('rm ' + os.path.join(".",uploaded_file.name))                             
    os.system('./pipelineFiles/get_aln_regions.py \
    ./pipelineFiles/All_profile_region.csv \
    ./pipelineFiles/file.stk > ./pipelineFiles/region_alignments.tsv')
    st.dataframe(pd.read_csv('./pipelineFiles/region_alignments.tsv', sep='\t'))
    st.sidebar.write('Step 2 finished')
    st.sidebar.write('## Step 3')
    os.system('python ./pipelineFiles/classification.py \
  --t ./pipelineFiles/region_alignments.tsv\
  --m ./pipelineFiles/several_cat_domains.tsv\
  --c ./pipelineFiles/class.tsv')

    st.dataframe(pd.read_csv('./pipelineFiles/class.tsv', sep='\t'))

    st.dataframe(pd.read_csv('./pipelineFiles/several_cat_domains.tsv', sep='\t'))