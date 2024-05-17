import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import os
skillset = []

custom = ['(',',',')','-','_',':','.']
s = stopwords.words('english') + custom
lemma = WordNetLemmatizer()

nltk.download("wordnet")

def token(text):
    tokens = nltk.word_tokenize(text)
    stem = []
    for i in tokens:
        if i not in s:
            i = lemma.lemmatize(i)
            stem.append(i.split('.')[0])
    return stem
path = os.path.dirname(__file__) + '\\linkedin skill'
with open(path,'rb') as e:
    e = e.readlines()
    for i in e:
        i = i.decode('utf-8')
        i = token(i)
        skillset.append(i[0].lower())

def extract_contact_info(text):
    # Define regular expressions for email and phone number extraction
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b(?:\d{5}[-\s]??\d{6}|\d{10})\b'

    # Extract email addresses and phone numbers
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    stem = token(text)
    fi = []
    for i in stem:
        i = i.lower()
        if i in skillset:
            fi.append(i)
    l = list(set(fi))
    print(phones)
    ret = {
        "email":emails[0] if emails[0] else None,
        "number":phones[0] if phones[0] else None,
        "name":stem[0].upper(),
        "skills":l
    }
    return ret

def match(data):
    company=token(data['company'])
    s = []
    skills = []
    for i in range(0,len(data['employee'])):
        a = extract_contact_info(data['employee'][i])
        s.append(a)
        skills.append(s[i]['skills'])
    best_match = find_best_match(company, skills)
    i=0
    
    for match, percent in best_match:
        s[i]['percent'] = percent
        s[i]['matched']={}
        for sk, p in match:
            s[i]['matched'][sk] = p
        i = i+1
    return s

    


def find_best_match(company_skills, employer_skill_sets):
   
    all_matched_skills = []
    
    for employer_skills in employer_skill_sets:
        total_percentage = 0
        matched_skills = []
        
        for company_skill in company_skills:
            if company_skill in employer_skills:
                matched_skills.append((company_skill, 1.0))
                total_percentage += 1.0
            else:
                matched_skills.append((company_skill,0.0))
        
        average_percentage = (total_percentage*100) / len(company_skills)
        
        all_matched_skills.append(( matched_skills, round(average_percentage,2)))
        
      
    
    return all_matched_skills
