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



def ExtractFeature(cnt,data,cs,it,dataframe):
    
    Centroid_x=statistics.mean([cs[it].pos[0] for it in cs ])
    Centroid_y=statistics.mean([cs[it].pos[1] for it in cs ])

    for CellID,it in enumerate(cs):
        if cs[it].id in dataframe['validID']:
            #cell Age
            lastFrame=len(dataframe['validID']) - 1 - dataframe['validID'][::-1].index(cs[it].id)
            dataframe['CellAge'].append(dataframe['CellAge'][lastFrame])
            dataframe['TrackObjects_ParentImageNumber_50'].append(cnt-1)
            dataframe['TrackObjects_ParentObjectNumber_50'].append(dataframe['ObjectNumber'][lastFrame])
            dataframe["TrackObjects_Label_50"].append(dataframe["TrackObjects_Label_50"][lastFrame])
        else:
            #parent detail
            if cs[it].id not in data['lineage']: #birth
                #cell Age
                dataframe['CellAge'].append(0)
                dataframe['TrackObjects_ParentImageNumber_50'].append(0)
                dataframe['TrackObjects_ParentObjectNumber_50'].append(0)
                if dataframe["TrackObjects_Label_50"]==[]:
                    dataframe["TrackObjects_Label_50"].append(1)
                else:
                    dataframe["TrackObjects_Label_50"].append(max(dataframe["TrackObjects_Label_50"])+1)
            else:
                ParentValidID=data['lineage'][cs[it].id]
                ParentFrame=len(dataframe['validID']) - 1 - dataframe['validID'][::-1].index(ParentValidID)
                dataframe['CellAge'].append(dataframe['CellAge'][ParentFrame]+1)
                dataframe['TrackObjects_ParentImageNumber_50'].append(cnt-1)
                dataframe['TrackObjects_ParentObjectNumber_50'].append(dataframe['ObjectNumber'][ParentFrame])
                dataframe["TrackObjects_Label_50"].append(dataframe["TrackObjects_Label_50"][ParentFrame])

        dataframe['ImageName'].append(data['stepNum'])
        dataframe['ImageNumber'].append(cnt)
        dataframe['ObjectNumber'].append(CellID+1)
        dataframe['validID'].append(cs[it].id)
        #cell Type
        # In CellModeller CellTypes are: 0,1,2,3,...
        for index in range(len(dataframe['Type'])):
            if cs[it].cellType==index:
                dataframe['Type'][index].append(1)
            else:
                dataframe['Type'][index].append(0)
        dataframe['AreaShape_Center_X'].append(cs[it].pos[0])
        dataframe['AreaShape_Center_Y'].append(cs[it].pos[1])
        dataframe['AreaShape_MajorAxisLength'].append(cs[it].length)
        dataframe['AreaShape_MinorAxisLength'].append(cs[it].radius)
        angle=math.atan2(cs[it].dir[1],cs[it].dir[0])
        dataframe['AreaShape_Orientation'].append(angle)
        dataframe['Node_x1_x'] .append(cs[it].pos[0] + cs[it].length/2 * math.cos(angle))
        dataframe['Node_x1_y'] .append(cs[it].pos[1] + cs[it].length/2 * math.sin(angle))
        dataframe['Node_x2_x'] .append(cs[it].pos[0] - cs[it].length/2 * math.cos(angle))
        dataframe['Node_x2_y'] .append(cs[it].pos[1] - cs[it].length/2 * math.sin(angle))
        #Surface area of a capsule:
        #S = 2πr(2r + a) 
        dataframe['AreaShape_Area'].append(2*math.pi*cs[it].radius*(cs[it].length+2*cs[it].radius))
        #Distance_from_Centroid
        DistanceFromCentroid=math.sqrt((cs[it].pos[0]-Centroid_x)**2+
                                       (cs[it].pos[1]-Centroid_y)**2)

        dataframe['Distance_from_Centroid'].append(DistanceFromCentroid)        

def startingProcess(Input,CellTypes,Output):
    for dname in enumerate(glob.glob(Input)):
        print(dname)
        dataframe={'ImageNumber':[],'ObjectNumber':[],'Type':[],'AreaShape_Area':[],'AreaShape_Center_X':[],'AreaShape_Center_Y':[],
                       'AreaShape_MajorAxisLength':[],'AreaShape_MinorAxisLength':[],'AreaShape_Orientation':[],
                       'Node_x1_x':[],'Node_x1_y':[],'Node_x2_x':[],'Node_x2_y':[],
                       'CellAge':[],'TrackObjects_ParentImageNumber_50':[],'TrackObjects_ParentObjectNumber_50':[],
                       'validID':[],'ImageName':[],'TrackObjects_Label_50':[],'Distance_from_Centroid':[]}

        for element in CellTypes:
            dataframe['Type'].append([])

        path = dname[1]+"/*.pickle"
        for cnt,fname in enumerate(glob.glob(path)):
            data = pickle.load(open(fname,'rb'))
            cs = data['cellStates']
            it = iter(cs)
            ExtractFeature(cnt+1,data,cs,it,dataframe)

        #create data frame
        df = pd.DataFrame({'ImageName':dataframe['ImageName'],'ImageNumber':dataframe['ImageNumber'],'ObjectNumber':dataframe['ObjectNumber'],
                           'AreaShape_Area':dataframe['AreaShape_Area'],'AreaShape_Center_X':dataframe['AreaShape_Center_X'],
                           'AreaShape_Center_Y':dataframe['AreaShape_Center_Y'],'AreaShape_MajorAxisLength':dataframe['AreaShape_MajorAxisLength'],
                           'AreaShape_MinorAxisLength':dataframe['AreaShape_MinorAxisLength'],
                           'AreaShape_Orientation':dataframe['AreaShape_Orientation'],'Number_Object_Number':dataframe['validID'],
                           "TrackObjects_Label_50":dataframe["TrackObjects_Label_50"],
                           'TrackObjects_ParentImageNumber_50':dataframe['TrackObjects_ParentImageNumber_50'],
                           'TrackObjects_ParentObjectNumber_50':dataframe['TrackObjects_ParentObjectNumber_50'],
                           'CellAge_Generation':dataframe['CellAge'],'Node_x1_x':dataframe['Node_x1_x'],'Node_x1_y':dataframe['Node_x1_y'],
                           'Node_x2_x':dataframe['Node_x2_x'],'Node_x2_y':dataframe['Node_x2_y'],
                           'Distance_from_Centroid':dataframe['Distance_from_Centroid']})

        # Using DataFrame.insert() to add a column
        columnNum=3
        for cnt,CellType in enumerate(CellTypes):
            df.insert(columnNum, CellType, dataframe['Type'][cnt], True)
            columnNum+=1

        #write to csv
        df.to_csv(Output+dname[1].split('/')[-1].split('\\')[-1]+".csv", index=False)



        




    


