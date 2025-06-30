import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

 
df_rad = pd.read_excel("./results/table_final.xlsx")

#df_rad.to_excel("./results/Table_X.xlsx")

df_rad['Country'].value_counts()
df_rad['Publisher'].value_counts()

# overwrite date, since it was faulty
df_rad["Date"] = df_rad["Publication date"].dt.year

df_rad["Months to Retraction"] = (
    (df_rad["Retraction date"].dt.year - df_rad["Publication date"].dt.year) * 12 +
    (df_rad["Retraction date"].dt.month - df_rad["Publication date"].dt.month)
)


# beautify it for paper 
pub_year = df_rad["Publication date"].dt.year
ret_year = df_rad["Retraction date"].dt.year
df_b = pd.DataFrame()
df_b["Authors"] = df_rad["Authors"]
df_b["Date"] = pub_year.astype(str) + " (" + ret_year.astype(str) + ")"
df_b["Journal"] = df_rad["Journal"]
df_b["Publisher"] = df_rad["Publisher"]
df_b["Country"] = df_rad["Country"]

df_b["Citations"] = (
    df_rad["Citations"].astype(str) +
    " (" +
    df_rad["Citations prior retraction"].astype(str) +
    "/" +
    df_rad["Citation after retraction"].astype(str) +
    ")"
)

df_b["DOI"] = df_rad["DOI"]
df_b["_Year"] = pub_year
df_b = df_b.sort_values(by=["_Year", "Authors"]).drop(columns=["_Year"])
df_b.to_excel("./results/Table_1.xlsx", index=False)


print ("Median Month-to-retraction:", np.median(df_rad["Months to Retraction"]))
print ("min/max Month-to-retraction:", np.min(df_rad["Months to Retraction"]), np.max(df_rad["Months to Retraction"]))

 


fig = plt.figure(figsize=(10,12))
gs = fig.add_gridspec(3, 2)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1])
ax5 = fig.add_subplot(gs[2, 0])
ax6 = fig.add_subplot(gs[2, 1])

pub_counts = df_rad['Publisher'].value_counts()
colmap = sns.light_palette("#37a797", n_colors=len(pub_counts)+3)[::-1]
ax1.pie(pub_counts, labels=pub_counts.index, autopct='%1.0f%%', colors=colmap)
ax1.set_title('Publications per Publisher', fontweight='bold', fontsize=14)

cty_counts = df_rad['Country'].value_counts()
colmap = sns.light_palette("#a73737", n_colors=len(cty_counts)+3)[::-1]
ax2.pie(cty_counts, labels=cty_counts.index, autopct='%1.0f%%', colors=colmap)
ax2.set_title('Publications per Country', fontweight='bold', fontsize=14)

reason_colors = {
    'Major overlap': '#ff9999',
    'Standard text': '#cccccc',
    'Systematic manipulation': '#cc5555',
    'Duplicate article': '#5555cc',
    'Inadequate peer review': '#99ccff'
}
reason_counts = df_rad['Reason'].value_counts()
colors = [reason_colors.get(reason, '#ffffff') for reason in reason_counts.index]
ax3.pie(reason_counts, labels=reason_counts.index, autopct='%1.0f%%', colors=colors, startangle=0)
ax3.set_title('Reasons for Retraction', fontweight='bold', fontsize=14)

df_rad['Retraction_Year'] = df_rad['Retraction date'].dt.year
all_years = list(range(df_rad['Retraction_Year'].min(), 2026))
df_rad['Retraction_Year_cat'] = pd.Categorical(df_rad['Retraction_Year'], categories=all_years, ordered=True)
colmap = sns.light_palette("#9737a7", n_colors=10)[2:]
sns.countplot(data=df_rad, x='Retraction_Year_cat', palette=colmap, ax=ax4, legend=False)
ax4.set_title('Retractions per Year', fontweight='bold', fontsize=14)
ax4.set_ylabel('Count')
ax4.set_xlabel('Year')


citations = [
    df_rad['Citations'].sum(),
    df_rad['Citations prior retraction'].sum(),
    df_rad['Citation after retraction'].sum()
]
labels = ['Total', 'Prior', 'After']
colors = ['#999999', '#44aa44', '#aa4444']
ax5.bar(labels, citations, color=colors)
ax5.set_title('Citations', fontweight='bold', fontsize=14)
ax5.set_ylabel('Citations')

bins = list(range(0, df_rad['Months to Retraction'].max() + 4, 3))
sns.histplot(df_rad['Months to Retraction'], bins=bins, kde=False, ax=ax6, color="#5566aa")
ax6.set_title('Months to Retraction', fontweight='bold', fontsize=14)
ax6.set_xlabel('Months')
ax6.set_ylabel('Count')
ax6.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

for ax, label in zip([ax1, ax2, ax3, ax4, ax5, ax6], ['A', 'B', 'C', 'D', 'E', 'F']):
    ax.text(-0.15, -0.05, label, transform=ax.transAxes,
            fontsize=16, fontweight='bold', ha='left', va='top')

plt.tight_layout(h_pad=3.0)
plt.savefig('./results/Figure_2.png', dpi=300)
plt.close()
