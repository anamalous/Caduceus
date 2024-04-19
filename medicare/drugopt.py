import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import matplotlib.pyplot as plt

def drugoptim(age,height,weight,sex,illness):
    data=pd.read_csv("./medicare//static/datasets/csvdata/patientdrugdata.csv")

    baseset=data[data["Current Illness"]==illness]
    baseset=baseset.fillna(0)

    X=baseset[["Age","Weight","Height","Sex"]]
    X[X["Sex"]=="Female"]=1
    X[X["Sex"]=="Male"]=0
    Y=baseset[["Medication","Route"]]

    meds=list(Y["Medication"].unique())
    routes=list(Y["Route"].unique())
    Y["Medication"]=[meds.index(i) for i in Y["Medication"]]
    Y["Route"]=[routes.index(i) for i in Y["Route"]]

    t=DecisionTreeClassifier(criterion="entropy",max_depth=40,max_features=45*9)
    t.fit(X,Y)
    res=t.predict(np.array([age,height,weight,sex]).reshape(1,4))

    bset=baseset[baseset["Medication"]==meds[res[0][0]]]
    bset=baseset[baseset["Route"]==routes[res[0][1]]]
    plt.scatter(baseset["Height"]/10,baseset["Weight"]/10)
    plt.plot([int(height)/10]*10,[i for i in range(0,10,1)])
    plt.plot([i for i in range(0,20,2)],[int(weight)/10]*10)
    try:
        plt.savefig("./medicare/media/media/graph"+str(age+weight)+".png")
    except:
        pass
    return [meds[res[0][0]],routes[res[0][1]],list(baseset["Dosage"])[0],"media/media/graph"+str(age+weight)+".png"]
