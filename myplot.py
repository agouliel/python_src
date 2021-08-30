import matplotlib.pyplot as plt
import numpy as np
import random
import seaborn as sns
import pandas as pd

### seaborn barplot random data ###

rolls = [random.randrange(1,7) for i in range(600)]
values, frequencies = np.unique(rolls, return_counts=True)
title = 'Title'
axes = sns.barplot(values, frequencies)

plt.show()

### seaborn relplot dataset ###

tips = sns.load_dataset("tips")
sns.relplot(data=tips, x="total_bill", y="tip", col="time", 
  hue="smoker", style="smoker", size="size",)

plt.show()

### matplotlib using pandas ###

titanic = pd.read_csv('https://vincentarelbundock.github.io/Rdatasets/csv/carData/TitanicSurvival.csv')

titanic.columns = ['name','survived','sex','age','class']
histogram = titanic.hist()

plt.show()
