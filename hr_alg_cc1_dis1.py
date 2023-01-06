import random
import math
import numpy 
import csv
import operator

#--------------------------------
def euclidean_normalize_dist(num1,num2,minVal,maxVal):
    #return math.pow((float(num1)-float(num2))/(maxVal-minVal),2)
    return abs(float(num1)-float(num2))/abs(maxVal-minVal)
#---------------------------------------
def allDistance(object1,object2):
    distance = 0
    commonAttr = 0

    #Numerical attr distance
    for j in numericalAttrIndex:
        if((object1[j].strip() == '?') or (object2[j].strip() == '?') ):
            distance += 1
        else:
            dis = round(euclidean_normalize_dist(object1[j],object2[j],0,rangeArr[j]),10)
            distance += dis
            if (dis) < threshold :
                commonAttr += 1  
            
    #nonNumerical attr distance
    for j in nonNumericalAttrIndex:
        if((object1[j].strip() == '?') or (object2[j].strip() == '?') ):
            distance += 1
        else:
            tmpSum = 0
            if object1[j] != object2[j]:
                for j2 in numericalAttrIndex:
                    if((object1[j2].strip() != '?') and (object2[j2].strip() != '?') ):
                        if ((abs(float(object1[j2])-float(object2[j2])))/(rangeArr[j2]))<= threshold:
                            tmpSum+=1

                for j2 in nonNumericalAttrIndex:
                    if object1[j2] == object2[j2]:
                        tmpSum+=1

                distance += (tmpSum/ (len(numericalAttrIndex)+len(nonNumericalAttrIndex)))
            else:
                commonAttr += 1  

    return distance,commonAttr
#-------------------------------------------------    
def custerCenterSelect(dataArr):
    #next ClusterCenters     #disMatix
    disMatrix = []

    for i2 in dataArr:
        disMatrixRow = []
        for j2 in dataArr:
            dis = allDistance(j2,i2)[0]
            disMatrixRow.append(dis)
        disMatrix.append(disMatrixRow)
    
    minDisC1 = 10000 
    minDisC1Index = 0 
    counterC1 = 0
    for i2 in disMatrix:
        sumC1 = 0
        for j2 in i2:
            sumC1 += j2
        #print('summmm:',sumC1)
        if(sumC1 < minDisC1):
            minDisC1 = sumC1
            minDisC1Index = counterC1
        #print('counterC1 - ', counterC1 ,' *org: ',int(dataArr[counterC1][0])-int(1), ' * sumC1: ', sumC1 , ' - minDisC1: ',minDisC1 )
        counterC1+= 1
    #print('**selected**',int(dataArr[minDisC1Index][0])-int(1))
    #print('**dataArr[minDisC1Index][0]-1**',int(dataArr[minDisC1Index][0])-int(1))
    #print(disMatrix)
    return (int(dataArr[minDisC1Index][dataIndexRow])-int(1))  #return index of object in dataset
    #print('selected',minDisC1 ,'**',minDisC1Index,'***',dataArr[minDisC1Index][0])
#--------------------------------------------------
def custerCenterSelect0(dataArr,ccCount):
    disMatrix = []

    for i2 in dataArr:
        disMatrixRow = []
        for j2 in dataArr:
            dis = allDistance(j2,i2)[0]
            disMatrixRow.append(dis)
        disMatrix.append(disMatrixRow)
    
    disArrList = []
    counterC1 = 0
    for i2 in disMatrix:
        sumC1 = 0
        for j2 in i2:
            sumC1 += j2
        disArrList.append({'dis':sumC1 , 'index': counterC1})
        counterC1+= 1

    sortedDisArrList = sorted(disArrList, key=operator.itemgetter('dis'))
    

    '''print("---01 ------------------------------")
    print(disArrList)
    print("---02 ------------------------------")    
    print(sortedDisArrList)
    print("---03 ------------------------------")'''

    '''
    print (" halate 1 ---------------------")
    returnCount = 0
    returnArr = []
    while(returnCount < ccCount):
        minDisIndex = sortedDisArrList[returnCount]['index']
        returnArr.append(int(dataArr[minDisIndex][dataIndexRow])-int(1))
        returnCount +=1
    print(returnArr)
    '''

    #print (" halate 2 ---------------------")
    ccArr = []
    ccArr.append(sortedDisArrList[0]['index'])
    #ccArr.append(sortedDisArrList[len(sortedDisArrList)-1]['index'])
    
    lastCC = sortedDisArrList[0]['dis']
    for item1 in sortedDisArrList:
        if ((item1['dis']- lastCC) >= ((sortedDisArrList[len(sortedDisArrList)-1]['dis'] - sortedDisArrList[0]['dis'])/ccCount)):
            if(item1['index'] not in ccArr):
                ccArr.append(item1['index'])
                lastCC = item1['dis']
        if(len(ccArr)== ccCount):
            break

    #print ("ccArr",len(ccArr))
    #exit

    #print ("ccArr",ccArr)

    if(len(ccArr)<ccCount):
        countLose = 1
        while (ccCount-len(ccArr)>0):
            selectedIndex = sortedDisArrList[len(sortedDisArrList)-countLose]['index']
            if selectedIndex not in ccArr:
                ccArr.append(selectedIndex)
            countLose += 1
                                               
    #print ("ccArr",ccArr)
    #exit
    #print("---------------------------")

    return ccArr  #return index of object in dataset
#--------------------------------------------------
def accuracyEv(clusterdata,className):
    if(len(clusterdata)==0):
        return 0,0

    cCount = []
    for item in CCClass:
        cCount.append(0)

    for d in clusterdata:
        if d[classIndex].strip() == CCClass[0]:
            cCount[0] += 1
        elif d[classIndex].strip() == CCClass[1]:
            cCount[1] += 1

    #print("\n***********************\n")
    #print("cCountClass:",cCount)

    max = 0
    clusterClass = ""
    for item in cCount:
        if(item>max):
            max = item
    clusterClass = max
    #print("selected:",clusterClass)
    #print("\n***********************\n")
    
    '''
    counter=0
    for d in clusterdata:
        if d[classIndex] == className:
            counter = counter+1

    accuracy = (counter) / len(clusterdata)
    '''
    accuracy = (max) / len(clusterdata)
    return accuracy ,max
#-------------------------------------

#seiitings

k=2
#k = raw_input("Enter Count of Clusters (k):")
#print("Count of Clusters (k): "+k)0.1

threshold = 0.05  #10 0.15 % normalize
#float(threshold)
#print("threshold : "+ str(threshold))

classIndex = 14
CCClass = ['<=50K','>50K']

dataIndexRow = 15

numericalAttrIndex = [0,2,4,10,11,12]
nonNumericalAttrIndex = [1,3,5,6,7,8,9,13]
rangeArr= numpy.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
rangeArr[0]=100
rangeArr[2]=1500000
rangeArr[4]=16
rangeArr[10]=100000
rangeArr[11]=4400
rangeArr[12]=100
#-------------------------------------------
#dataset
with open('dataset\\adult.csv', 'rt') as csvfile:
    data2 = list(csv.reader(csvfile))
dataset = data2

dataIndex =0
for i in dataset:
    dataIndex +=1
    i.append(dataIndex)   #add RowIndex To item
#-----------------------------------------------
accArr = [] 
RIArr = []
FMArr = []

topAcc = 0
topRI = 0
topFM = 0

cluster1 = []
cluster1det = []
cluster2 = []
cluster2det = []

objectsCCArrOLD = [0]
objectsCCArrNEW = [-1]
oldACC = -1
newACC=0

minDisC1Index=0

itercounter=0
#while(itercounter<50):
while((objectsCCArrOLD != objectsCCArrNEW) and (oldACC < newACC )):
    objectsCCArrOLD = objectsCCArrNEW
    objectsCCArrNEW = []

    oldACC = newACC
    newACC = 0

    #clusterCenters -------------------------------------------

    clusterCenters = []

    if(itercounter == 0):
        tmpDataset = dataset
        ccArr = custerCenterSelect0(dataset,k)
        for item in ccArr:
            clusterCenters.append(dataset[item])        
    else:        
        clusterCenters.append(dataset[custerCenterSelect(cluster1det)])
        clusterCenters.append(dataset[custerCenterSelect(cluster2det)])

    #print('clusterCenters : ',clusterCenters )
    #-----------------------------------------------
    cluster1 = []
    cluster1det = []
    cluster2 = []
    cluster2det = []
    dataIndex = 0

    for i in dataset:
        dataIndex +=1
        disArr =[]
        commonAttrArr = []
        for k in clusterCenters:
            result = allDistance(i,k)
            distance = result[0]                                                                            
            commonAttr = result[1]
            disArr.append(distance)
            commonAttrArr.append(commonAttr)
            #print ("distance: " , distance ,"  - commonAttr: " ,commonAttr)

        sortedDisArr = sorted(disArr)

        sortedCommonArr = sorted(commonAttrArr)[::-1]
        #print  ("minDis : ", round(sortedDisArr[0] ,2) , "--", "maxCommon : ", sortedCommonArr[0])

        minDisIndex= disArr.index(sortedDisArr[0])
        maxCommonIndex= commonAttrArr.index(sortedCommonArr[0])

        #print  ("minDisIndex : ", minDisIndex , "--", "maxCommonIndex : ", maxCommonIndex)

        if minDisIndex==maxCommonIndex:
            if minDisIndex==0:
                cluster1.append(dataIndex)
                cluster1det.append(i)
                objectsCCArrNEW.append(1)
            else:
                cluster2.append(dataIndex)   
                cluster2det.append(i)
                objectsCCArrNEW.append(2)

        elif  commonAttrArr[minDisIndex] ==sortedCommonArr[0] :
            if minDisIndex==0:
                cluster1.append(dataIndex)
                cluster1det.append(i)
                objectsCCArrNEW.append(1)
            else:
                cluster2.append(dataIndex)   
                cluster2det.append(i)
                objectsCCArrNEW.append(2)

        elif  (abs(sortedDisArr[0]-disArr[maxCommonIndex])/100) < threshold:
            if maxCommonIndex==0:
                cluster1.append(dataIndex)
                cluster1det.append(i)
                objectsCCArrNEW.append(1)
            else:
                cluster2.append(dataIndex)   
                cluster2det.append(i)
                objectsCCArrNEW.append(2)

        else:
            if minDisIndex==0:
                cluster1.append(dataIndex)
                cluster1det.append(i)
                objectsCCArrNEW.append(1)
            else:
                cluster2.append(dataIndex)   
                cluster2det.append(i)
                objectsCCArrNEW.append(2)

    #print ('\n ')

    #print ("cluster1: ", cluster1)
    #print ("cluster2: ", cluster2)
    #evaluation -----------------------------------------
    sumCounter = 0
    result = []
    result = accuracyEv(cluster1det,CCClass[0])
    sumCounter += result[1]
    #print ("acuracy of cluster 1 is : ", result[0],'**------',result[1])

    result = accuracyEv(cluster2det,CCClass[1])
    sumCounter += result[1]
    #print ("acuracy of cluster 2 is : ", result[0],'**------',result[1])

    totalAcc = sumCounter / len(dataset)
    accArr.append(totalAcc)
    #print ("total acuracy is : ", totalAcc)
    newACC = totalAcc
    #----------------------------------
    # RI (rand Index) measure
    count = 0
    numArr = []
    TP = 0 
    FP = 0
    TN = 0
    FN = 0

    '''
    while (count < len(dataset) ):
        numArr2 = []
        while (len(numArr2)<2):
            index1 = random.randint(0,149)
            if(index1 not in numArr and index1 not in numArr2):
                numArr.append(index1)
                count +=1
                numArr2.append(index1) '''

    tmpArr = []
    for x in range(len(dataset)):
        tmpArr.append(x)

    while (len(tmpArr)>1):
        numArr2 = []
        while (len(numArr2)<2):
            rndIndex = random.randint(0,len(tmpArr)-1)
            numArr2.append(tmpArr[rndIndex])
            tmpArr.pop(rndIndex)
        #print('numArr2:',numArr2)        
                
        index1 = numArr2[0]
        index2 = numArr2[1]

        if(dataset[index1][classIndex].strip() == dataset[index2][classIndex].strip() ):
            if (((index1) in cluster1) and ((index2) in cluster1)) or (((index1) in cluster2) and ((index2) in cluster2 )):
                TP += 1
            else:
                FN += 1
        else:
            if (((index1) in cluster1) and ((index2) in cluster1)) or (((index1) in cluster2) and ((index2) in cluster2 )):
                FP += 1
            else:
                TN += 1


        #print ("index1:",index1," - index2:",index2)
    #print ("TP:",TP," - TN:",TN," - FP:", FP , " - FN:", FN)

    RI = (TP+TN)/(TP+FP+ FN+TN)
    RIArr.append(RI)
    #print ("RI : ",RI)

    # F-measure
    P = TP / (TP+FP)
    R= TP / (TP+FN)
    FM = (2*P*R)/(P+R)
    FMArr.append(FM)
    #print ("F-measure : ",FM)

    #----------------------------------------------------
    itercounter+=1
    #print ('-------------------------------------------------')
#print(disMatrix[1])

#print("total acc arr :",sorted(accArr)[::-1])
print("total acc arr :",accArr)
print("top ACC  Sorted: :",sorted(accArr)[::-1])
print("top ACC  : :",sorted(accArr)[::-1][0])
print("final RI  :",sorted(RIArr)[::-1][0])
print("final FM  :",sorted(FMArr)[::-1][0])