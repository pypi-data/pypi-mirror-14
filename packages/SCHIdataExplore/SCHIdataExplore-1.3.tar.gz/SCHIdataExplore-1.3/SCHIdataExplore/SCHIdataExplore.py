#########################
# Data Exploration pipeline for new students and data wranglers
# Authors: Alexander Titus & Rebecca Faill
# Dartmouth College: Social Computing & Health Informatics Lab
# PI: Amar K. Das, MD, PhD
# ~~~~~~~~~~~~~~~~~~~~~~~
# This file is intended to provide a pipeline for people to summaryize and
# explore their data when they are getting into a new project or working
# with new and previoulsy unknown data to them.
#########################

# LOAD THE NECESSARY ENVIRONMENT DEPENDENCIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os

# IMPORT A SINGLE .CSV FILE FROM A DESIGNATED DIRECTORY
def importSingleCSV(directory, fileName):
    """
    importData(directory)
    Parameters:
        directory - the absolute file directory where the csv file is kept.
        fileName - the string name of the file to import (ex 'file.csv')
    """
    os.chdir(directory)
    data = pd.read_csv(fileName)
    return data

# IMPORT .CSVs FROM A USER DEFINED LIST OF FILES
def importMultCSVs(directory, fileList):
    """
    importUserCsvFiles(directory, fileList) imports and concatenates .csv files
    from a user defined list in a directory into one large file using a full
    outer-join. It is recommended that you check to make sure your files have
    the same columns in each.
    Parameters:
        directory - the absolute file directory where the csv files are kept.
        fileList - the list of string names of the files to import (ex ['file.csv', 'file2.csv'])
    """
    os.chdir(directory)
    keys = list()
    data = list()
    for file in fileList:
        if not file.startswith('.'):
            tempData = importSingleCSV(directory, file)
            data.append(tempData)
            keys.append(file)
    fullData = pd.concat(data, join = 'outer', keys = keys)
    return fullData

# IMPORT ALL .CSV FILES LISTED IN A DESIGNATED DIRECTORY
def importCsvDataDir(directory):
    """
    importData(directory) imports and concatenates every csv file in a directory
    into one large file using a full outer-join. It is recommended that you check
    to make sure your files have the same columns in each.
    Parameters:
        directory - the absolute file directory where the csv files are kept.
    """
    os.chdir(directory)
    fileList = os.listdir(directory)
    fullData = importMultCSVs(directory, fileList)
    return fullData

# SUBSET A DATAFRAME BY A USER DEFINED LIST OF COLUMNS
def subsetData(dataFrame, colList):
    subset = dataFrame[colList]
    return subset

# SUMMARIZE THE NUMBER OF ROWS AND COLUMNS IN A SUBSET OF DATA
def summarize(data):
    """
    This function is designed to be used in the manner of:
    data.groupby('selector').apply(summarize)
    This allows the user to summarize the number of records found
    for different groupings.
    """
    return pd.Series({'nrow':len(data), 'ncol': len(data.columns)})

# SUMMARIZE THE NUMBER OF ROWS AND COLUMNS IN A SUBSET OF DATA
def summarize2(data):
    """
    This function is designed to be used in the manner of:
    data.groupby('selector').apply(summarize)
    This allows the user to summarize the number of records found
    for different groupings.
    """
    return pd.Series({'nrow':len(data)})

# DESCRIBE THE DATA WE ARE IMPORTING
def describeData(dataFrame):
    """
    This function provides descriptive data for each column in the input dataframe.
    The output is: row count; unique row count; value most common; frequency of common value.
    """
    descriptions = dataFrame.describe()
    descDictionary = dict()
    for col in descriptions.columns:
        descDictionary[col] = descriptions[col]
    temp = pd.DataFrame()
    for key in descDictionary.keys():
        col = descDictionary[key]
        temp = pd.concat([temp, col], axis=1)
    return temp

# DESCRIBE THE DATA WE ARE IMPORTING ORGANIZING BY ONE USER DEFINED COLUMNS
def oneColDescData(dataFrame, colName, sumVar):
    """
    Parameters:
        dataFrame - The data we are using.
        colName - The column name to stratify by.
        sumVar - The column name to analyze in each stratification.
    """
    print 'Summarizing data, stratifying by ' + colName + ', and summarizing ' + sumVar + '.'
    print ''
    data = dataFrame.groupby(colName)[sumVar].describe()
    return data

# DESCRIBE THE DATA WE ARE IMPORTING ORGANIZING BY TWO USER DEFINED COLUMNS
def twoColDescData(dataFrame, colTuple, sumVar):
    """
    Parameters:
        dataFrame - The data we are using.
        colTuple - The column names to stratify by (ex/ [name1, name2]).
        sumVar - The column name to analyze in each stratification.
    """
    print 'Summarizing data, stratifying by ' + colTuple[0] +' & ' + colTuple[1] + ', and summarizing ' + sumVar + '.'
    print ''
    data = dataFrame.groupby([colTuple[0], colTuple[1]])[sumVar].describe()
    return data

# DESCRIBE THE DATA WE ARE IMPORTING ORGANIZING BY THREE USER DEFINED COLUMNS
def threeColDescData(dataFrame, colTriple, sumVar):
    """
    Parameters:
        dataFrame - The data we are using.
        colTriple - The column names to stratify by (ex/ [name1, name2, name3]).
        sumVar - The column name to analyze in each stratification.
    """
    print 'Summarizing data, stratifying by ' + colTriple[0] +', ' + colTriple[1] + ', & ' + colTriple[2] + ', and summarizing ' + sumVar + '.'
    print ''
    data = dataFrame.groupby([colTriple[0], colTriple[1], colTriple[2]])[sumVar].describe()
    return data

# SAVE DATAFILE TO .CSV
def saveCSV(fileName, dataFrame):
    """
    saveCSV(fileName, dataFrame) saves a designated dataframe to a csv file in the
    current working directory.
    Parameters:
        fileName - The name of the output file
        dataFrame - the dataframe that is being saved to a .CSV file
    """
    dataFrame.to_csv(fileName, sep = ',')

# COUNT MISSING VALUES
def numMissing(x):
    """
    This function counts the number of missing data points in a data list.
    Parameters:
        x - a list of data to check for missing values.
    """
    return sum(x.isnull())

# FIND THE DUPLICATED ROWS IN A DATAFRAME
def findDuplicateRows(dataFrame):
    """
    This function takes in a dataframe and outputs two dataframes, the first for
    unique data rows and the second a dataframe of duplicated data from the first.
    """
    duplicated = dataFrame.duplicated()
    duplicatedDataFrame = dataFrame[duplicated==True]
    uniqueDataFrame = dataFrame[duplicated==False]
    return duplicatedDataFrame, uniqueDataFrame, duplicated

# SUMMARIZE DUPLICATED DATA ROWS
def summarizeDuplicateData(dataFrame):
    """
    This function generates a summary of duplicated data from a dataframes
    Parameters:
        dataFrame - The dataframe to analyze for duplicated data.
    """
    data = findDuplicateRows(dataFrame)
    description = describeData(data[0])
    return description

# IDENTIFY COLUMNS THAT HAVE MISSING VALUES
def missingByCol(dataFrame):
    """
    findMissCol(dataFrame) returns a dictionary of column names associated
    with a list of indecies with NULL values.
    Parameters:
        dataFrame - The dataframe we are searching for null values.
    """
    missing = dataFrame.apply(numMissing, axis=0).to_frame()
    return missing.sort_values(by=missing.columns[0], ascending=False)

# SUMMARIZE DATA BY CATEGORICAL COLUMNS
def dataSummaryByCol(dataFrame, colNames, colClassList):
    """
    This function returns a dictionary of data summaries for each column in the
    dataframe that is categorical data, based on a user defined list of
    classifications.
    Parameters:
        dataFrame - the dataframe to summarize
        colClassList - a list of continuous/categorical classifications for
            each data column in dataFrame ('Cont', 'Cat').
    """
    summaries = dict()
    count = 0
    for column in colClassList:
        colName = colNames[count]
        if column == 'Cat':
            tempSummary = dataFrame.groupby(colName).apply(summarize2)
            summaries[colName] = tempSummary.sort_values(by='nrow', ascending=False)
            count+= 1
    return summaries

# PLOT A HISTOGRAM FROM OUR DATAFRAME
def plotHistOneColDesc(oneColDescSeries, fileName):
    """
    This function plots the mean and frequency of data in a data set.
    Parameters:
        oneColDescSeries - The output from the function oneColDescData()
        fileName - The user-specified output file name
    """
    values = oneColDescSeries.index.levels[0].values
    d = dict()
    for i in range(len(values)):
        # Making an assumption that if the description exists at all, it has mean at #2, etc.
        if(len(oneColDescSeries[values[i]]) > 0):
            d[values[i]] = oneColDescSeries[values[i]].values[1] # the mean - the second row
    fig = plt.figure()
    fig1 = fig.add_subplot(1, 2, 1)
    plt.bar(range(len(d)), d.values(), align='center')
    plt.xticks(range(len(d)), d.keys(), rotation='vertical')
    plt.title('Mean by Category')
    plt.ylabel('Mean')
    plt.xlabel('Categories')
    d = dict()
    for i in range(len(values)):
        # Making an assumption that if the description exists at all, it has mean at #2, count at #1,  etc.
        if(len(oneColDescSeries[values[i]]) > 0):
            d[values[i]] = oneColDescSeries[values[i]].values[0]
    fig2 = fig.add_subplot(1, 2, 2)
    plt.bar(range(len(d)), d.values(), align='center')
    plt.xticks(range(len(d)), d.keys(), rotation='vertical')
    plt.title('Count by Category')
    plt.ylabel('Number of Records')
    plt.xlabel('Categories')
    plt.subplots_adjust(wspace=0.5)
    plt.savefig(fileName + '.png', dpi=400)
    return fig

# PLOT A HISTOGRAM FROM OUR DATAFRAME
def plotHistTwoColDesc(twoColDescSeries, fileName):
    """
    This function plots the mean and frequency of data in a data set.
    Parameters:
        twoColDescSeries - The output from the function twoColDescData()
        fileName - The user-specified output file name
    """
    values = twoColDescSeries.index.levels[0].values
    for i in range(len(values)):
        level = twoColDescSeries[values[i]]
        fileName2 = str(fileName) + '_' + str(values[i])
        figs = plotHistOneColDesc(level, fileName)
        fileName2 = ''
    return figs
