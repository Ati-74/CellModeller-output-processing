import CellModellerProcessing

#Getting the location of simulations.
Input="E:/MyDrive/UWaterloo/Feb 9/Sensitivity Analysis/gamma/gamma=2/T*"
#The name of the bacteria Types.
CellTypes=['RFP','YFP']
#The location of the CSV output files
#(For each simulation, an output file will be created.)
Output="E:/MyDrive/UWaterloo/Feb 9/Sensitivity Analysis/gamma/gamma=2/CellModellerProcess/"
#Start Processing
CellModellerProcessing.startingProcess(Input,CellTypes,Output)
