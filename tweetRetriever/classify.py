import os
import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report


def generate_model(path_to_dataset):
    print("Importing dataset.csv")
    df = pd.read_csv(path_to_dataset, encoding='UTF-8')

    # remove columns: 'id' and 'Keyword'
    df = df.drop(['id', 'Keyword'], axis=1)
    print(df['Target'].value_counts())  # this should give us 667 negatives and 328 positives

    # Balancing the dataset by undersampling the negative class
    df_0_class = df[df['Target']==0]
    df_1_class = df[df['Target']==1]
    df_0_class_undersampled = df_0_class.sample(df_1_class.shape[0])
    df = pd.concat([df_0_class_undersampled, df_1_class], axis=0)

    print("Preparing dataset and BERT Model")
    # Splitting the dataset
    X_train, X_test, y_train, y_test = train_test_split(df['Tweet'], df['Target'], stratify=df['Target'])

    # Using BERT Model (Preprocessor & Encoder)
    preprocesser = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3")
    encoder = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4")

    text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text-layer')
    preprocessed_text = preprocesser(text_input)
    outputs = encoder(preprocessed_text)
    d_layer = tf.keras.layers.Dropout(0.1, name="dropout-layer")(outputs['pooled_output'])
    d_layer = tf.keras.layers.Dense(1, activation='sigmoid', name="output")(d_layer)
    model = tf.keras.Model(inputs=[text_input], outputs = [d_layer])
    print(model.summary())

    m= [
      tf.keras.metrics.BinaryAccuracy(name='accuracy'),
      tf.keras.metrics.Precision(name='precision'),
      tf.keras.metrics.Recall(name='recall')
    ]
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=m)

    print("Training model")
    # Model Training and Evaluation
    model.fit(X_train, y_train, epochs=10)
    model.evaluate(X_test, y_test)
    model.save('./trained_model.h5')

    y_predicted = model.predict(X_test)
    y_predicted = y_predicted.flatten()
    y_predicted = np.where(y_predicted > 0.5, 1, 0)
    matrix = confusion_matrix(y_test, y_predicted)
    print(matrix)
    print(classification_report(y_test, y_predicted))


def classify_tweet(trained_model, tweets):
    tweets_predicted = trained_model.predict(tweets)  # returns an array containing the probability of tweet being fitness-related e.g. [[0.6], [0.4], [0.7]]
    print(tweets_predicted)
    return np.where(tweets_predicted > 0.55, 1, 0)  # returns an array containing the predictions e.g. [[1], [0], [1]]


def calculate_fitness(trained_model, tweets):
    pred_array = classify_tweet(trained_model, tweets)
    num_of_pred = len(pred_array)
    positive_pred = 0
    for pred in pred_array:
        if pred[0] == 1:
            positive_pred += 1
    return positive_pred/num_of_pred


if __name__ == '__main__':
    if not os.path.exists('./trained_model.h5'):
        generate_model('./dataset.csv')
    else:
        print("Model already trained.")

    with tf.device('/cpu:0'):
        model = tf.keras.models.load_model('./trained_model.h5', custom_objects={'KerasLayer':hub.KerasLayer})
    sporty_test_sent = [
        "How the humble Exercise / Swiss Ball can be an older adult's ideal fitness companion",
        "How seniors and older adults can benefit from a structured and supervised home fitness program",
        "Why it makes more sense to workout with a partner or your significant other in your senior/older adult years:",
        "I'm glad that he can start swim lessons soon.",
        "The poor boy has been asking, \"When am I going to swim class mama?\"",
        "And he keeps insisting to go inside the swim school every time we sent his sister for class.",
        "I have been a runner over the past 12 years of my life. Running had brought me so much pain, tears, and joy. Here are some of the things that I had learned through the journey.",
        "Ended the month with an easy 6km after an enjoyable weekend with friends. Disappointed with the volume of this short month but time to sort myself out and get the machine running for March.",
        "Would say that this month was evenly spread out in terms of mileage. Did some harder workouts, swam more and also ran more with friends ",
        "Friends Who Sweat Together, Stay Together. Make Fitness Your Lifestyle!"
    ]
    non_sporty_test_sent = [
        "Happy New Year! May Joy, Peace, Good Health & Success be with each and every one of you! Best wishes from",
        "I think this would be good for our community cats too but then again, we have assholes who don't like that we have nice things for non-humans.",
        "being told from birth to never pursue the arts lmao",
        "My kind of flight",
        "Achievement unlocked! Within the 9 days, we had completed 418.52 of 100 km, raised S$1938 so far.",
        "Let's welcome the year of Tiger with fun and joy! Wishing you all good health and prosperity in the upcoming year! ",
        "And we're bringing public sector innovations along.",
        "I stepped away from music quite a while ago, for a number of reasons, but I still really love it, so the kindness and support I’ve received the past few days just for a little tiny toe dip back into some music means the absolute world to me",
        "This is clearly something I would not have done a year ago but time to muster the courage to choose the tougher but more meaningful route",
        "I used to think people are weird for liking things that does not fit the social norm but I am beginning to change this perception. It might actually be cool."
    ]
    prediction_array = classify_tweet(model, non_sporty_test_sent)
    print(prediction_array)
    #print(calculate_fitness(prediction_array))
