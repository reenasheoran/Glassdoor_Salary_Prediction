import os 
import pandas as pd 
from load_data import read_params
import argparse

def data_clean(config_path):
    config= read_params(config_path)
    data_path=config["load_data"]["raw_data_csv"]
    df = pd.read_csv(data_path,sep=',',encoding='utf-8')
    
    #salary

    df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
    df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)
    df = df[df['Salary Estimate'] != '-1']
    df['Salary Estimate']= df['Salary Estimate'].apply(lambda x: x.split('(')[0])
    df['Salary Estimate'] = df['Salary Estimate'].apply(lambda x: x.replace('K','').replace('$',''))
    df['Salary Estimate'] = df['Salary Estimate'].apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))
    df['min_salary'] = df['Salary Estimate'].apply(lambda x: int(x.split('-')[0]))
    df['max_salary'] = df['Salary Estimate'].apply(lambda x: int(x.split('-')[1]))
    df['avg_salary'] = (df.min_salary+df.max_salary)/2

    #Company 
    df['Company']=df['Company Name']
    
    #state  
    df['State'] = df['Location'].apply(lambda x: x.split(',')[1])
    #print(df.State.value_counts())
    df['In-HQ_State'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis = 1)

    #Company Age
    df['Company Age'] = df.Founded.apply(lambda x: x if x <1 else 2021 - x)

    #job skill description 

    #python
    df['Python'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
    print(df.Python.value_counts())
    #r studio 
    df['R'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
    print(df.R.value_counts())

    #spark 
    df['Spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
    print(df.Spark.value_counts())

    #aws 
    df['AWS'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
    print(df.AWS.value_counts())

    #excel
    df['Excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
    print(df.Excel.value_counts())

    print(df.columns)

    df = df.drop(['Unnamed: 0'], axis =1)
    cleaned_data_path=config["cleaned_data"]["cleaned_data_csv"]
    df.to_csv(cleaned_data_path,sep=',',encoding='utf-8',header=True,index=False)
    

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default='params.yaml')
    args_parsed = args.parse_args()
    data_clean(config_path=args_parsed.config)