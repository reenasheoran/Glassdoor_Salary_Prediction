import os
import scraper as sp 
import pandas as pd 

path = "C:/Users/reena/Desktop/Salary_Prediction"

df = sp.get_jobs('data scientist',1000, False, path, 15)
df.to_csv('job_listings.csv', index = False)