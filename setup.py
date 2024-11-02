import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report

# Read the parsed data from csv
data = pd.read_csv("/Hadoop/newlog.csv")

# Combine Date and Time into a single datetime column
data['date'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], format="%Y-%m-%d %H:%M:%S")
data = data.drop(['Date', 'Time'], axis=1)

# Drop rows with NA in the Response column
data = data[~data['Response'].str.contains("#N/A")]

# Unique values in Response column
print(data['Response'].unique())

# Grouping data (you can further customize this if you need a specific grouping)
gdata = data.groupby(['date', 'Block_ID', 'PID', 'Response']).size().reset_index(name='count')

# Factorize Response variable (Normal = 0, Anomaly = 1)
gdata['Response'] = gdata['Response'].apply(lambda x: 0 if x == "Normal" else 1)

# Split data into training and testing sets (70-30 split)
gdata_train, gdata_test = train_test_split(gdata, test_size=0.3, random_state=42)
Response_test = gdata_test['Response']
gdata_test = gdata_test.drop(columns=['Response'])

# Fit RandomForest model
rf = RandomForestClassifier(n_estimators=100, max_features=3, random_state=42)
rf.fit(gdata_train.drop(columns=['Response']), gdata_train['Response'])

# Print training error and accuracy
train_predictions = rf.predict(gdata_train.drop(columns=['Response']))
train_accuracy = np.mean(train_predictions == gdata_train['Response'])
print(f"The training prediction error is: {1 - train_accuracy}")
print("Confusion matrix for training model:")
print(confusion_matrix(gdata_train['Response'], train_predictions))

# Predict the response variable for the test set
pred = rf.predict(gdata_test)

# Print confusion matrix for test set
print("Confusion matrix for the test set:")
print(confusion_matrix(Response_test, pred))

# Feature importance
feature_importance = rf.feature_importances_
print("Feature importance:", feature_importance)

# Drop less important columns if needed
# Adjust columns based on actual data and feature importance results
data2 = gdata.drop(columns=['root', 'succeeded'], errors='ignore')

# Split data2 into training and testing sets
data2_train, data2_test = train_test_split(data2, test_size=0.3, random_state=42)
Response2_test = data2_test['Response']
data2_test = data2_test.drop(columns=['Response'])

# Fit another RandomForest model on data2
rf2 = RandomForestClassifier(n_estimators=100, max_features=3, random_state=42)
rf2.fit(data2_train.drop(columns=['Response']), data2_train['Response'])

# Predictions for data2 test set
pred2 = rf2.predict(data2_test)

# Print training error and accuracy for data2 model
train_predictions2 = rf2.predict(data2_train.drop(columns=['Response']))
train_accuracy2 = np.mean(train_predictions2 == data2_train['Response'])
print(f"The training prediction error is: {1 - train_accuracy2}")
print("Confusion matrix for training model:")
print(confusion_matrix(data2_train['Response'], train_predictions2))

# Confusion matrix for data2 test set
print("Confusion matrix for the test set:")
print(confusion_matrix(Response2_test, pred2))
