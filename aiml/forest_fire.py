import numpy as np
import pandas as pd
import torch
import torch.nn as nn


from datetime import datetime
from scipy.stats import zscore
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


df = pd.read_csv("/home/shan/Downloads/forest+fires/forestfires.csv")

df["month"] = df["month"].apply(lambda mon_str: datetime.strptime(mon_str, "%b").month)
days = {"sun": 0, "mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5, "sat": 6}
df["day"] = df["day"].apply(lambda day_str: days[day_str])

zscore_target_cols = df.columns.difference(["area"])
df[zscore_target_cols] = df[zscore_target_cols].apply(zscore)

X = df.drop(["area"],axis=1).values
y = np.log1p(df["area"].values)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

X_train = torch.FloatTensor(X_train)
X_test = torch.FloatTensor(X_test)
y_train = torch.FloatTensor(y_train).unsqueeze(1)
y_test = torch.FloatTensor(y_test).unsqueeze(1)

input_dimensions = X.shape[1]
output_dimensions = 1

class NeuralNetwork(nn.Module):
    def __init__(self, input_dimensions, output_dimensions):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(input_dimensions, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, output_dimensions),
        )

    def forward(self, x):
        x = self.flatten(x)
        out = self.linear_relu_stack(x)
        return out


model = NeuralNetwork(input_dimensions, output_dimensions)

# creating our optimizer and loss function object
learning_rate = 1e-3
weight_decay = 1e-3
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(list(model.parameters()),lr=learning_rate, weight_decay=weight_decay)

model.train()


def train_network(model,optimizer,criterion,X_train,y_train,X_test,y_test,num_epochs,train_losses,test_losses):
    for epoch in range(num_epochs):
        #clear out the gradients from the last step loss.backward()
        optimizer.zero_grad()
        
        #forward feed
        output_train = model(X_train)

        #calculate the loss
        loss_train = criterion(output_train, y_train)
        
        #backward propagation: calculate gradients
        loss_train.backward()

        #update the weights
        optimizer.step()

        
        output_test = model(X_test)
        loss_test = criterion(output_test,y_test)

        model.eval()
        with torch.no_grad():
            output_test = model(X_test)
            loss_test = criterion(output_test, y_test)
        model.train()

        if (epoch + 1) % 50 == 0:
            print(f"Epoch {epoch+1}/{num_epochs}, Train Loss: {loss_train.item():.4f}, Test Loss: {loss_test.item():.4f}")

num_epochs = 500
train_losses = np.zeros(num_epochs)
test_losses  = np.zeros(num_epochs)

train_network(model,optimizer,criterion,X_train,y_train,X_test,y_test,num_epochs,train_losses,test_losses)

plt.figure(figsize=(10,10))
plt.plot(train_losses, label='train loss')
plt.plot(test_losses, label='test loss')
plt.legend()
plt.show()