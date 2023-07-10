import os
import pandas as pd
from flask import request, jsonify
import string
import re
import sqlite3
from database import create_database_file


# pandas dataframe untuk kamusalay
temp_kamusalay = pd.read_csv('data/new_kamusalay.csv',
                           encoding='latin-1', names=['find', 'replace'])
# Mapping data untuk kamusalay
kamusalay_map = dict(zip(temp_kamusalay['find'], temp_kamusalay['replace']))


# pandas dataframe untuk kamusabusive
temp_kamusabusive = pd.read_csv('data/abusive.csv',
                              encoding='latin-1',
                              names=['find', 'replace'],
                              skiprows=1)

# Mapping data untuk kamusabusive
kamusabusive_map = dict(zip(temp_kamusabusive['find'], ['' for _ in temp_kamusabusive['find']]))
def text_processing_file():
    file = request.files.getlist('file')[0]
    df = pd.read_csv(file, sep=",", encoding="latin-1")

    assert any(df.columns == 'Tweet')

    df = apply_cleansing_file(df)

    texts = df.Tweet.to_list()

    cleaned_text = []
    for text in texts:
        cleaned_text.append(text)

    json_response = {
        'status_code': 200,
        'description': "Teks yang telah diproses",
        'data': cleaned_text
    }

    create_database_file(cleaned_text)

    # membuat response JSON
    response = jsonify(json_response)
    return response


def apply_cleansing_file(data):
    # menghapus duplikasi data
    data = data.drop_duplicates()
    # merubah menjadi huruf non capital
    data['text_lower'] = data['Tweet'].apply(lambda x: text_lower(x))
    # drop kolom tweet
    data.drop(['Tweet'], axis=1, inplace=True)
    # implement menghapus_unnecessary_char method dengan menggunakan regex
    data['text_clean'] = data['text_lower'].apply(
        lambda x: remove_unnecessary_char(x))
    # apply kamusalay method
    data['Tweet'] = data['text_clean'].apply(lambda x: handler_kamusalay(x))
    # apply kamusabusive method
    data['Tweet'] = data['text_clean'].apply(lambda x: handler_kamusabusive(x))
    # drop text clean column
    data.drop(['text_lower', 'text_clean'], axis=1, inplace=True)

    return data


def text_lower(text):
    text = text.lower()
    return text


def remove_unnecessary_char(text):
    text = re.sub(r'[^a-z ]', ' ', text)
    text = re.sub(r'  +', ' ', text)
    text = re.sub(r'\\+n', ' ', text)
    text = re.sub(r'\n', " ", text)
    text = re.sub(r'(rt)', ' ', text)
    text = re.sub(r'\\x.{2}', ' ', text)
    text = re.sub('user', ' ', text)
    text = re.sub(r'&amp;', 'dan', text)
    text = re.sub(r'&', 'dan', text)
    text = re.sub(r'\+62\d{2,}', ' ', text)
    text = re.sub('[\+\d{5}\-\d{4}\-\d{4}]', ' ', text)
    text = text.rstrip().lstrip()

    return text


def handler_kamusalay(text):
    wordlist = text.split()
    data = ' '.join([kamusalay_map.get(x, x) for x in wordlist])
    return data


def handler_kamusabusive(text):
    wordlist = text.split()
    data = ' '.join([kamusabusive_map.get(x, x) for x in wordlist])
    return data


    df.to_sql('tweet',
              con=conn,
              if_exists='append',
              index=False
              )