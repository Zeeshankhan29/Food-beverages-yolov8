from src.checkout.entity import DataAnalyticsconfig
import pandas as pd
import numpy as np 
import seaborn as sn 
import matplotlib.pyplot as plt 
import os
import yaml



class DataAnalytics:
    def __init__(self,DataAnalyticsconfig = DataAnalyticsconfig):
        self.config = DataAnalyticsconfig
        self.curdir = os.getcwd()


    def load_files(self):
        for file in os.listdir(self.config.Analytics_input_dir):
            filename = file.split(".")[0]
            file_path = os.path.join(self.curdir,self.config.Analytics_input_dir,file)
            df = pd.read_csv(file_path)
            
            alldataframe=[]
            for i in df['Model Name'].unique():
                alldataframe.append(df[df['Model Name'] == i])
            else:
                print(f"Total models data found ----> {len(alldataframe)}")

            for i in range(len(alldataframe)):
                model_name = alldataframe[i]['Model Name'].unique()[0]
                dataframe = alldataframe[i]
                final_path = os.path.join(self.curdir,self.config.Analytics_output_dir,filename,model_name)
                os.makedirs(final_path, exist_ok=True)
                dataframe.to_csv(f"{final_path}/{model_name}.csv",index=False)
            else:
                print('Data Splitting completed')
    
    def analysis(self):
        folder_path = os.path.join(self.curdir,self.config.Analytics_output_dir)
        for subfolder in os.listdir(folder_path):
            for file in os.listdir(os.path.join(folder_path,subfolder)):
                for filename in os.listdir(os.path.join(folder_path,subfolder,file)):
                    filename1 = filename.split('.')[0]
                    out_path = os.path.join(folder_path,subfolder,file)
                    if not file == filename1:
                        continue
                    print(f'{filename} file found, Analysis started')
                    print('\n')
                    file_path = os.path.join(out_path,filename)
                    df = pd.read_csv(file_path)
                    df1 =df[['Model Name','Class Name','Prediction Confidence','Predicted Class','Captured Image Path','Date of Creation']]
                    df2 = df1.sort_values(by=['Class Name','Prediction Confidence'],ascending=[True,False])
                    
                    #top1 with >= 0.89 Confidence (TP)
                    df3 = df2[(df2['Class Name'] == df2['Predicted Class']) & (df2['Prediction Confidence'] > 0.89)]
                    df3.to_csv(f"{out_path}/top1&greater0.89PredictionConf.csv",index=False)
                    
                    #top1 with 0.0 Confience
                    df3 = df2[(df2['Class Name'] == df2['Predicted Class'])]
                    df3.to_csv(f"{out_path}/top1&0.0PredictionConf.csv",index=False)
                    
                    #worst1 with <= 0.09 Confidence(TN)
                    df3 = df2[(df2['Class Name'] != df2['Predicted Class']) & (df2['Prediction Confidence'] < 0.09)]
                    df3.to_csv(f"{out_path}/worst1&less0.09PredictionConf.csv",index=False)

                    #Positive Statistics 
                    df3 = df2[df2['Class Name'] == df2['Predicted Class']].describe()
                    df3.to_csv(f"{out_path}/Positivestats.csv")

                    #Negative Statistics 
                    df3 = df2[df2['Class Name'] != df2['Predicted Class']].describe()
                    df3.to_csv(f"{out_path}/Negativestats.csv")
        else:
            print(f"{'^'*20}Analysis Completed{'^'*20}")