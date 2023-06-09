# -*- coding: utf-8 -*-
"""Twitter_Data_Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1H_knisuivM1ZFOPfJuDgdwbxQpoGGoQo

### Importing dataset
"""

from sys import platform
#utilities
import pandas as pd
import numpy as np
import re
import string
#plotting
import seaborn as sns
from wordcloud import WordCloud
import matplotlib.pyplot as plt
#nltk
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
#sklearn
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, classification_report, confusion_matrix, f1_score


from textblob import TextBlob
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

df = pd.read_csv('twitter-data.csv', encoding= 'unicode_escape')

df.head()

df.shape

df.info()

df.groupby('companies').count()

df['sentiment'].value_counts()

df_maruti = df[df['companies']== 'Maruti Suzuki']
df_maruti['sentiment'].value_counts()

label = ['Negative', 'Neutral', 'Positive']
plt.pie(df_maruti.groupby('sentiment')['sentiment'].count(), autopct="%.1f%%", labels=label)
plt.show()

df_tata = df[df['companies']=='Tata Motors']
df_tata['sentiment'].value_counts()

label = ['Negative', 'Neutral', 'Positive']
plt.pie(df_tata.groupby('sentiment')['sentiment'].count(), autopct="%.1f%%", labels=label)
plt.show()

df_mah = df[df['companies']=='Mahindra & Mahindra']
df_mah['sentiment'].value_counts()

label = ['Negative', 'Neutral', 'Positive']
plt.pie(df_mah.groupby('sentiment')['sentiment'].count(), autopct="%.1f%%", labels=label)
plt.show()

"""#### Visualising the Data"""

sent_map={0:'Negative sentiment', 1:'Positive Sentiment', 2:'Neutral Sentiment'}

import warnings
warnings.filterwarnings('ignore')

#cprint("Total number of sentiments of tweets :",'green')
print(df.sentiment.value_counts())
plt.figure(figsize=(8, 6))
ax = sns.countplot(x ='sentiment', data = df)
ax.set_title(label = 'Total number of sentiments of tweets', fontsize = 20) 
plt.show()

label = ['Negative', 'Neutral', 'Positive']
plt.pie(df.groupby('sentiment')['sentiment'].count(), autopct="%.1f%%", labels=label)
plt.show()

colors = sns.color_palette('husl', 10)
pd.Series(df['companies']).value_counts().plot(kind='bar', color=colors, figsize=(10,8), fontsize=10, rot=0, title='Total Number of tweets for each Automobile Company')
plt.xlabel('Company', fontsize=10)
plt.ylabel('Number of tweets', fontsize = 10)

pd.DataFrame(df.groupby('companies')['sentiment'].value_counts()).unstack().plot.barh(figsize=(10,10), stacked=True)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=10)
plt.show()

import seaborn as sns
sns.countplot(x='sentiment', data=df)

"""### Word Counts"""

df['tweet'][2]

df['word_counts']=df['tweet'].apply(lambda x:len(str(x).split()))
df.head()

"""### Converting HTML entities"""

# Converting html entities i.e. (&lt; is converted to "<" and &amp; is converted to "&")
from html.parser import HTMLParser

html_parser = HTMLParser()

df['tweet'] = df['tweet'].apply(lambda x: html_parser.unescape(x))
df.head()

"""### Cleaning and removing punctuations"""

import string
english_punctuations = string.punctuation
punctuations_list = english_punctuations
def cleaning_punctuations(text):
  translator = str.maketrans('', '', punctuations_list)
  return text.translate(translator)

#applying the function to our dataset
df['tweet'] = df['tweet'].apply(lambda x: cleaning_punctuations(x))
df.head()

"""### Cleaning and Removing repeating characters"""

def cleaning_repeating_char(text):
  return re.sub(r'(.)1+', r'1', text)
df['tweet'] = df['tweet'].apply(lambda x: cleaning_repeating_char(x))
df.head()

"""### Cleaning and Removing Numerics"""

def cleaning_numbers(data):
  return re.sub('[0-9]+', '', data)

df['tweet'] = df['tweet'].apply(lambda x: cleaning_numbers(x))
df.head()

"""### Case Folding (converting tweets into lowercase)"""

df['tweet'] = df['tweet'].apply(lambda x: x.lower())
df.head()

"""### Removing words with length 1"""

df['tweet'] = df['tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>1]))
df['tweet'].head()

"""### Replacing Special Characters with space"""

df['tweet'] = df['tweet'].apply(lambda x: re.sub(r'[^a-zA-Z0-9]', ' ', x))
df.head()

"""### Stop words Removal"""

# Removing stopwords using spacy

df['tweet'] = df['tweet'].apply(lambda x: ' '.join([t for t in x.split() if t not in STOP_WORDS]))

df['tweet'].head()

df.head()

"""### Short word lookup"""

short_word_dict = {
"121": "one to one",
"a/s/l": "age, sex, location",
"adn": "any day now",
"afaik": "as far as I know",
"afk": "away from keyboard",
"aight": "alright",
"alol": "actually laughing out loud",
"b4": "before",
"b4n": "bye for now",
"bak": "back at the keyboard",
"bf": "boyfriend",
"bff": "best friends forever",
"bfn": "bye for now",
"bg": "big grin",
"bta": "but then again",
"btw": "by the way",
"cid": "crying in disgrace",
"cnp": "continued in my next post",
"cp": "chat post",
"cu": "see you",
"cul": "see you later",
"cul8r": "see you later",
"cya": "bye",
"cyo": "see you online",
"dbau": "doing business as usual",
"fud": "fear, uncertainty, and doubt",
"fwiw": "for what it's worth",
"fyi": "for your information",
"g": "grin",
"g2g": "got to go",
"ga": "go ahead",
"gal": "get a life",
"gf": "girlfriend",
"gfn": "gone for now",
"gmbo": "giggling my butt off",
"gmta": "great minds think alike",
"h8": "hate",
"hagn": "have a good night",
"hdop": "help delete online predators",
"hhis": "hanging head in shame",
"iac": "in any case",
"ianal": "I am not a lawyer",
"ic": "I see",
"idk": "I don't know",
"imao": "in my arrogant opinion",
"imnsho": "in my not so humble opinion",
"imo": "in my opinion",
"iow": "in other words",
"ipn": "I’m posting naked",
"irl": "in real life",
"jk": "just kidding",
"l8r": "later",
"ld": "later, dude",
"ldr": "long distance relationship",
"llta": "lots and lots of thunderous applause",
"lmao": "laugh my ass off",
"lmirl": "let's meet in real life",
"lol": "laugh out loud",
"ltr": "longterm relationship",
"lulab": "love you like a brother",
"lulas": "love you like a sister",
"luv": "love",
"m/f": "male or female",
"m8": "mate",
"milf": "mother I would like to fuck",
"oll": "online love",
"omg": "oh my god",
"otoh": "on the other hand",
"pir": "parent in room",
"ppl": "people",
"r": "are",
"rofl": "roll on the floor laughing",
"rpg": "role playing games",
"ru": "are you",
"shid": "slaps head in disgust",
"somy": "sick of me yet",
"sot": "short of time",
"thanx": "thanks",
"thx": "thanks",
"ttyl": "talk to you later",
"u": "you",
"ur": "you are",
"uw": "you’re welcome",
"wb": "welcome back",
"wfm": "works for me",
"wibni": "wouldn't it be nice if",
"wtf": "what the fuck",
"wtg": "way to go",
"wtgp": "want to go private",
"ym": "young man",
"gr8": "great"
}

def lookup_dict(text, dictionary):
  for word in text.split():
    if word.lower() in dictionary:
      if word.lower() in text.split():
        text = text.replace(word, dictionary[word.lower()])
  return text

df['tweet'] = df['tweet'].apply(lambda x: lookup_dict(x, short_word_dict))
df.head()

"""### Word Tokenisation"""

# Importing stop words from NLTK corpus and word tokenizer

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# creating token for clean tweets

df['tweet_token'] = df['tweet'].apply(lambda x: word_tokenize(x))

## Fully formatted tweets and their tokens
df.head()

"""### Stop Word Removal"""

# Removing stopwords using spacy
df['tweet_token'] = df['tweet_token'].apply(lambda x: ([t for t in x if t not in STOP_WORDS]))

df.head()

"""### Text Analysis

#### Lexicon based approach
#### Vader
"""

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
vader = SentimentIntensityAnalyzer()
vader.polarity_scores(" ".join(df.tweet_token[0]))

texts = [" ".join(df.tweet_token[i]) for i in range(len(df))]

print(df.tweet[0])
print(texts[0])
print(vader.polarity_scores(texts[0]), f'--> Actual Classification: {df.sentiment[0]}','\n')

"""### Sentence Normalisation using Stemming and Lemmatization

#### We will create two new columns for Stemming and Lemmatization 
##### The difference between stemming and Lemmatization is that lemmatization considers the context and converts the word to its meaningful base form, while stemming just removes the last few characters, often leading to incorrect meanings and spelling errors.

### **Stemming** - Refers to the removal of suffices like "ing", "ly", "s", etc by a simple rule-based approach
"""

# Importing library for stemming
from nltk.stem import PorterStemmer
stemming = PorterStemmer()

# Creating a column tweet_stemmed to show the tweet's stemmed version
df['tweet_stemmed'] = df['tweet_token'].apply(lambda x: ' '.join([stemming.stem(i) for i in x]))
df.head()

"""### **Lemmatization** - It is the process of converting a word to its base form """

# Importing libraries for lemmatizing
from nltk.stem.wordnet import WordNetLemmatizer
lm = WordNetLemmatizer()

# Creating a column tweet_lemmatized to show the tweet's lemmatized version

def lemmatizer_on_text(data):
  text = [lm.lemmatize(word) for word in data]
  return data

df['tweet_lemmatized'] = df['tweet_stemmed'].apply(lambda x: lemmatizer_on_text(x))
df.head()

# drop all rows with any NaN and NaT values
df = df.dropna()
print(df)

"""### Text can now be analysed on the cleaned data

##### We will do our analysis on two columns i.e. 'tweet_stemmed' and 'tweet_lemmatized'

##### A - Will see the most commonly used words for both the above columns

#### Creating three different dfs for each company's positive word cloud
"""

maruti_df = df[df["companies"] == 'Maruti Suzuki']
maruti_pos_df = maruti_df[maruti_df['sentiment'] == 'Positive']
# Visualizing all the words in the column "tweet_stemmed" in our data belonging to Maruti Suzuki using the wordcloud

from wordcloud import WordCloud

all_words=' '.join([text for text in maruti_pos_df['tweet_stemmed']])

wordcloud = WordCloud(background_color ='white', width = 1000, height = 700, colormap = 'Set2', random_state= 21, max_font_size = 110).generate(all_words)

plt.figure(figsize=(10,7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.title("Most common positive words in the tweet_stemmed column for Maruti Suzuki")
plt.show()

# Visualising the word cloud for Tata Motors

Tata_df = df[df["companies"]=='Tata Motors']
tata_pos_df = Tata_df[Tata_df["sentiment"] == 'Positive']
all_words=' '.join([text for text in tata_pos_df['tweet_stemmed']])

wordcloud = WordCloud(background_color ='white', width = 1000, height = 700, colormap = 'Set2', random_state= 21, max_font_size = 110).generate(all_words)

plt.figure(figsize=(10,7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.title("Most common positive words in the tweet_stemmed column for Tata Motors")
plt.show()

# Visualising the word cloud for Mahindra & Mahindra

Mah_df = df[df["companies"]=='Mahindra & Mahindra']
Mah_pos_df = Mah_df[Mah_df["sentiment"] == 'Positive']
all_words=' '.join([text for text in Mah_pos_df['tweet_stemmed']])

wordcloud = WordCloud(background_color ='white', width = 1000, height = 700, colormap = 'Set2', random_state= 21, max_font_size = 110).generate(all_words)

plt.figure(figsize=(10,7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.title("Most common positive words in the tweet_stemmed column for Mahindra & Mahindra")
plt.show()

# Visualising the negative word cloud for each company

maruti_df = df[df["companies"] == 'Maruti Suzuki']
maruti_neg_df = maruti_df[maruti_df['sentiment'] == 'Negative']
# Visualizing all the words in the column "tweet_stemmed" in our data belonging to Maruti Suzuki using the wordcloud

from wordcloud import WordCloud

all_words=' '.join([text for text in maruti_neg_df['tweet_stemmed']])

wordcloud = WordCloud(background_color ='white', width = 1000, height = 700, colormap = 'Set2', random_state= 21, max_font_size = 110).generate(all_words)

plt.figure(figsize=(10,7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.title("Most common words negative words in the tweet_stemmed column for Maruti Suzuki")
plt.show()

# Visualising the negative word cloud for Tata Motors

tata_df = df[df["companies"] == 'Tata Motors']
tata_neg_df = tata_df[tata_df['sentiment'] == 'Negative']
# Visualizing all the words in the column "tweet_stemmed" in our data belonging to Maruti Suzuki using the wordcloud

from wordcloud import WordCloud

all_words=' '.join([text for text in tata_neg_df['tweet_stemmed']])

wordcloud = WordCloud(background_color ='white', width = 1000, height = 700, colormap = 'Set2', random_state= 21, max_font_size = 110).generate(all_words)


plt.figure(figsize=(10,7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.title("Most common words neagtive words in the tweet_stemmed column for Tata Motors")
plt.show()

# Visualising the negative word cloud for Mahindra & Mahindra

mah_df = df[df["companies"] == 'Mahindra & Mahindra']
mah_neg_df = mah_df[mah_df['sentiment'] == 'Negative']
# Visualizing all the words in the column "tweet_stemmed" in our data belonging to Maruti Suzuki using the wordcloud

from wordcloud import WordCloud

all_words=' '.join([text for text in mah_df['tweet_stemmed']])

wordcloud = WordCloud(background_color ='white', width = 1000, height = 700, colormap = 'Set2', random_state= 21, max_font_size = 110).generate(all_words)

plt.figure(figsize=(10,7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.title("Most common negative words in the tweet_stemmed column for Mahindra & Mahindra")
plt.show()

# Visualizing all the words in column "tweet_stemmed" in our data using the wordcloud plot

all_words = ' '.join([text for text in df['tweet_stemmed']])

from wordcloud import WordCloud

# generating a word cloud image
wordcloud = WordCloud(background_color ='#fcf2ed', width = 1000, height = 700, colormap = 'flag', random_state= 21, max_font_size = 110).generate(all_words)

plt.figure(figsize=(10,7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.title("Most common words in the tweet_stemmed column")
plt.show()

# Visualizing all the words in column "tweet_lemmatized" in our data using the wordcloud plot

all_words = ' '.join([text for text in df['tweet_lemmatized']])

# generating a word cloud image
wordcloud = WordCloud(background_color ='#fcf2ed', width = 1000, height = 700, colormap = 'flag', random_state= 21, max_font_size = 110).generate(all_words)

plt.figure(figsize=(10,7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.title("Most common words in the tweet_stemmed column")
plt.show()

"""## Extracting features from PreProcessed Tweets

#### Changing the labels into integers
"""

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
le.fit(df.sentiment)
df['target'] = le.transform(df.sentiment)

"""##### Selecting the text and target columns for further analysis

"""

X = df.tweet_stemmed
y = df.target

"""### Transforming dataset using Tf-Idf Vectorizer"""

#Importing Library

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=10000)

# Fit the TF-IDF Vectorizer

vectorizer.fit(X)

X_final = vectorizer.transform(X)

print('No. of feature_words: ', len(vectorizer.get_feature_names()))

# Transform the data using TF-IDF Vectorizer
#X_train = vectorizer.transform(X_train)
#X_test = vectorizer.transform(X_test)

"""### Splitting Data into train and test"""

# Splitting the data into training and validation set
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.25, random_state = 3)

"""## Twitter Sentiment Analysis"""

df.head()

"""### Function for Model Evaluation

###..

###After training the model we apply the following evaluation measures to check how the models are performing. Accordingly we use the following evaluation parameters to check the performance of the models respectively

#### 1) Accuracy Score
#### 2) Precision
#### 3) Recall
#### 4) Confusion Matrix

"""

def model_Evaluate(model):
# Predict values for Test dataset
 y_pred = model.predict(X_test)
# Print the evaluation metrics for the dataset
 print(classification_report(y_test, y_pred))
 accuracy = accuracy_score(y_test, y_pred)
 precision = precision_score(y_test, y_pred, average = 'macro')
 recall = recall_score(y_test, y_pred, average = 'macro')
 f1score = f1_score(y_test, y_pred, average ='macro')
 print('accuracy = %0.3f, precision = %0.3f, recall = %0.3f, f1_score = %0.3f' % (accuracy, precision, recall, f1score))
# Compute and plot the confusion matrix
 cf_matrix = confusion_matrix(y_test, y_pred)
 categories = ['Negative', 'Positive', 'Neutral']
 group_names = ['True Neg', 'False Pos', 'False Neg', 'True Pos']
 group_percentages = ['{0:2%}'.format(value) for value in cf_matrix.flatten() / np.sum(cf_matrix)]
 labels = [f'{v1}n{v2}' for v1, v2 in zip(group_names, group_percentages)]
 labels = np.asarray(labels).reshape(2,2)
 sns.heatmap(cf_matrix, annot = True, cmap = 'Blues', fmt = '',
             xticklabels = categories, yticklabels= categories)
 plt.xlabel("Predicted values", fontdict = {'size':14}, labelpad = 10)
 plt.ylabel("Actual values", fontdict = {'size':14}, labelpad = 10)
 confusion_mat = confusion_matrix(y_test, y_pred)

 #plt.title( "Confusion Matrix", fontdict = {'size': 18}, labelpad = 20)

"""## Bernoulli Naive Bayes"""

#Importing Library
from sklearn.naive_bayes import BernoulliNB

BNBmodel = BernoulliNB()
BNBmodel.fit(X_train, y_train)
model_Evaluate(BNBmodel)
#score_metrics(BNBmodel)
y_pred1 = BNBmodel.predict(X_test)

"""### Support Vector Machine (SVM)"""

# Importing Library
from sklearn.svm import LinearSVC

SVCmodel = LinearSVC()
SVCmodel.fit(X_train, y_train)
model_Evaluate(SVCmodel)
y_pred2 = SVCmodel.predict(X_test)

"""### Logistic Regression model """

#Importing Libraries
from sklearn.linear_model import LogisticRegression

LRmodel = LogisticRegression(C = 2, max_iter=1000, n_jobs=-1)
LRmodel.fit(X_train, y_train)
model_Evaluate(LRmodel)
y_pred3 = LRmodel.predict(X_test)

"""### K-Nearest Neighbours Classifier"""

#Importing Libraries

from sklearn.model_selection import RandomizedSearchCV
from sklearn.neighbors import KNeighborsClassifier

grid_params = {'n_neighbors' : [40,50,60,70,80,90],
               'metric' : ['manhattan']}

knn = KNeighborsClassifier()
clf = RandomizedSearchCV(knn, grid_params, random_state=0, n_jobs=-1, verbose=1)
clf.fit(X_train, y_train)

# Evaluation of the model

model_Evaluate(clf)
y_pred4 = clf.predict(X_test)

"""### Decision Trees"""

# Importing Libraries

from sklearn.tree import DecisionTreeClassifier

# Fitting the model
dt_classifier = DecisionTreeClassifier(criterion='entropy', random_state = 32)
dt_classifier.fit(X_train, y_train)

# Evaluating the model

model_Evaluate(dt_classifier)
y_pred5 = dt_classifier.predict(X_test)

"""### Random Forest"""

# Importing Libraries

from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, AdaBoostClassifier

# Fitting the model

rdt_classifier = RandomForestClassifier(n_estimators=10, criterion='entropy',
                                        n_jobs=-1, random_state=32)
rdt_classifier.fit(X_train, y_train)

# Evaluating the model

model_Evaluate(rdt_classifier)
y_pred6 = rdt_classifier.predict(X_test)

"""### We can see that the SVM Classifier gives the highest accuracy of 0.74 on our data

### Introducing Synthetic Minority Over-Sampling Technique (SMOTE)

#### Handling Imbalance
"""

from imblearn.over_sampling import SMOTE 
smote = SMOTE()
x_sm, y_sm = smote.fit_resample(X_final, y)

"""#### Splitting the data again with the transformed data"""

X_train, X_test, y_train, y_test = train_test_split(x_sm, y_sm, test_size=0.25, random_state=3)

"""#### Bernoulli Naive Bayes"""

# Fitting the model
BNBmodel = BernoulliNB()
BNBmodel.fit(X_train, y_train)
model_Evaluate(BNBmodel)

# Evaluating the model
y_pred1 = BNBmodel.predict(X_test)

"""#### Support Vector Machine"""

#Fitting the model

SVCmodel = LinearSVC()
SVCmodel.fit(X_train, y_train)
model_Evaluate(SVCmodel)
y_pred2 = SVCmodel.predict(X_test)

"""#### Logistic Regression"""

# Fitting the model

LRmodel = LogisticRegression(C = 2, max_iter=1000, n_jobs=-1)
LRmodel.fit(X_train, y_train)
model_Evaluate(LRmodel)
y_pred3 = LRmodel.predict(X_test)

"""#### K Nearest Neighbours"""

# Fitting the model

grid_params = {'n_neighbors' : [40,50,60,70,80,90],
               'metric' : ['manhattan']}

knn = KNeighborsClassifier()
clf = RandomizedSearchCV(knn, grid_params, random_state=0, n_jobs=-1, verbose=1)
clf.fit(X_train, y_train)

# Evaluation of the model

model_Evaluate(clf)
y_pred4 = clf.predict(X_test)

"""#### Decision Trees"""

# Fitting the model
dt_classifier = DecisionTreeClassifier(criterion='entropy', random_state = 32)
dt_classifier.fit(X_train, y_train)

# Evaluating the model

model_Evaluate(dt_classifier)
y_pred5 = dt_classifier.predict(X_test)

"""#### Random Forest"""

# Fitting the model
rdt_classifier = RandomForestClassifier(n_estimators=10, criterion='entropy',
                                        n_jobs=-1, random_state=32)
rdt_classifier.fit(X_train, y_train)

# Evaluating the model

model_Evaluate(rdt_classifier)
y_pred6 = rdt_classifier.predict(X_test)

"""We can see after applying SMOTE, the accuracy and f1 scores of all the classifiers except K Nearest Neighbours increase. The classifier with the highest accuracy and fi score is Naive Bayes Classifier.
*{the scores will be subject to change since they are sampled differently everytime the code runs, but the comparison will remain the same} 
"""

