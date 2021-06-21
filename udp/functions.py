import os
import pandas as pd
from udp import db
import requests
import time
import datetime
import requests
import numpy as np
import random
import math
import json
from bs4 import BeautifulSoup


####### import -> model part ---
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
# try:
    # tensorflow_version 2.x
# except Exception:
    # pass
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras import layers
import bert 
import matplotlib.pyplot as plt
####### import -> model part ---


#######
def setup_proPlayer_dict():
    proPlayer_url = "https://api.opendota.com/api/proPlayers"
    proPlayer_response = requests.get(proPlayer_url, params='dictionary')
    proPlayer_list = proPlayer_response.json()
    key_proPlayer_list = list(proPlayer_list[0].keys())
    key_proPlayer_list = key_proPlayer_list[1:14] + [key_proPlayer_list[15]] + key_proPlayer_list[19:23]
    for dic in proPlayer_list:
        for j in key_proPlayer_list:
            del dic[j]
    return proPlayer_list

def setup_team_dict():
    team_url = "https://api.opendota.com/api/teams"
    team_response = requests.get(team_url, params='dictionary')
    team_list = team_response.json()
    key_team_list = list(team_list[0].keys())
    key_team_list = [key_team_list[1]] + key_team_list[4:]
    for dic in team_list:
        for j in key_team_list:
            del dic[j]
    return team_list

def absoluteFilePaths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            yield os.path.abspath(os.path.join(dirpath, filename))

def extract_team_id(account_id):
    for dic in proPlayer_list:
        if dic["account_id"] == account_id:
            return int(dic["team_id"])

def fill_big_df(df):
    df['team_id'] = df['account_id'].apply(extract_team_id)

def check_team_id(id):
    def clear_zero(sort_count):
        return sort_count.drop(0.0)
    def team_append(sort_count):
        team_id_list = list()
        team_id_list.append(sort_count.index[0])
        team_id_list.append(sort_count.index[1])
        return team_id_list
    def clear_n_smallest(sort_count,n):
        for _ in range(n):
            sort_count = sort_count.drop(sort_count.nsmallest(n).index[0])
        return sort_count
    team_id_list = list()
    sort_count = big_df.loc[id,:].team_id.value_counts()[big_df.loc[id,:].team_id.unique()]
    if len(sort_count)<2:
        team_id_list.append(sort_count.index[0])
        team_id_list.append(sort_count.index[0])
    elif len(sort_count)==2:
        team_id_list = team_append(sort_count)
    else:
        if 0.0 in sort_count.index:
            sort_count = clear_zero(sort_count)
            sort_count = clear_n_smallest(sort_count,len(sort_count)-2)
            team_id_list = team_append(sort_count)
        else:
            sort_count = clear_n_smallest(sort_count,len(sort_count)-2)
            team_id_list = team_append(sort_count)
    return team_id_list

def initiate_df(columns, data):
    data = dict(zip(columns,data))
    ref_df = pd.DataFrame(data=data, columns=columns, index=[0])
    return ref_df

def appendto_df(ref_df, columns, data):
    data = dict(zip(columns,data))
    a_row = pd.Series(data)
    ref_df = ref_df.append(a_row, ignore_index=True)
    return ref_df

# we won't use this function ---
def big_df_format():
    proPlayer_list = setup_proPlayer_dict()
    team_list = setup_team_dict()
    dat_path = '/Users/elstargo/Documents/allin/udp/datasets'
    files_list = [file for file in absoluteFilePaths(dat_path)]
    big_df = pd.concat([pd.read_csv(file) for file in files_list])
    big_df = big_df.reset_index(drop=True)
    fill_big_df(big_df)
    match_id_list = list(big_df.match_id.unique())
    start_time_list = list(big_df.start_time.unique())
    big_df.set_index(['match_id', 'start_time'], inplace=True)
    big_df = big_df.set_index(big_df.groupby(level=[0,1]).cumcount(), append=True)
    big_df['team_id'] = np.nan_to_num(big_df['team_id']).astype(int)
    id = match_id_list[0]
    team_id_list = check_team_id(id)
    account_id_list = big_df.loc[id,:].account_id.unique()
    hero_id_list = big_df.loc[id,:].hero_id.unique()
    radiant_victory_list = big_df.loc[id,:].win.unique()
    columns = ['match_id', 'team_radiant_id', 'radiant|1', 'radiant|2', 'radiant|3',
               'radiant|4', 'radiant|5', 'team_dire_id', 'dire|1', 'dire|2',
               'dire|3', 'dire|4', 'dire|5', 'radiant_victory']
    data = [id, team_id_list[0], [(account_id_list[0],hero_id_list[0])], [(account_id_list[1],hero_id_list[1])],
           [(account_id_list[2],hero_id_list[2])], [(account_id_list[3],hero_id_list[3])],
           [(account_id_list[4],hero_id_list[4])], team_id_list[1], [(account_id_list[5],hero_id_list[5])],
           [(account_id_list[6],hero_id_list[6])], [(account_id_list[7],hero_id_list[7])],
           [(account_id_list[8],hero_id_list[8])], [(account_id_list[9],hero_id_list[9])], radiant_victory_list[0]]
    ref_df = initiate_df(columns, data)
    for id in match_id_list[1:]:
        team_id_list = check_team_id(id)
        account_id_list = big_df.loc[id,:].account_id.unique()
        hero_id_list = big_df.loc[id,:].hero_id.unique()
        radiant_victory_list = big_df.loc[id,:].win.unique()
        columns = ['match_id', 'team_radiant_id', 'radiant|1', 'radiant|2', 'radiant|3',
                   'radiant|4', 'radiant|5', 'team_dire_id', 'dire|1', 'dire|2',
                   'dire|3', 'dire|4', 'dire|5', 'radiant_victory']
        data = [id, team_id_list[0], (account_id_list[0],hero_id_list[0]), (account_id_list[1],hero_id_list[1]),
                (account_id_list[2],hero_id_list[2]), (account_id_list[3],hero_id_list[3]),
                (account_id_list[4],hero_id_list[4]), team_id_list[1], (account_id_list[5],hero_id_list[5]),
                (account_id_list[6],hero_id_list[6]), (account_id_list[7],hero_id_list[7]),
                (account_id_list[8],hero_id_list[8]), (account_id_list[9],hero_id_list[9]),
                radiant_victory_list[0]]
        ref_df = appendto_df(ref_df, columns, data)
    return ref_df
# we won't use this function ---

def get_rightlive(unsort_live_list):
    live_list = list()
    for dic in unsort_live_list:
        if dic['league_id']!=0 and len(dic['players'])==10:
            catch_team_id = [dic['players'][i].get('team_id','not found') for i in range(10)]
            if not 'not found' in catch_team_id:
                live_list.append(dic)
    return live_list

# create function for sorting account id list
def sort_player_hero(account_list, hero_list, id_radiant):
    account_id_list = list()
    account_radiant = list()
    account_dire = list()
    hero_id_list = list()
    hero_radiant = list()
    hero_dire = list()
    for i in range(len(account_list)):
        if extract_team_id(account_list[i])==id_radiant:
            account_radiant.append(account_list[i])
            hero_radiant.append(hero_list[i])
        else:
            account_dire.append(account_list[i])
            hero_dire.append(hero_list[i])
    account_id_list = account_radiant + account_dire
    hero_id_list = hero_radiant + hero_dire
    return account_id_list, hero_id_list


def live_df_format():
    live_url = 'https://api.opendota.com/api/live'
    unsort_live_response = requests.get(live_url, params='dictionary')
    unsort_live_list = unsort_live_response.json()
    live_list = get_rightlive(unsort_live_list)
    try:
        unsort_team_id = [live_list[0]['players'][i]['team_id'] for i in range(len(live_list[0]['players']))]
    except IndexError:
        pass
    try:
        match_id = live_list[3]['match_id']
        team_id_radiant = live_list[3]['team_id_radiant']
        team_id_dire = live_list[3]['team_id_dire']
        account_id_list = [live_list[3]['players'][i]['account_id'] for i in range(10)]
        hero_id_list = [live_list[3]['players'][i]['hero_id'] for i in range(10)]
        account_id_list, hero_id_list = sort_player_hero(account_id_list, hero_id_list, team_id_radiant)
    except IndexError:
        pass
    # initiate dataframe
    try:
        match_id = live_list[0]['match_id']
        team_id_radiant = live_list[0]['team_id_radiant']
        team_id_dire = live_list[0]['team_id_dire']
        account_id_list = [live_list[0]['players'][i]['account_id'] for i in range(10)]
        hero_id_list = [live_list[0]['players'][i]['hero_id'] for i in range(10)]
        account_id_list, hero_id_list = sort_player_hero(account_id_list, hero_id_list, team_id_radiant)

        live_columns = ['match_id', 'team_radiant_id', 'radiant|1', 'radiant|2', 'radiant|3',
                        'radiant|4', 'radiant|5', 'team_dire_id', 'dire|1', 'dire|2',
                        'dire|3', 'dire|4', 'dire|5']
        live_data = [match_id, team_id_radiant, [(account_id_list[0],hero_id_list[0])], [(account_id_list[1],hero_id_list[1])],
                [(account_id_list[2],hero_id_list[2])], [(account_id_list[3],hero_id_list[3])],
                [(account_id_list[4],hero_id_list[4])], team_id_dire, [(account_id_list[5],hero_id_list[5])],
                [(account_id_list[6],hero_id_list[6])], [(account_id_list[7],hero_id_list[7])],
                [(account_id_list[8],hero_id_list[8])], [(account_id_list[9],hero_id_list[9])]]
    except IndexError:
        pass
    try:
        live_df = initiate_df(live_columns, live_data)
    except NameError:
        pass
    # add data row to dataframe
    for i in range(1,len(live_list)):
        match_id = live_list[i]['match_id']
        team_id_radiant = live_list[i]['team_id_radiant']
        team_id_dire = live_list[i]['team_id_dire']
        account_id_list = [live_list[i]['players'][j]['account_id'] for j in range(10)]
        hero_id_list = [live_list[i]['players'][j]['hero_id'] for j in range(10)]
        account_id_list, hero_id_list = sort_player_hero(account_id_list, hero_id_list, team_id_radiant)

        live_columns = ['match_id', 'team_radiant_id', 'radiant|1', 'radiant|2', 'radiant|3',
                    'radiant|4', 'radiant|5', 'team_dire_id', 'dire|1', 'dire|2',
                    'dire|3', 'dire|4', 'dire|5']
        live_data = [match_id, team_id_radiant, (account_id_list[0],hero_id_list[0]), (account_id_list[1],hero_id_list[1]),
                (account_id_list[2],hero_id_list[2]), (account_id_list[3],hero_id_list[3]),
                (account_id_list[4],hero_id_list[4]), team_id_dire, (account_id_list[5],hero_id_list[5]),
                (account_id_list[6],hero_id_list[6]), (account_id_list[7],hero_id_list[7]),
                (account_id_list[8],hero_id_list[8]), (account_id_list[9],hero_id_list[9])]

        live_df = appendto_df(live_df, live_columns, live_data)
    try:
        if not live_df.empty:
            return live_df
        else:
            return 'No live match available'
    except NameError:
        pass


# model loading

# define deep convolutional neural network


class DCNN(tf.keras.Model):

    def __init__(self, vocab_size, emb_dim=128, nb_filters=50, FFN_units=512, nb_classes=2, dropout_rate=0.1,
                training=False, name='dcnn'):    
        super(DCNN, self).__init__(name=name)
        
        self.embedding = layers.Embedding(vocab_size+1, emb_dim)
        self.bigram = layers.Conv1D(filters=nb_filters, kernel_size=2, padding="valid", activation="relu")
        self.trigram = layers.Conv1D(filters=nb_filters, kernel_size=3, padding="valid", activation="relu")
        self.fourgram = layers.Conv1D(filters=nb_filters, kernel_size=4, padding="valid", activation="relu")
        self.pool = layers.GlobalMaxPooling1D()
        self.dense_1 = layers.Dense(units=FFN_units, activation="relu")
        self.dropout = layers.Dropout(rate=dropout_rate)
        if nb_classes == 2:
            self.last_dense = layers.Dense(units=1, activation="sigmoid")
        else:
            self.last_dense = layers.Dense(units=nb_classes, activation="softmax")
            
    def call(self, inputs, training):
        x = self.embedding(inputs)
        x_1 = self.bigram(x)
        x_1 = self.pool(x_1)
        x_2 = self.trigram(x)
        x_2 = self.pool(x_2)
        x_3 = self.fourgram(x)
        x_3 = self.pool(x_3)    # (batch_size, nb_filters)
        merged = tf.concat([x_1, x_2, x_3], axis=-1) # (batch_size, 3*nb_filters)
        merged = self.dense_1(merged)
        merged = self.dropout(merged, training)
        output = self.last_dense(merged)
        return output
    
def encode_sentence(sent):
    return match_tokenizer.texts_to_sequences(list([sent]))[0]


# new get_prediction
def get_prediction(sent, team_id):
    # Decorator
    team_decorator = dict_team_decorator()
    match_btw = list()
    match_btw.append( team_decorator[team_id[0]] ) 
    match_btw.append( team_decorator[team_id[1]] )
    # # # # # #
    match_tokens = encode_sentence(sent)
    match_inputs = tf.expand_dims(match_tokens, 0)
    match_output = Dcnn(match_inputs, training=False)
    match_sentiment = math.floor(match_output*2)
    if match_sentiment == 0:
        # print('Output of the model: {}\nPredicted sentiment: Dire Victory.'.format(1-match_output))
        result = '{} Victory'.format(match_btw[1])
    elif match_sentiment == 1:
        # print('Output of the model: {}]\nPredicted sentiment: Radiant Victory.'.format(match_output))
        result = '{} Victory'.format(match_btw[0])
    else:
        print('nothing happen?')
    return result
        
        
# # # # # # # Decorator Zone # # # # # # #
def dict_team_decorator():
    team_url = "https://api.opendota.com/api/teams"
    team_response = requests.get(team_url, params='dictionary')
    team_list = team_response.json()
    key_team_list = list(team_list[0].keys())
    key_team_list = key_team_list[6:8] + key_team_list[1:5]
    for dic in team_list:
        for j in key_team_list:
            del dic[j]
    team_decorator = dict()
    for j in range(len(team_list)):
        key, value = team_list[j].values()
        team_decorator[key] = value
    return team_decorator
# # # # # # # # # # # # # # # # # # # # # #
    
def predict_ckpnt_model(match_sentence, match_btw):
    # recieve only one row of input
    with open('/Users/elstargo/Documents/allin/udp/json_tokenizer/json_tokenizer.txt') as json_file:
        json_tokenizer = json.load(json_file)
    
    match_tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(json_tokenizer)
    # setup arguments for the model parameter
    VOCAB_SIZE = len(match_tokenizer.word_index)
    EMB_DIM = 200
    NB_FILTERS = 100
    FFN_UNITS = 256
    NB_CLASSES = 2 
    DROPOUT_RATE = 0.2
    NB_EPOCHS = 10
    # # # # # # # # # # # #
    # set hyperparameter to the model
    Dcnn = DCNN(vocab_size=VOCAB_SIZE, emb_dim=EMB_DIM, nb_filters=NB_FILTERS,
                FFN_units=FFN_UNITS, nb_classes=NB_CLASSES, dropout_rate=DROPOUT_RATE)
    if NB_CLASSES == 2:
        Dcnn.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    else:
        Dcnn.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['sparse_categorial_accuracy'])
    
    # run this to restore the lastest checkpoint
    checkpoint_path = '/Users/elstargo/Documents/allin/udp/ckpnt_bert'
    ckpt = tf.train.Checkpoint(Dcnn=Dcnn)
    ckpt_manager = tf.train.CheckpointManager(ckpt, checkpoint_path, max_to_keep=1)
    if ckpt_manager.latest_checkpoint:
        ckpt.restore(ckpt_manager.latest_checkpoint) # Lastest checkpoint restored!
    return get_prediction(match_sentence, match_btw)




