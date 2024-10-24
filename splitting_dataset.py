import pandas as pd

# loading data 
df = pd.read_csv("disease_diagnosis.csv")

print(df.shape[0])

# randomnly splitting 80% of dataset into train and 20% to prediction set
train_data_set = df.sample(frac  = 0.8)
prediction_data =  df.drop(train_data_set.index)

# making them csv files
train_data_set.to_csv("training_set.csv", index=False)
prediction_data.to_csv("prediction_set.csv", index=False)