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


def classify_tweet(model, tweets):
    tweets_predicted = model.predict(tweets)  # returns an array containing the probability of tweet being fitness-related e.g. [[0.6], [0.4], [0.7]]
    print(tweets_predicted)
    return np.where(tweets_predicted > 0.55, 1, 0)  # returns an array containing the predictions e.g. [[1], [0], [1]]


def calculate_fitness(prediction_array):
    num_of_pred = len(prediction_array)
    positive_pred = 0
    for pred in prediction_array:
        if pred[0] == 1:
            positive_pred += 1
    return positive_pred/num_of_pred


if __name__ == '__main__':
    if not os.path.exists('./trained_model.h5'):
        generate_model('./dataset.csv')
    else:
        print("Model already trained.")
    
    model = tf.keras.models.load_model('./trained_model.h5', custom_objects={'KerasLayer':hub.KerasLayer})
    prediction_array = classify_tweet(model, ["What a great workout!", "This assignment is so difficult..."])
    print(calculate_fitness(prediction_array))
