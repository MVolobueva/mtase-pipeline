import streamlit as st
import pandas as pd
import os
import etsv

k = os.system('./pipelineFiles/get_aln_regions.py \
  ./pipelineFiles/All_profile_region.csv \
  ./pipelineFiles/file.stk > ./pipelineFiles/region_alignments.tsv')

#dddkk

st.write(k)