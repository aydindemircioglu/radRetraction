import pandas as pd
import webbrowser

# retraction watch database 
df = pd.read_csv("./data/RWD/retraction_watch.csv")
df = df.fillna('')
mask = df.astype(str).apply(lambda row: row.str.contains("radiomics", case=False, na=False)).any(axis=1)
df_filtered = df[mask]
df_filtered = df_filtered[["Author", "OriginalPaperDate", "Title", "Journal", "Publisher", "Country", "OriginalPaperDOI", "Reason"]]
df_filtered["Author"] = df_filtered["Author"].apply(
    lambda x: x.split(";")[0].strip().split()[-1] + " et al."
)
df_filtered["Date"] = pd.to_datetime(df_filtered["OriginalPaperDate"], errors='coerce').dt.year
df_filtered = df_filtered.drop(["OriginalPaperDate"], axis = 1).copy()
df_filtered = df_filtered.rename(columns={"OriginalPaperDOI": "DOI", "Author": "Authors"})
df_RWD = df_filtered.copy()
print (f"Have {len(df_RWD)} publications from RWD.")

# pubmed
df = pd.read_csv("./data/PubMed/csv-radiomics-set.csv")
df = df.rename(columns={
    'Author': 'Authors',
    'Title': 'Title',
    'Journal/Book': 'Journal',
    'Publication Year': 'Date',
    'DOI': 'DOI'
})
desired_columns = df_RWD.keys()
for col in desired_columns:
    if col not in df.columns:
        df[col] = ''
df_PubMed = df[desired_columns].copy()
print (f"Have {len(df_PubMed)} publications from pubmed.")



# web of science
df = pd.read_csv("./data/WoS/savedrecs.txt", sep = '\t')
wos_to_rwd = {
    'AU': 'Authors',
    'TI': 'Title',
    'SO': 'Journal',
    'PU': 'Publisher',
    'PA': 'Country',
    'DI': 'DOI',
    'DA': 'Date'
}
df = df.rename(columns={k: v for k, v in wos_to_rwd.items() if k in df.columns})
desired_columns = df_RWD.keys()
for col in desired_columns:
    if col not in df.columns:
        df[col] = ''
df["Authors"] = df["Authors"].apply(
    lambda x: x.split(",")[0].strip().split()[-1] + " et al."
)
df_WoS = df[desired_columns].copy()
df_WoS["Country"] = ''
df_WoS["Date"] = pd.to_datetime(df_WoS["Date"], errors='coerce').dt.year
print (f"Have {len(df_WoS)} publications from wos.")



# scopus
df = pd.read_csv("./data/Scopus/scopus.csv")
scopus_to_wos = {
    'Source title': 'Journal',
    'Year': 'Date'
}
df_renamed = df.rename(columns={k: v for k, v in scopus_to_wos.items() if k in df.columns})
desired_columns = df_RWD.keys()
for col in desired_columns:
    if col not in df_renamed.columns:
        df_renamed[col] = ''
df_scopus = df_renamed[desired_columns].copy()
df_scopus["Authors"] = df_scopus["Authors"].apply(
    lambda x: x.split(" ")[0].strip().split()[-1] + " et al."
)
print (f"Have {len(df_scopus)} publications from scopus.")



# merge and save
df_final = pd.concat([df_WoS, df_scopus, df_PubMed, df_RWD], ignore_index=True)
print (f"Have overall {len(df_final)} publications.")
has_doi = df_final['DOI'].str.strip() != ''
df_with_doi = df_final[has_doi]
df_without_doi = df_final[~has_doi]
df_with_doi_nodup = df_with_doi.drop_duplicates(subset='DOI', keep='first')
df_merged_clean = pd.concat([df_with_doi_nodup, df_without_doi], ignore_index=True)

df_merged_clean['Title'] = df_merged_clean['Title'].str.replace(r'^(RETRACTION: |RETRACTED: )', '', case=False, regex=True)
df_merged_clean.to_csv("./results/table_raw.csv")
print (f"Have  {len(df_merged_clean)} publications after removing duplicates.")


# we used this to automatically open all papers, caution, it will open 100 tabs!!!
if 1 == 0:
    firefox = webbrowser.get('/Applications/Firefox.app/Contents/MacOS/firefox')
    for i, doi in enumerate(df_merged_clean['DOI']):
        doi = str(doi).strip()
        if doi:
            url = f'https://doi.org/{doi}'
            webbrowser.open_new_tab(url)
