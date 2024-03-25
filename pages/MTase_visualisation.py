### Step 1) Imports
import stmol
import streamlit as st
import py3Dmol
from stmol import showmol
import pandas as pd


#color MTase chain in red
def color_MTase(df):
    MTasechain = {'chain':hl_chain}
    view.setStyle(MTasechain,{'cartoon':{'color':'blue'}})
    #view.addResLabels({"chain": hl_chain,"resi": 1-10})

    a = tuple(df[df['REBASE_name'] == option].iloc[0]['Region_coords'].split(','))
    b = tuple(df[df['REBASE_name'] == option].iloc[0]['Regions'].split(','))
    i1 = 0

    l1 = ''
    if hl_chain:
        for i,l in zip(a,b):
            if i1 != 0 and i1+1 < int(i.split('-')[0]) and l1 != 'sam_motif' and l1 != 'cat_motif':

                for k in range(i1+1, int(i.split('-')[0])):
                    view.setStyle({'resi': k, 'chain': hl_chain}, {'cartoon': {'color': 'green'}})

            if l == 'sam_motif' or l == 'cat_motif':

                for k in range(int(i.split('-')[0]), int(i.split('-')[1]) + 1):
                    view.setStyle({'resi': k, 'chain': hl_chain}, {'cartoon': {'color': 'red'}})
            else:
                for k in range(int(i.split('-')[0]), int(i.split('-')[1]) + 1):
                    view.setStyle({'resi': k, 'chain': hl_chain}, {'cartoon': {'color': 'yellow'}})
            i1 = int(i.split('-')[1])
            l1 =  l
    else:
            st.error("Please paste chain")


#original
st.sidebar.title("Settings")

uploaded_file = st.sidebar.file_uploader("Choose a file with MTase classes\
    from [MTase classification pipline](https://github.com/MVolobueva/MTase-classification/blob/main/Classification_pipeline.ipynb)")
uploaded_file_pdb = st.sidebar.file_uploader("Choose PBD file")
st.markdown(
    f"# DNA-methyltransferases (MTases) classes")
option = 'M.HhaI'
k = 1
if uploaded_file is not None:
    k = 0
    df = pd.read_csv(uploaded_file, sep = '\t', index_col=0)
    option = st.selectbox(
    'What MTase would you like to analyse?',
    df['REBASE_name'],
    index=None)
    if not option:
        st.error("Please choose MTase")
    else:
        st.write('You selected:', option)
        st.write(df[df['REBASE_name'] == option][['REBASE_name', 'New_class', 'Regions', 'Region_coords']])
    pdb_code = st.sidebar.text_input(
        label="PDB Code")
    if not pdb_code and uploaded_file_pdb is None:
        st.sidebar.error("Please paste PDB code or paste PDB file")
    else:
        k=1

        hl_chain = st.sidebar.text_input(label="Choose MTase chain")

        hl_resi_list = st.sidebar.multiselect(label="Highlight Residues", options=list(range(1, 5000)))

        label_resi = st.sidebar.checkbox(label="Label Residues", value=True)

        surf_transp = st.sidebar.slider("Surface Transparency", min_value=0.0, max_value=1.0, value=0.0)

        hl_color = st.sidebar.text_input(label="Highlight Color",value="red")

        bb_color = st.sidebar.text_input(label="Backbone Color",value="lightgrey")
        lig_color = st.sidebar.text_input(label="Ligand Color",value="white")


        st.markdown(
            f"## MTase {option} from class {df[df['REBASE_name'] == option].iloc[0]['New_class']}: PDB [{pdb_code.upper()}](https://www.rcsb.org/structure/{pdb_code}) (Chain {hl_chain})")
else:
    df = pd.read_csv('./class_withStructure1.tsv', sep='\t', index_col=0)
    st.write('## Prokaryotic MTases with available 3D structure')
    option = st.selectbox(
        'What MTase would you like to analyse?',
        df['REBASE_name'],
        index= 1)
    st.write(df[df['REBASE_name'] == option][['REBASE_name', 'New_class', 'Repr. PDB code', 'Regions', 'Region_coords']].style.format({"Expense": lambda x : '{:.4f}'.format(x)}))
    pdb_code = st.sidebar.text_input(
        label="PDB Code",
        value= df[df['REBASE_name'] == option].iloc[0]['Repr. PDB code'])

    hl_chain = st.sidebar.text_input(label="Choose MTase chain", value="A")

    hl_resi_list = st.sidebar.multiselect(label="Highlight Residues", options=list(range(1, 5000)))

    label_resi = st.sidebar.checkbox(label="Label Residues", value=True)

    surf_transp = st.sidebar.slider("Surface Transparency", min_value=0.0, max_value=1.0, value=0.0)

    hl_color = st.sidebar.text_input(label="Highlight Color",value="red")

    bb_color = st.sidebar.text_input(label="Backbone Color",value="lightgrey")
    lig_color = st.sidebar.text_input(label="Ligand Color",value="white")


    st.markdown(
        f"## MTase {option} from class {df[df['REBASE_name'] == option].iloc[0]['New_class']}: PDB [{pdb_code.upper()}](https://www.rcsb.org/structure/{pdb_code}) (Chain {hl_chain})")


### Step 3) Py3Dmol

width = 700
height = 700

cartoon_radius = 0.2
stick_radius = 0.2

if k!= 0:
    st.write('MTase chain is green. Sam-motif and cat-motif are red.\
     Elements detected by hmm-profiles are yellow.\
     Loops between detected elements are green.')
    if uploaded_file_pdb is not None and not pdb_code:
        view = stmol.obj_upload(uploaded_file_pdb)
    else:
        view = py3Dmol.view(query=f"pdb:{pdb_code.lower()}", width=width, height=height)

    view.setStyle({"cartoon": {"style": "oval","color": bb_color,"thickness": cartoon_radius}})

    view.addSurface(py3Dmol.VDW, {"opacity": surf_transp, "color": bb_color},{"hetflag": False})

    view.addStyle({"elem": "C", "hetflag": True},
                    {"stick": {"color": lig_color, "radius": stick_radius}})

    view.addStyle({"hetflag": True},
                        {"stick": {"radius": stick_radius}})

    for hl_resi in hl_resi_list:
        view.addStyle({"chain": hl_chain, "resi": hl_resi, "elem": "C"},
                        {"stick": {"color": hl_color, "radius": stick_radius}})

        view.addStyle({"chain": hl_chain, "resi": hl_resi},
                            {"stick": {"radius": stick_radius}})

    if label_resi:
        for hl_resi in hl_resi_list:
            view.addResLabels({"chain": hl_chain,"resi": hl_resi},
            {"backgroundColor": "lightgray","fontColor": "black","backgroundOpacity": 0.5})
    color_MTase(df)

    showmol(view, height=height, width=width)