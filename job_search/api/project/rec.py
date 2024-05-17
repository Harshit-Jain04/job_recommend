import pickle
import nltk
import re
from nltk.stem import WordNetLemmatizer
import os
lemma=WordNetLemmatizer()
job_df = pickle.load(open(os.path.dirname(__file__)+'\\job_df_sample1.pkl','rb'))
similarity = pickle.load(open(os.path.dirname(__file__)+'\\similarity_sample1.pkl','rb'))
def recommend(title):
        title = title.lower().split(" ")
        #print(len(title))
        if len(title)>1:
            #print("l")
            word1 = lemma.lemmatize(title[0])
            word2 = lemma.lemmatize(title[-1])
            title = fr"\b{re.escape(word1)}\b(?:\s+\w+)*\s+\b{re.escape(word2)}\b"
        else:
            title = lemma.lemmatize(title[0])
        try:
            indx = job_df[job_df['Job Title'].str.contains(title)].index[0]
            
        except (IndexError) as e:
            try:
                indx =  job_df[job_df['clean'].str.contains(title)].index[0]
            except (IndexError) as e:
                return "err"
        #indx = job_df[job_df['Position'] == title].index[0]
        indx = job_df.index.get_loc(indx)
        distances = sorted(list(enumerate(similarity[indx])), key=lambda x: x[1], reverse=True)
        jobs = []
        h = 0
        for i in range(len(distances)):
            #jobs.append(job_df.iloc[i[0]].Title)
            
            z = distances[i]
            tem = job_df.iloc[z[0]]
            try:
                x = distances[i+1]
            except (IndexError) as e:
                continue
            zen = job_df.iloc[x[0]]
            if tem['Job Title']==zen['Job Title'] and tem['Role']==zen['Role'] and tem['Job Description']==zen['Job Description']:
                continue
            ret = {
                'title':tem['Job Title'],
                'role':tem['Role'],
                'company':tem['Company'],
                'description':tem['Job Description'],
                'experience':tem['Experience'],
                'qualifications':tem['Qualifications'],
                'salary':tem['Salary Range'],
                'location':tem['location'],
                'time':tem['Work Type'],
                'responsibility':tem['Responsibilities'],
                'skills':tem['skills']
            }
            jobs.append(ret)
            h+=1
            if h==10:
                return jobs
        return jobs
#print(job_df['Job Title'][:5])
