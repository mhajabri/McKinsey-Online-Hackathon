# -*- coding: utf-8 -*-
"""

@author: Mhamed
"""

import numpy as np
import pandas as pd

""" 
Implementation of target mean encoding. This is not specific to this competition and can be used 
whenever you're dealing with categorical features.
"""

def add_noise(series, noise_level):
    return series * (1 + noise_level * np.random.randn(len(series)))

def target_encode(trn_series=None, 
                  tst_series=None, 
                  target=None, 
                  min_samples_leaf=1, 
                  smoothing=1,
                  noise_level=0):

    assert len(trn_series) == len(target)
    assert trn_series.name == tst_series.name
    temp = pd.concat([trn_series, target], axis=1)
    # Compute target mean 
    averages = temp.groupby(by=trn_series.name)[target.name].agg(["mean", "count"])
    # Compute smoothing
    smoothing = 1 / (1 + np.exp(-(averages["count"] - min_samples_leaf) / smoothing))
    # Apply average function to all target data
    prior = target.mean()
    # The bigger the count the less full_avg is taken into account
    averages[target.name] = prior * (1 - smoothing) + averages["mean"] * smoothing
    averages.drop(["mean", "count"], axis=1, inplace=True)
    # Apply averages to trn and tst series
    ft_trn_series = pd.merge(
        trn_series.to_frame(trn_series.name),
        averages.reset_index().rename(columns={'index': target.name, target.name: 'average'}),
        on=trn_series.name,
        how='left')['average'].rename(trn_series.name + '_mean').fillna(prior)
    # pd.merge does not keep the index so restore it
    ft_trn_series.index = trn_series.index 
    ft_tst_series = pd.merge(
        tst_series.to_frame(tst_series.name),
        averages.reset_index().rename(columns={'index': target.name, target.name: 'average'}),
        on=tst_series.name,
        how='left')['average'].rename(trn_series.name + '_mean').fillna(prior)
    # pd.merge does not keep the index so restore it
    ft_tst_series.index = tst_series.index
    return add_noise(ft_trn_series, noise_level), add_noise(ft_tst_series, noise_level)


"""
Building new features from the ones we have in our training set
""" 

def get_age_years(series):
    return round(series/365)

def get_ratio_late(dataframe) :  
    col_list= list(dataframe)
    col_list.remove('no_of_premiums_paid')
    dataframe['late'] = dataframe[col_list].sum(axis=1).div(dataframe["no_of_premiums_paid"], axis=0)
    return dataframe['late']

def get_estimate_loyalty(df):
    return df.no_of_premiums_paid / (df.age_in_years - 20)

def get_ratio_to_income(df) :
    return df.premium / df.Income

def get_bins_income(df) :
    return pd.cut(df['Income'], bins = [0, 110000, 200000, 9999999999], labels=[1, 2, 3])

def get_bins_score(df) :
    return pd.cut(df['application_underwriting_score'], bins = [0,90,95,98,99, 100], labels=[0, 1,2,3,4])

def get_bins_age(df) :
    return pd.cut(df['age_in_years'], bins = [20,40,55,100], labels=[1,2,3])

def get_efficient_income(df):
    return df['application_underwriting_score']*(df['Income']-df['premium'])/100

def replace_string(df) : 
    try : 
        df.replace({'residence_area_type':{'Urban':1, 'Rural':0}, 'sourcing_channel':{'A':1, 'B':2, 'C':3, 'D':4, 'E':5}},inplace=True)
    except :
        print('already done')
        
def get_new_score(df) :
    return df['application_underwriting_score']*df['premium_to_income']/(df['ratio_late']+1)

def get_new_score2(df) :
    return df['perc_premium_paid_by_cash_credit']*df['Income']
################################################################################################################################## 

def add_features(train, test) :
    train['age_in_years'] = get_age_years(train['age_in_days'])
    test['age_in_years'] = get_age_years(test['age_in_days'])
    train['ratio_late'] = get_ratio_late(train[['Count_3-6_months_late','Count_6-12_months_late','Count_more_than_12_months_late','no_of_premiums_paid']])
    test['ratio_late'] =get_ratio_late(test[['Count_3-6_months_late','Count_6-12_months_late','Count_more_than_12_months_late','no_of_premiums_paid']])
    train['estimate_loyalty'] = get_estimate_loyalty(train)
    test['estimate_loyalty'] = get_estimate_loyalty(test)
    train['premium_to_income'] = get_ratio_to_income(train)
    test['premium_to_income'] = get_ratio_to_income(test)
    train['bin_income'] = get_bins_income(train)
    test['bin_income'] = get_bins_income(test)
    train['bin_score'] = get_bins_score(train)
    test['bin_score'] = get_bins_score(test)
    train['bin_age'] = get_bins_age(train)
    test['bin_age'] = get_bins_age(test)
    train['efficient_income'] = get_efficient_income(train)
    test['efficient_income'] = get_efficient_income(test)
    train['appliscore_reviewed'] = get_new_score(train)
    test['appliscore_reviewed'] = get_new_score(test)
    train['cashincome'] = get_new_score2(train)
    test['cashincome'] = get_new_score2(test)
    replace_string(train)
    replace_string(test)
    return train, test