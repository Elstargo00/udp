import os
import pandas as pd
from .. import db
import requests
from .dbs_handle import Numerical_record, League, Score

####### import for model part
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle
####### build ml model
# def logistic_regression():

#######



def absoluteFilePaths(directory):
  for dirpath, _, filenames in os.walk(directory):
    for filename in filenames:
      yield os.path.abspath(os.path.join(dirpath, filename))

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

proPlayer_list = setup_proPlayer_dict()
team_list = setup_team_dict()

### Extract information (team_id) from account id
def extract_team_id(account_id):
  for dic in proPlayer_list:
    if dic["account_id"] == account_id:
      return int(dic["team_id"])


### Extract information: win rate from team_id
def extract_team_winrate(team_id):
  for dic in team_list:
    if dic["team_id"] == team_id:
      return dic["wins"]/(dic["wins"]+dic["losses"])



def big_df_format():
  def check_team_id(id):
    team_id_list = big_df.loc[id,:].team_id.unique()
    if len(team_id_list) > 2:
      sort_count = big_df.loc[id,:].team_id.value_counts().sort_index(ascending = False)
      team_id_list = list()
      for indx in sort_count.index:
        if sort_count[indx] > 3:
          team_id_list.append(indx)
      if len(team_id_list) == 2:
        return team_id_list
      else:
        team_id_list = big_df.loc[id,:].team_id.unique()
        return team_id_list
    else:
      return team_id_list
  dat_path = '/Users/elstargo/Documents/allin/udp/datasets'
  files_list = [file for file in absoluteFilePaths(dat_path)]
  big_df = pd.concat([pd.read_csv(file) for file in files_list])
  big_df = big_df.reset_index(drop=True)
  proPlayer_list = setup_proPlayer_dict()
  big_df['team_id'] = big_df['account_id'].apply(extract_team_id)
  match_id_list = list(big_df.match_id.unique())
  start_time_list = list(big_df.start_time.unique())
  big_df.set_index(['match_id', 'start_time'], inplace=True)
  big_df = big_df.set_index(big_df.groupby(level=[0,1]).cumcount(), append=True)
  id = match_id_list[0]
  team_id_list = check_team_id(id)
  account_id_list = big_df.loc[id,:].account_id.unique()
  hero_id_list = big_df.loc[id,:].hero_id.unique()
  radiant_victory_list = big_df.loc[id,:].win.unique()
  data = {'match_id': [id],\
          'team_radiant_id': [team_id_list[0]],\
          'radiant|1': [(account_id_list[0],hero_id_list[0])],\
          'radiant|2': [(account_id_list[1],hero_id_list[1])],\
          'radiant|3': [(account_id_list[2],hero_id_list[2])],\
          'radiant|4': [(account_id_list[3],hero_id_list[3])],\
          'radiant|5': [(account_id_list[4],hero_id_list[4])],\
          'team_dire_id': [team_id_list[1]],\
          'dire|1': [(account_id_list[5],hero_id_list[5])],\
          'dire|2': [(account_id_list[6],hero_id_list[6])],\
          'dire|3': [(account_id_list[7],hero_id_list[7])],\
          'dire|4': [(account_id_list[8],hero_id_list[8])],\
          'dire|5': [(account_id_list[9],hero_id_list[9])],\
          'radiant_victory': [radiant_victory_list[0]]\
      }

  ref_df = pd.DataFrame(data, columns=['match_id','team_radiant_id','radiant|1','radiant|2','radiant|3','radiant|4','radiant|5',\
                                       'team_dire_id','dire|1','dire|2','dire|3','dire|4','dire|5','radiant_victory'])
  for id in match_id_list[1:]:
    team_id_list = check_team_id(id)
    account_id_list = big_df.loc[id,:].account_id.unique()
    hero_id_list = big_df.loc[id,:].hero_id.unique()
    team_dire_id_list = big_df.loc[id,:].team_id.unique()
    radiant_victory_list = big_df.loc[id,:].win.unique()
    
    data = {'match_id': id,\
            'team_radiant_id': team_id_list[0],\
            'radiant|1': (account_id_list[0],hero_id_list[0]),\
            'radiant|2': (account_id_list[1],hero_id_list[1]),\
            'radiant|3': (account_id_list[2],hero_id_list[2]),\
            'radiant|4': (account_id_list[3],hero_id_list[3]),\
            'radiant|5': (account_id_list[4],hero_id_list[4]),\
            'team_dire_id' : team_id_list[1],\
            'dire|1': (account_id_list[5],hero_id_list[5]),\
            'dire|2': (account_id_list[6],hero_id_list[6]),\
            'dire|3': (account_id_list[7],hero_id_list[7]),\
            'dire|4': (account_id_list[8],hero_id_list[8]),\
            'dire|5': (account_id_list[9],hero_id_list[9]),\
            'radiant_victory': radiant_victory_list[0]\
        }
    a_row = pd.Series(data)
    ref_df = ref_df.append(a_row, ignore_index=True)
  return ref_df

def live_df_format():
####### Get available live data
  live_url = 'https://api.opendota.com/api/live'
  unsort_live_response = requests.get(live_url, params='dictionary')
  unsort_live_list = unsort_live_response.json()
  pre_live_list = list()
  for dic in unsort_live_list:
    if dic['league_id'] != 0:
      pre_live_list.append(dic)
  live_list = list()
  for dic in pre_live_list:
    if len(dic['players'])==10:
      live_list.append(dic)
  ####### start filling the table
  match_id = live_list[0]['match_id']
  team_radiant_id = live_list[0]['team_id_radiant']
  team_dire_id = live_list[0]['team_id_dire']
  ####### sort team_id
  unsort_team_id = [live_list[0]['players'][i]['team_id'] for i in range(len(live_list[0]['players']))]
  sort_index_team_id_radiant = list()
  sort_index_team_id_dire = list()
  sort_index_team_id = list()
  for index, team_id in enumerate(unsort_team_id):
    if team_id == team_radiant_id:
      sort_index_team_id_radiant.append(index)
    elif team_id == team_dire_id:
      sort_index_team_id_dire.append(index)
    else:
      sort_index_team_id.append(index)
  if len(sort_index_team_id_radiant)==5 and len(sort_index_team_id_dire)==5:
    index_team_id = sort_index_team_id_radiant + sort_index_team_id_dire
  elif len(sort_index_team_id_radiant)<5 and len(sort_index_team_id_dire)==5:
    index_team_id = sort_index_team_id_radiant + sort_index_team_id + sort_index_team_id_dire
  elif len(sort_index_team_id_radiant)==5 and len(sort_index_team_id_dire)<5:
    index_team_id = sort_index_team_id_radiant + sort_index_team_id_dire + sort_index_team_id
  else:
    index_team_id = sort_index_team_id_radiant
    for index in sort_index_team: 
      if len(index_team_id)<5:
        index_team_id.append(index)
      elif len(index_team_id)<6+len(sort_index_team_id_dire):
        index_team_id.append(index)
      else:
        index_team_id += sort_index_team_id_dire
  ####### extract information
  account_id_list = [live_list[0]['players'][i]['account_id'] for i in index_team_id]
  hero_id_list = [live_list[0]['players'][i]['hero_id'] for i in index_team_id]
  data = {'match_id': [match_id],\
          'team_radiant_id': [team_radiant_id],\
          'radiant|1': [(account_id_list[0],hero_id_list[0])],\
          'radiant|2': [(account_id_list[1],hero_id_list[1])],\
          'radiant|3': [(account_id_list[2],hero_id_list[2])],\
          'radiant|4': [(account_id_list[3],hero_id_list[3])],\
          'radiant|5': [(account_id_list[4],hero_id_list[4])],\
          'team_dire_id': [team_dire_id],\
          'dire|1': [(account_id_list[5],hero_id_list[0])],\
          'dire|2': [(account_id_list[6],hero_id_list[1])],\
          'dire|3': [(account_id_list[7],hero_id_list[2])],\
          'dire|4': [(account_id_list[8],hero_id_list[3])],\
          'dire|5': [(account_id_list[9],hero_id_list[4])]\
        }

  live_df = pd.DataFrame(data, columns=['match_id','team_radiant_id','radiant|1','radiant|2','radiant|3','radiant|4',
                                  'radiant|5','team_dire_id','dire|1','dire|2','dire|3','dire|4','dire|5'])

  for live in live_list[1:]:
    ####### start filling the table
    match_id = live['match_id']
    team_radiant_id = live['team_id_radiant']
    team_dire_id = live['team_id_dire']
    ####### sort team_id
    unsort_team_id = [live['players'][i]['team_id'] for i in range(len(live['players']))]
    sort_index_team_id_radiant = list()
    sort_index_team_id_dire = list()
    sort_index_team_id = list()
    for index, team_id in enumerate(unsort_team_id):
      if team_id == team_radiant_id:
        sort_index_team_id_radiant.append(index)
      elif team_id == team_dire_id:
        sort_index_team_id_dire.append(index)
      else:
        sort_index_team_id.append(index)
    if len(sort_index_team_id_radiant)==5 and len(sort_index_team_id_dire)==5:
      index_team_id = sort_index_team_id_radiant + sort_index_team_id_dire
    elif len(sort_index_team_id_radiant)<5 and len(sort_index_team_id_dire)==5:
      index_team_id = sort_index_team_id_radiant + sort_index_team_id + sort_index_team_id_dire
    elif len(sort_index_team_id_radiant)==5 and len(sort_index_team_id_dire)<5:
      index_team_id = sort_index_team_id_radiant + sort_index_team_id_dire + sort_index_team_id
    else:
      index_team_id = sort_index_team_id_radiant
      for index in sort_index_team: 
        if len(index_team_id)<5:
          index_team_id.append(index)
        elif len(index_team_id)<6+len(sort_index_team_id_dire):
          index_team_id.append(index)
        else:
          index_team_id += sort_index_team_id_dire
    ####### extract information
    account_id_list = [live['players'][i]['account_id'] for i in index_team_id]
    hero_id_list = [live['players'][i]['hero_id'] for i in index_team_id]
    data = {'match_id': match_id,\
            'team_radiant_id': team_radiant_id,\
            'radiant|1': (account_id_list[0],hero_id_list[0]),\
            'radiant|2': (account_id_list[1],hero_id_list[1]),\
            'radiant|3': (account_id_list[2],hero_id_list[2]),\
            'radiant|4': (account_id_list[3],hero_id_list[3]),\
            'radiant|5': (account_id_list[4],hero_id_list[4]),\
            'team_dire_id' : team_dire_id,\
            'dire|1': (account_id_list[5],hero_id_list[5]),\
            'dire|2': (account_id_list[6],hero_id_list[6]),\
            'dire|3': (account_id_list[7],hero_id_list[7]),\
            'dire|4': (account_id_list[8],hero_id_list[8]),\
            'dire|5': (account_id_list[9],hero_id_list[9]),\
          }
    a_row = pd.Series(data)
    live_df = live_df.append(a_row, ignore_index=True)  
  return live_df


ref_df = big_df_format()
live_df = live_df_format()

###

def player_hero_dict_tonum(df):
  for i in range(len(df)):
    recorded_match_id = Numerical_record.query.filter_by(match_id=df.iloc[i]['match_id']).first()
    player_hero_key_list = list(df.iloc[i,2:7]) + list(df.iloc[i,8:13])
    player_hero_key_list = [str(int(element[0])) + '_' + str(int(element[1]))  for element in player_hero_key_list]
    if recorded_match_id is None:
      if df.iloc[i]['radiant_victory']:
        victory = True
        for element in player_hero_key_list[0:5]:
          recorded_player_hero = Score.query.filter_by(player_hero=element).first()
          if recorded_player_hero is None:
            score_in = Score(player_hero=element, success_score=1.0, exp=1.0)
            db.session.add(score_in)
            db.session.commit()
          else:
            recorded_player_hero.success_score+=1.0/recorded_player_hero.exp; recorded_player_hero.exp+=1.0
            db.session.commit()
        for element in player_hero_key_list[5:]:
          recorded_player_hero = Score.query.filter_by(player_hero=element).first()
          if recorded_player_hero is None:
            score_out = Score(player_hero=element, success_score=-1.0, exp=1.0)
            db.session.add(score_out)
            db.session.commit()
          else:
            recorded_player_hero.success_score-=1.0/recorded_player_hero.exp; recorded_player_hero.exp+=1.0
            db.session.commit()
      else:
        victory = False
        for element in player_hero_key_list[5:]:
          recorded_player_hero = Score.query.filter_by(player_hero=element).first()
          if recorded_player_hero is None:
            score_in = Score(player_hero=element, success_score=1.0, exp=1.0)
            db.session.add(score_in)
            db.session.commit()
          else:
            recorded_player_hero.success_score+=1.0/recorded_player_hero.exp; recorded_player_hero.exp+=1.0
            db.session.commit()
        for element in player_hero_key_list[0:5]:
          recorded_player_hero = Score.query.filter_by(player_hero=element).first()
          if recorded_player_hero is None:
            score_out = Score(player_hero=element, success_score=-1.0, exp=1.0)
            db.session.add(score_out)
            db.session.commit()
          else:
            recorded_player_hero.success_score-=1.0/recorded_player_hero.exp; recorded_player_hero.exp+=1.0
            db.session.commit()
    

    # add Numerical_record with the lastest updated dictionary (outside if statement: always updated)   
    team_radiant_winrate = extract_team_winrate(df.iloc[i]['team_radiant_id'])
    if team_radiant_winrate is None: team_radiant_winrate = 0
    team_dire_winrate = extract_team_winrate(df.iloc[i]['team_dire_id'])
    if team_dire_winrate is None: team_dire_winrate = 0
    player_hero_score_list = list()
    for a_player_hero in player_hero_key_list:
      player_hero_query = Score.query.filter_by(player_hero=a_player_hero).first()
      player_hero_score_list.append(player_hero_query.success_score)

    match_in = Numerical_record(match_id=df.iloc[i]['match_id'], team_radiant=team_radiant_winrate, radiant_1=player_hero_score_list[0],\
                                 radiant_2=player_hero_score_list[1], radiant_3=player_hero_score_list[2], radiant_4=player_hero_score_list[3],\
                                 radiant_5=player_hero_score_list[4], team_dire=team_dire_winrate, dire_1=player_hero_score_list[5],\
                                 dire_2=player_hero_score_list[6], dire_3=player_hero_score_list[7], dire_4=player_hero_score_list[8],\
                                 dire_5=player_hero_score_list[9], victory=victory)
    db.session.add(match_in)
    db.session.commit()

player_hero_dict_tonum(ref_df)


def nolabel_player_hero_dict_tonum(df):
  team_radiant_winrate = extract_team_winrate(df.iloc[0]['team_radiant_id'])
  if team_radiant_winrate is None: team_radiant_winrate = 0
  team_dire_winrate = extract_team_winrate(df.iloc[0]['team_dire_id'])
  if team_dire_winrate is None: team_dire_winrate = 0
  player_hero_key_list = list(df.iloc[0,2:7]) + list(df.iloc[0,8:13])
  player_hero_key_list = [str(int(element[0])) + '_' + str(int(element[1]))  for element in player_hero_key_list]
  player_hero_score_list = list()
  for a_player_hero in player_hero_key_list:
    player_hero_query = Score.query.filter_by(player_hero=a_player_hero).first()
    if player_hero_query is None:
      player_hero_score_list.append(1.0)
    else:
      player_hero_score_list.append(player_hero_query.success_score)

  data = {'team_radiant': team_radiant_winrate,\
          'radiant_1': player_hero_score_list[0],\
          'radiant_2': player_hero_score_list[1],\
          'radiant_3': player_hero_score_list[2],\
          'radiant_4': player_hero_score_list[3],\
          'radiant_5': player_hero_score_list[4],\
          'team_dire' : team_dire_winrate,\
          'dire_1': player_hero_score_list[5],\
          'dire_2': player_hero_score_list[6],\
          'dire_3': player_hero_score_list[7],\
          'dire_4': player_hero_score_list[8],\
          'dire_5': player_hero_score_list[9]\
        }

  live_num_df = pd.DataFrame(data, columns=['team_radiant','radiant_1','radiant_2','radiant_3','radiant_4',
                                    'radiant_5','team_dire','dire_1','dire_2','dire_3','dire_4','dire_5'],index=[0])
  for row in range(1,len(df)):
    print(row)
    team_radiant_winrate = extract_team_winrate(df.iloc[row]['team_radiant_id'])
    if team_radiant_winrate is None: team_radiant_winrate = 0
    team_dire_winrate = extract_team_winrate(df.iloc[row]['team_dire_id'])
    if team_dire_winrate is None: team_dire_winrate = 0
    player_hero_key_list = list(df.iloc[row,2:7]) + list(df.iloc[row,8:13])
    player_hero_key_list = [str(int(element[0])) + '_' + str(int(element[1]))  for element in player_hero_key_list]
    player_hero_score_list = list()
    for a_player_hero in player_hero_key_list:
      player_hero_query = Score.query.filter_by(player_hero=a_player_hero).first()
      if player_hero_query is None:
        player_hero_score_list.append(1.0)
      else:
        player_hero_score_list.append(player_hero_query.success_score)

    data = {'team_radiant': team_radiant_winrate,\
            'radiant_1': player_hero_score_list[0],\
            'radiant_2': player_hero_score_list[1],\
            'radiant_3': player_hero_score_list[2],\
            'radiant_4': player_hero_score_list[3],\
            'radiant_5': player_hero_score_list[4],\
            'team_dire' : team_dire_winrate,\
            'dire_1': player_hero_score_list[5],\
            'dire_2': player_hero_score_list[6],\
            'dire_3': player_hero_score_list[7],\
            'dire_4': player_hero_score_list[8],\
            'dire_5': player_hero_score_list[9]\
        }
    a_row = pd.Series(data)
    live_num_df = live_num_df.append(a_row, ignore_index=True)
  return live_num_df
    

live_num_df = nolabel_player_hero_dict_tonum(live_df)





