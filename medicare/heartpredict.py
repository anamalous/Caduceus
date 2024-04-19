from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def heartpredict(data):
    neigh = KNeighborsClassifier(n_neighbors=1000)
    df = pd.read_csv("./medicare/heart_disease_health_indicators_BRFSS2015.csv")
    X = df.drop(columns=['HeartDiseaseorAttack','PhysActivity', 'Fruits', 'Veggies',
       'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'GenHlth',
       'MentHlth', 'PhysHlth', 'DiffWalk', 'Sex', 'Age', 'Education',
       'Income'], axis=1)
    y = df['HeartDiseaseorAttack']
    neigh.fit(X, y)
    return neigh.predict(data)
print(heartpredict(np.array([0,0,0,0,0,0,0]).reshape(1,7)))
