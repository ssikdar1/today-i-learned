# Introduction

I recently rediscovered a final paper for a Soft Computing class (ISE 419) I took in the Industrial and Systems Engineering school at SUNY Binghamton. Graduating as a mathematics major in the midst of the recession was a time uncertain of job prospects. As a result I took a bunch of software and engineering classes with the hope I would be able to tie my math education to something more tangible.

Then my programming knowledge was limited to introductory Python and Java. I belive this was the first time I tried to take something that was presented mathematically in class and try to actually implement it in actual code. At this point it hadn't occured to me that you could use libraries for coding projects so I implemented everything with just raw python lists. I don't seem to have the actual code anymore but I pasted portions of the code in the final write up  (proabably to make the paper seem longer).

The paper was titled "Feed Forward Back Propogation Neural Network" ( nowadays we would just call that a normal nueral network I think). It used a dataset on entries of wildfires in Portugal ([link](https://archive.ics.uci.edu/dataset/162/forest+fires)). 
The task was given 12 Integer, Categorical and Continuous variables, predict the amount of forest burned in that fire.

## Task

In a previous post I used pytorch to implement [fizz buzz](fizz_buzz_perceptron.md). 
That was useful in showing some of the basic module class and methods, but it didn't really do much. 
This time around I thought it would be interesting to retry my final paper by implementing it in pytorch.

This will involve both feed forawrd and backpropgation elements as well as feature engineering.

The final code I ended up using is at [forest_fire.py](forest_fire.py).

## Feature Engineering

Before doing anything pytorch or neural network related, I wanted to quickly use pandas to investigate the dataset and then from there do some feature engineering.

```{Python}
import pandas as pd

df = pd.read_csv("forestfires.csv")

>>> df
     X  Y month  day  FFMC    DMC     DC   ISI  temp  RH  wind  rain   area
0    7  5   mar  fri  86.2   26.2   94.3   5.1   8.2  51   6.7   0.0   0.00
1    7  4   oct  tue  90.6   35.4  669.1   6.7  18.0  33   0.9   0.0   0.00
2    7  4   oct  sat  90.6   43.7  686.9   6.7  14.6  33   1.3   0.0   0.00
3    8  6   mar  fri  91.7   33.3   77.5   9.0   8.3  97   4.0   0.2   0.00
4    8  6   mar  sun  89.3   51.3  102.2   9.6  11.4  99   1.8   0.0   0.00
..  .. ..   ...  ...   ...    ...    ...   ...   ...  ..   ...   ...    ...
512  4  3   aug  sun  81.6   56.7  665.6   1.9  27.8  32   2.7   0.0   6.44
513  2  4   aug  sun  81.6   56.7  665.6   1.9  21.9  71   5.8   0.0  54.29
514  7  4   aug  sun  81.6   56.7  665.6   1.9  21.2  70   6.7   0.0  11.16
515  1  4   aug  sat  94.4  146.0  614.7  11.3  25.6  42   4.0   0.0   0.00
516  6  3   nov  tue  79.5    3.0  106.7   1.1  11.8  31   4.5   0.0   0.00

[517 rows x 13 columns]
```

At a first glance we can convert month and day into numeric values.

```
from datetime import datetime
df["month"] = df["month"].apply(lambda mon_str: datetime.strptime(mon_str, "%b").month)
days = {"sun": 0, "mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5, "sat": 6}
df["day"] = df["day"].apply(lambda day_str: days[day_str])
```

Next I want to use the X,Y coordinates in some way. I asked Claude for some advice, it gave some useful suggestions such as different one hot encoding and in and grouping. However it also wrote:

```
The simplest approach is to treat X and Y as continuous and normalize them, either min-max to [0, 1] or standardize to zero mean and unit variance. Neural networks train much better with scaled inputs, so you should do this regardless of which other techniques you add.

The downside is that the network has to learn any non-linear spatial patterns (e.g., “fires in the northeast corner behave differently”) on its own, which is hard with only 517 rows.
```

Well simple is good, and with so few datapoints no one technique outshines the other. So we can go with this for now.

### Normalizing
Also this is a good segway to the topic of normalizing. In my paper I did seem to know that here are benefits to normalizing the data in the pre-procesing phase. 

In my paper I seemd to have done min-max normalization, there I wrote:

```
One of the most popular techniques to pre-process the data is known as data normalization. This is a method which scales all the data between whatever range you need. Data normalization is given by the formula:

I = Imin + (Imax-Imin)*(D-Dmin)/(Dmax-Dmin)  (Mendelsohn)
```

However looking at the summary of the dataframe some of the variables have large ranges of potential values. 

```
>>> df.describe()
                X           Y       month         day        FFMC         DMC          DC         ISI        temp          RH        wind        rain         area
count  517.000000  517.000000  517.000000  517.000000  517.000000  517.000000  517.000000  517.000000  517.000000  517.000000  517.000000  517.000000   517.000000
mean     4.669246    4.299807    7.475822    2.972921   90.644681  110.872340  547.940039    9.021663   18.889168   44.288201    4.017602    0.021663    12.847292
std      2.313778    1.229900    2.275990    2.143867    5.520111   64.046482  248.066192    4.559477    5.806625   16.317469    1.791653    0.295959    63.655818
min      1.000000    2.000000    1.000000    0.000000   18.700000    1.100000    7.900000    0.000000    2.200000   15.000000    0.400000    0.000000     0.000000
25%      3.000000    4.000000    7.000000    1.000000   90.200000   68.600000  437.700000    6.500000   15.500000   33.000000    2.700000    0.000000     0.000000
50%      4.000000    4.000000    8.000000    3.000000   91.600000  108.300000  664.200000    8.400000   19.300000   42.000000    4.000000    0.000000     0.520000
75%      7.000000    5.000000    9.000000    5.000000   92.900000  142.400000  713.900000   10.800000   22.800000   53.000000    4.900000    0.000000     6.570000
max      9.000000    9.000000   12.000000    6.000000   96.200000  291.300000  860.600000   56.100000   33.300000  100.000000    9.400000    6.400000  1090.840000
```

Since min-max normalization can be sensative to such large ranges, for this time around I will use zscale for all columns instead. 
If I was more serious I would probably play around with choosing specific techniques for each coulmn.


```
from scipy.stats import zscore

# dont apply zscore to areaa
zscore_target_cols = df.columns.difference(["area"])
df[zscore_target_cols] = df[zscore_target_cols].apply(zscore)
```


## Implementing the Neural Network

Back in 2012 I clearly had no idea how to feature engineer and build a complex network because my impelementation only had the following:

```
NI = 3                            #Number of Input Nodes
NH = 2                          #Number of Hidden Nodes
NO = 1                          #Number of Output Nodes
```

For this time around I wanted to see if I could implement something a little more complex. Using some of the pytorch tutorials I came up with a network with 12 input nodes and two hidden layers of size 32 and 16 nodes respectively.

```
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
```

# Training and Testing

While blogging about implementing fizz buzz in pytorch I had mentioned it wasn't enough to get a feel for how `train`, `eval` and backpropogation worked. This time by using some code found on Kaggle and getting some suggestions from claude I was able to implement a training phase with backprop followed by doing some validation:

```

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
```

# Results
So in the end how did I do? At first I was experiencing horrible test loss and extensive overfitting. Eventually I was finally able to get the results to the following:

```
$ python forest_fire.py 
Epoch 50/500, Train Loss: 2.0253, Test Loss: 1.9857
Epoch 100/500, Train Loss: 1.8441, Test Loss: 1.8931
Epoch 150/500, Train Loss: 1.7623, Test Loss: 1.8563
Epoch 200/500, Train Loss: 1.6715, Test Loss: 1.8329
Epoch 250/500, Train Loss: 1.5601, Test Loss: 1.8537
Epoch 300/500, Train Loss: 1.4449, Test Loss: 1.9068
Epoch 350/500, Train Loss: 1.3193, Test Loss: 1.9883
Epoch 400/500, Train Loss: 1.1671, Test Loss: 2.1044
Epoch 450/500, Train Loss: 1.0257, Test Loss: 2.2726
Epoch 500/500, Train Loss: 0.8852, Test Loss: 2.4668
```

Which I don't think is too bad. I tried to see how I did way back in 2012 but apparently I never actually posted my results.

# Conclusion

In conclusion we know have an actual network attempting to do prediction! The network has some complexity with some hidden layers and I've dipped my toes into the area of feature engineering. 

# Next steps

* Implement a larger network. Maybe a deep learning network, reccurant network, or transformer?
* Try building a more useful model in some area such as speech, image, or natural language.

* Learn more aout weight decay.
* Try one hot encoding.
* Better way to implement zcore normalization?



# Links
https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html
https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html

https://theaveragecoder.medium.com/training-and-testing-a-basic-neural-network-using-pytorch-4010300fda45

https://www.kaggle.com/code/mohitchaitanya/simple-iris-dataset-classification-using-pytorch


# AI Disclaimer

I'm always trying to be mindful of disclosing when I've used AI. 

While I tried to do as much on my own as possible I did use AI for the following:

* Asked Claude on advice on how to treat the spatial coordinates.
* Asked AI on how to apply zscore on columns except for target column

* The code I had based my solution from was doing a classification answer. Claude caught the mistake.

```
1. Wrong loss for this task. The target area is a continuous value (burned hectares), so this is regression. CrossEntropyLoss is for classification with class indices, and with output_dimensions = 1 it would be meaningless anyway. Use nn.MSELoss() (or nn.L1Loss() / nn.HuberLoss()).
```

And also had given me tips on model.eval and torch.no_grad:

```
model.train() is fine, but you should call model.eval() and use torch.no_grad() when computing the test loss.
```

* Alerted me that I should have feature engineered the output target variable as well.

```
3. area is extremely skewed. Many rows are 0 and a few are huge. The standard approach for this dataset is to transform the target, e.g. y = np.log1p(df["area"]), and train on that. Otherwise a handful of big fires dominate the loss.
```
