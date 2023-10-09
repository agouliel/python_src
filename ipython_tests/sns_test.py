# ipython --matplotlib
# %run ./sns_test.py

import seaborn as sns
import numpy as np
import random

sns.set_theme()
tips = sns.load_dataset("tips")
sns.relplot(
  data=tips,
  x="total_bill", y="tip", col="time",
  hue="smoker", style="smoker", size="size",
)
rolls = [random.randrange(1,7) for i in range(600)]
values, frequencies = np.unique(rolls, return_counts=True)
#axes = sns.barplot(x=values, y=frequencies, palette='bright')
