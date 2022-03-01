import sys
import os
import math
import numpy as np
sys.path.append('.')
import pickle
import CellModeller
import pandas as pd
import glob
import statistics
      

def startingProcess(Input,Output):
    for fname in enumerate(glob.glob(Input)):
        print(fname[1])
        df = pd.read_csv(fname[1])
        df2=pd.DataFrame()

        df2 = df.loc[df["ImageName"] %30==0]
            

        #write to csv
        df2.to_csv(Output+fname[1].split('/')[-1].split('\\')[-1], index=False)


#Getting the location of simulations.
Input="G:/My Drive/UWaterloo/Feb 9/Sensitivity Analysis/default values/CellModellerProcess/*.csv"
#The location of the CSV output files
#(For each simulation, an output file will be created.)
Output="G:/My Drive/UWaterloo/Feb 9/Sensitivity Analysis/default values/CellModellerProcessSkip30/"
#Start Processing
startingProcess(Input,Output)




        




    


