# https://twitter.com/driscollis/status/1466030253697077248

import pandas as pd

df = pd.read_json("https://api.github.com/users/driscollis/repos?perpage=100")
columns = ["name", "stargazers_count", "forks"]

# Get the top 10 repos sorted by stargazer count
print(df[columns].sort_values("stargazers_count", ascending=False).head(10))
