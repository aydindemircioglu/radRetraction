import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import webbrowser

journal_normalizing_dict = {
    "MEDICAL PHYSICS": "Medical Physics",
    "Med Phys": "Medical Physics",
    "Journal of Healthcare Engineering": "Journal of Healthcare Engineering",
    "CANCERS": "Cancers",
    "BioMed Research International": "BioMed Research International",
    "BIOMED RESEARCH INTERNATIONAL": "BioMed Research International",
    "Scanning": "Scanning",
    "APPLIED BIONICS AND BIOMECHANICS": "Applied Bionics and Biomechanics",
    "COMPUTATIONAL AND MATHEMATICAL METHODS IN MEDICINE": "Computational and Mathematical Methods in Medicine",
    "J Oncol": "Journal of Oncology",
    "ADVANCES IN MATERIALS SCIENCE AND ENGINEERING": "Advances in Materials Science and Engineering",
    "Journal of Intelligent and Fuzzy Systems": "Journal of Intelligent and Fuzzy Systems",
    "CONTRAST MEDIA & MOLECULAR IMAGING": "Contrast Media & Molecular Imaging",
    "OXIDATIVE MEDICINE AND CELLULAR LONGEVITY": "Oxidative Medicine and Cellular Longevity",
    "Functional and Integrative Genomics": "Functional and Integrative Genomics",
    "STEM CELLS INTERNATIONAL": "Stem Cells International",
    "Concurrency and Computation: Practice and Experience": "Concurrency and Computation: Practice and Experience",
}


reason_normalizing_dict = {
    "Standard WILEY/Hindawi": "Standard text",
    "This action has been agreed due to an error at the publisher which caused a duplicate of the article to be published online": "Duplicate article",
    "retraction has been agreed on as the peer review and publishing process was found to be manipulated. Furthermore, the authors included incoherent, meaningless, and irrelevant information in this article. The underlying dataset is not referenced correctly and a detailed description of the applied methods is missing so that the results cannot be considered reproducible": "Manipulated peer review, irreproducible",
    "Institutional Review Board approval in this study": "IRB missing",  
    "evidence of systematic manipulation of the publication and peer-review process": "Systematic manipulation",
    "major overlap with a previously published article": "Major overlap",
    "peer review process underlying the articles was inadequate. We have no evidence to suggest authors were involved": "Inadequate peer review",
    "including but not limited to compromised editorial handling and peer review process, inappropriate or irrelevant references or not being in scope of the journal or guest-edited issue": "Compromised editorial/peer review",
}


df = pd.read_excel("./results/table_raw.xlsx", header = 1)
df = df.iloc[0:92].copy()
df['Journal'] = df['Journal'].map(journal_normalizing_dict).fillna(df['Journal'])
df["Reason_Code"] = df["Unnamed: 0"]

assert np.sum(df["Reason_Code"] == "I") == np.sum(df["Exclude"] == 0.0)

df['Reason'] = df['Reason'].map(reason_normalizing_dict).fillna(df['Reason'])

print(df.Reason_Code.value_counts())


df_rad = df.query("Reason_Code == 'I'").copy()
df_rad = df_rad.drop(["Unnamed: 0", "Reason_Code", "Exclude" ], axis = 1)
df_rad = df_rad.sort_values(["Date"])
df_rad.to_excel("./results/table_relevant.xlsx")

# open publications for further investigation
if 1 == 1:
    firefox = webbrowser.get('/Applications/Firefox.app/Contents/MacOS/firefox')
    for i, doi in enumerate(df_rad['DOI']):
        doi = str(doi).strip()
        if doi:
            url = f'https://doi.org/{doi}'
            webbrowser.open_new_tab(url)


#
