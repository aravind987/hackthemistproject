import pandas as pd

df = pd.read_csv('Dynamically Generated Hate Dataset v0.2.3.csv')

#class 0 will be nothate, class 1 will be general hate, class 2 will be racist

#get necessary rows & add final label
cleanedDf = df[['text','label','target']].copy()
cleanedDf['finalLabel'] = 'nothate'

for index,row in cleanedDf.iterrows():
    if row['label'] == 'hate':
        row['finalLabel'] = 'hate'

for index,row in cleanedDf.iterrows():
    if row['target'] in ['mixed','bla','blawom','ethnic minority','indig','indigwom','non-white','trav','african','jew','mus','muswom','asi','asiwom','east','south','chinese','pak','arab','eastern european','russian','pol','hispanic','nazi','hitler']:
        row['finalLabel'] = 'racism'

print((cleanedDf['finalLabel'] == 'nothate').sum())
print((cleanedDf['finalLabel'] == 'hate').sum())
print((cleanedDf['finalLabel'] == 'racism').sum())

cleanedDf.to_csv('out.csv')