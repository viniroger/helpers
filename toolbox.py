#!/usr/bin/env python3.7.9
# -*- Coding: UTF-8 -*-

'''
Generic methods for python scripts
author: Vinicius Roggério da Rocha
e-mail: viniroger@monolitonimbus.com.br
version: 0.0.1
date: 2021-04-01
'''

import glob
import numpy as np
import pandas as pd

class Files():
    '''
    Functions to deal with files
    '''

    @staticmethod
    def list_files(pattern):
        '''
        Create file's list using pattern (with path)
        Ex: /path/*.ext to list all ext files at path
        '''
        files = sorted([f for f in glob.glob(pattern, recursive=True)])
        return files

    @staticmethod
    def create_df(columns_names):
        '''
        Create empty dataframe with columns names pased by argument
        '''
        df = pd.DataFrame(columns=columns_names)
        return df

    @staticmethod
    def read_csv(filename):
        '''
        Read CSV by file name
        '''
        df = pd.read_csv(filename)
        return df

    @staticmethod
    def save_csv(df, filename):
        '''
        Save DF into CSV
        '''
        df.to_csv(filename, index=False)

    @staticmethod
    def write_dat(filename, df, fmt):
        '''
        Write df to file with column fixed according to given format fmt
        '''
        with open(filename, 'w') as ofile:
            np.savetxt(ofile, df.values, fmt=fmt)

class Data():
    '''
    Functions to deal with dataframes etc
    '''

    @staticmethod
    def append_lst_df(df, lst):
        '''
        Append list as new row at dataframe
        '''
        df.loc[len(df)] = lst
        return df

    @staticmethod
    def join_df(df_all, df):
        '''
        Join two dataframes
        '''
        if df_all.empty:
            df_all = df.copy()
        else:
            df_all = df_all.append(df)
        return df_all

    @staticmethod
    def mean_df(df, column_name):
        '''
        Calculate means at each 5 minutes
        New timestamp like index
        '''
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S')
        df = df.set_index('Timestamp')
        df[column_name] = df[column_name].apply(pd.to_numeric, errors='coerce')
        df_means = df.resample('5Min').mean()
        return df_means

class Plot():
    '''
    Functions to plot images
    '''

    @staticmethod
    def plot_ts(df, varname, path):
        '''
        Plot variable versus time for one day and save PNG
        Time is at Timestamp format
        '''
        # Convert datetime format
        format = '%Y-%m-%d %H:%M:%S'
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], format=format)

        fig, ax = plt.subplots()
        ax.plot(df['Timestamp'], df[varname], label=varname,\
         linestyle=':', marker='o')

        day_in = pd.to_datetime(df['Timestamp'][0])
        day = day_in.strftime('%Y-%m-%d')
        plt.title('{0} - {1}'.format(day, varname))

        hours = mdates.HourLocator(interval = 1)
        h_fmt = mdates.DateFormatter('%H:%M')
        ax.xaxis.set_major_locator(hours)
        ax.xaxis.set_major_formatter(h_fmt)

        fig.autofmt_xdate()
        plt.savefig('{0}/{1}_{2}.png'.format(path, varname, day))
        plt.close()
