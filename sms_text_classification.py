import tensorflow as tf
import pandas as pd
!pip install tensorflow-datasets
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

print(tf.__version__)
# get data files
!wget https://cdn.freecodecamp.org/project-data/sms/train-data.tsv
!wget https://cdn.freecodecamp.org/project-data/sms/valid-data.tsv

#Without specifying sep="\t", pandas would incorrectly assume a comma delimiter.
#If header=None were omitted, pandas would incorrectly treat the first row as the header (column name)
#To make the data easier to work with and more readable, we provide meaningful names (label and message) for the columns.
train_dataset = pd.read_csv("train-data.tsv", sep='\t', header=None, names=['label','message'])
test_dataset = pd.read_csv("valid-data.tsv", sep='\t', header=None, names=['label','message'])

vectorizer = TfidfVectorizer()

#vectorizing mssgs using TF-IDF (text vectorization technique.Measures how unique or rare a word is across all documents. Common words like "the", "is", or "and" will have a low IDF score, while rare or important words will have a high IDF score.)
train_vectors = vectorizer.fit_transform(train_dataset['message'])
test_vectors = vectorizer.transform(test_dataset['message'])

#Logistic Regression is a ml algorithm for classification problems. It predicts probabilities and maps them to classes (e.g., spam or ham).
#create the model
model = LogisticRegression()

#train the model
model.fit(train_vectors, train_dataset['label'])

# function to predict messages based on model
# (should return list containing prediction and label, ex. [0.008318834938108921, 'ham'])
def predict_message(pred_text):
  pred_vector = vectorizer.transform([pred_text])

  #model.predict would return 'ham'/'spam' but we need probabilities
  #The predict_proba() method of LogisticRegression returns the probabilities for each class (e.g., "ham" and "spam") as list of lists [[p(ham), P(spam)], [P(ham),...]...] so [0] to access the first raw (1 message) and [1] to accces the prob of spam
  prediction_proba = model.predict_proba(pred_vector)[0][1]

  prediction_label = "spam" if prediction_proba>0.5 else "ham"
  return [float(prediction_proba), prediction_label]

pred_text = "how are you doing today?"

prediction = predict_message(pred_text)
print(prediction)

# Run this cell to test your function and model. Do not modify contents.
def test_predictions():
  test_messages = ["how are you doing today",
                   "sale today! to stop texts call 98912460324",
                   "i dont want to go. can we try it a different day? available sat",
                   "our new mobile video service is live. just install on your phone to start watching.",
                   "you have won £1000 cash! call to claim your prize.",
                   "i'll bring it tomorrow. don't forget the milk.",
                   "wow, is your arm alright. that happened to me one time too"
                  ]

  test_answers = ["ham", "spam", "ham", "spam", "spam", "ham", "ham"]
  passed = True

  for msg, ans in zip(test_messages, test_answers):
    prediction = predict_message(msg)
    if prediction[1] != ans:
      passed = False

  if passed:
    print("You passed the challenge. Great job!")
  else:
    print("You haven't passed yet. Keep trying.")

test_predictions()
