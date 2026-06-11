import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy import stats

#aesthetic setting:
sns.set_theme(style= "whitegrid", palette= "muted")
plt.rcParams.update({"figure.dpi": 120, "font.size": 11})


#2. Loading dataset
df = pd.read_csv("D:\int_task\main_crafts\student-mat.csv", sep = ";")
print(f"dataset loaded : {df.shape[0]} rows x {df.shape[1]} cols")
print(df.head())


#3. Explore & Data Cleaning:


#3.1 Dataset shape & datatypes.......
print("shape :", df.shape)
print()
print("Colund Data Types :")
print(df.dtypes.to_string())

#3.2 checking missing values........
missing = df.isnull().sum()
print("missing values per column :")
if missing.sum() == 0:
    print("no missing values found in any column")
else:
    print(missing[missing > 0])
print("Total missing cells :", missing.sum())

#3.3 Remove Duplicates.........
dupes = df.duplicated().sum()
df.drop_duplicates(inplace = True)
print("Duplicate rows found :", dupes)
print("Rows after deduolication :", len(df))

# 3.4 Statistical summary........
print(df.describe().round(2))



#4. Analysis Questions.....

#4.1 Average final grade (G3)
#'G3' is final period grade on a 0-20 scale (output target)

avg_g3 = df['G3'].mean()
median_g3 = df['G3'].median()
std_g3 = df['G3'].std()


print(f"Average final Grade (G3) : {avg_g3:.2f} / 20")
print(f"Median  final Grade (G3) : {median_g3:.2f} / 20")
print(f"Std Dev                  : {std_g3:.2f} ")
print(f"Min / Max                : {df['G3'].min()} / {df['G3'].max()}")

# 4.2 how many students scored above 15?

above_15 = (df['G3'] > 15).sum()
pct = above_15 / len(df) * 100
print(f"Students scoring G3 > 15 : {above_15} out of {len(df)} ({pct:.1f}%)")

#4.3 Is Study Time Correlated with Performance ?
# 'studytime' is ordinal variable coded 1-4 :
# -1 = < 2 hrs/week
# -2 = 2-5 hrs/week
# -3 = 5-10 hrs/week
# -4 = > 10 hrs/week
#
# we use Pearson r to measure linear correlation and a p-value to assess significance.

corr, pval = stats.pearsonr(df['studytime'], df['G3'])
print(f"Pearson r (studytime vs G3) : {corr:.4f}")
print(f"P-value                     : {pval:.4f}")

if pval < 0.05:
    direction = "positive" if corr > 0 else "negative"
    print(f"\n Statistically significant {direction} correlation (p < 0.05)")
else : 
    print("\n Correlation is not statistically significant (p > 0.05)")

print("\n Average G3 by study time level :")
print(df.groupby('studytime')['G3'].mean().round(2)
      .rename(index= {1:'1 (<2 hrs)', 2:'2 (2-5 hrs)', 3:'3(5-10 hrs)', 4:'4 (>10 hrs)'}))


#4.4 which gender performs better on average 
# We compare mean G3 between Male('M') and Female('F') students and run an independent-samples t-test

gender_avg = df.groupby('sex')['G3'].agg(['mean', 'median', 'std', 'count']).round(2)
gender_avg.index = gender_avg.index.map({'F' : 'Female', 'M' : 'Male'})
print("G3 Statistics by Gender : ")
print(gender_avg)

male_g3 = df[df['sex'] == 'M']['G3']
female_g3 = df[df['sex'] == 'F']['G3']
t_stat, p_val = stats.ttest_ind(male_g3, female_g3)
print(f"\nIndependent t-test : t = {t_stat:.3f}, p = {p_val:.4f}")
if p_val < 0.05:
    better = "Males" if male_g3.mean() > female_g3.mean() else "Females"
    print(f"Statistically significant difference - {better} score higher on average.")
else :
    print("No Statistically significant difference between genders (p >= 0.05).")



# 5. Visualizations................ :


#5.1 Histogram - Distribution of final grades(G3)

fig, ax = plt.subplots(figsize = (9,5))

ax.hist(df['G3'], bins=21, range = (-0.5, 20.5),
        color = 'steelblue', edgecolor = 'white', linewidth = 0.8, alpha = 0.9)
ax.axvline(df['G3'].mean(), color = 'red', linestyle = '--', linewidth = 2,
         label = f'Mean  = {df['G3'].mean():.2f}')
ax.axvline(df['G3'].median(), color = 'goldenrod', linestyle = ':', linewidth = 2,
           label = f'Median = {df['G3'].median():.0f}')
ax.axvspan(15.5, 20.5, alpha = 0.07, color = 'green', label = 'score > 15')

ax.set_title("Distribution of Final Grades(G3)", fontsize = 14, fontweight = 'bold', pad = 12)
ax.set_xlabel('Final Grade (G3) [0-20 scale]', fontsize = 12)
ax.set_ylabel('Number of Stuents', fontsize = 12)
ax.set_xlim(-0.5, 20.5)
ax.legend(fontsize = 10)
sns.despine()
plt.tight_layout()
plt.savefig('plot_grade_histogram.png', bbox_inches = 'tight')
plt.show()
print("Saved : plot_grade_histogram.png")


#5.2 Scatter plot - Study Time vs. Final Grade :

fig, ax = plt.subplots(figsize = (9,5))

np.random.seed(0)
jx = df['studytime'] + np.random.uniform(-0.15, 0.15, len(df))
jy = df['G3'] + np.random.uniform(-0.25, 0.25, len(df))

sc = ax.scatter(jx, jy, c=df['G3'], cmap = 'RdYlGn', 
                alpha = 0.65, edgecolors = 'none', s = 55, vmin = 0, vmax = 25)

m, b, r, p, _ = stats.linregress(df['studytime'], df['G3'])
xl = np.linspace(0.8, 4.2, 100)
ax.plot(xl, m*xl + b, color = 'steelblue', linewidth = 2.5,
        label = f'Trend r = {r:.3f}, p = {r:.3f}' )


ax.set_xticks([1, 2, 3, 4])
ax.set_xticklabels(['< 2hrs\n(1)', '2-5hrs\n(2)', '5-10hrs\n(3)', '> 10hrs\n(4)'])
ax.set_xlabel('Study Time (weekly category)', fontsize = 12)
ax.set_ylabel('Finsl Grade (G3)', fontsize = 12)
ax.set_title('Study Time Final Grade(G3)', fontsize = 14, fontweight = 'bold', pad = 12)
ax.legend(fontsize = 10)
plt.colorbar(sc, ax=ax, label = 'G3 Grade')
sns.despine()
plt.tight_layout()
plt.savefig('plot_studytime_scatter.png', bbox_inches = 'tight')
plt.show()
print('saved : plot_studytime_scatter.png')
print('correlation coeff :', r)
    

#5.3 Bar Chart - Male Vs. Female avg score:

fig, axes = plt.subplots(1, 2, figsize = (11,5))

# left - bar chart with 95% CI error bars
gs = df.groupby('sex')['G3'].agg(['mean', 'sem']).reset_index()
gs['label'] = gs['sex'].map({'F' : 'Female', 'M' : 'Male'})


colors = ['#E87E8A','#5B9BD5']
bars = axes[0].bar(gs['label'], gs['mean'],
                   yerr = gs['sem']*1.96, color = colors,
                   edgecolor = 'white', linewidth = 1.2,
                   capsize = 6, error_kw = dict(elinewidth = 1.5, ecolor = '#444'))

for bar, val in zip(bars, gs['mean']):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                 f'{val:.2f}', ha = 'center', va = 'bottom', fontweight = 'bold', fontsize = 12)
    
axes[0].axhline(df['G3'].mean(), color = 'grey', linestyle = '--', linewidth = 1.3, alpha = 0.7,
                label = f'Overall mean = {df['G3'].mean():.2f}')
axes[0].set_ylim(0, 20)
axes[0].set_title('Average Final Grade By Gender', fontsize = 13, fontweight = 'bold')
axes[0].set_xlabel('Gender', fontsize = 11)
axes[0].set_ylabel('Average G3 Grade', fontsize = 11)
axes[0].legend(fontsize = 9)

# Right - violin plot:
df_p = df.copy()
df_p['Gender'] = df_p['sex'].map({'F' : 'Female', 'M' : 'Male'})
sns.violinplot(data = df_p, x = 'Gender', y = 'G3',
               palette= {'Female':'#E87E8A','Male':'#5B9BD5'},
               inner = 'box', ax = axes[1], linewidth= 1.2)
axes[1].set_title('Grade distribution by Gender', fontsize = 13, fontweight = 'bold')
axes[1].set_xlabel('Gender', fontsize = 11)
axes[1].set_ylabel('Final Grade G3', fontsize = 11)

sns.despine()
plt.tight_layout()
plt.savefig('plot_gender_bar.png', bbox_inches = 'tight')
plt.show()
print('Saved : plot_gender_bar.png')


#5.4 Correlation Heatmap of numeric features :
num_cols = ['age', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures',
            'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences', 'G1', 'G2', 'G3']

corr_matrix = df[num_cols].corr()
mask = np.triu(np.ones_like(corr_matrix, dtype= bool))

fig, ax = plt.subplots(figsize = (12,9))
sns.heatmap(corr_matrix, mask= mask, annot= True, fmt = '.2f',
            cmap = 'coolwarm', center = 0, vmin=-1, vmax= 1,
            linewidths= 0.5, ax= ax, annot_kws= {'size' : 8})
ax.set_title('Correlation Heatmap - Numeric Features', fontsize = 14, fontweight= 'bold', pad=15)
plt.tight_layout()
plt.savefig('plot_correlation_heatmap.png', bbox_inches = 'tight')
plt.show()
print('Saved : plt_correlation_heatmap.png')


