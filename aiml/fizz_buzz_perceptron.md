# Pytorching Fizz Buzz

The Astoria Tech meetup does 5 minute lightning rounds every month. I really don't have anything to present so I came up with this dumb thing so that I could have something to present next month to practice public speaking. Enjoy!


## Academic Background

With the recent AI hype the past few years it's often easy to forget that some of the techniques we use in AI/ML go way back to the 50's and 60's.

Take the perception for example, one of the simplest types of nueral networks. The concept of a "neuron" and "network" was formed in 1943 with actual simulations happening by the late 50's. ([source](https://en.wikipedia.org/wiki/Perceptron)).

## A Single Layer Network

Deep diving into the architecture of specific neuron in a neural network, we can simplfy the architecture to:

```
x_1 \
     \
      \  
        \    _ _ __ _ _ _ _ 
...         |               |
            |     f         | - - - - > output
            | _ _ __ _ _ _ _|
           /
        / 
       /
x_n 
```

Where x are inputs and typically the black box involves a fancy function ( e.g sigmoid ).

However, it recently occured to me though this function could probably be implemented to be any find of function.

So could we then just have one element as an input and then implement f to be simply fizz buzz?

```
         -----------
x ----> | fizz_buzz |   - - - - - > output 
         -----------
```

## Torching the Buzz

### Quick Review of Fizz Buzz

Leet code defines fizzbuzz problem as the following:

```
Given an integer n, return a string array answer (1-indexed) where:
answer[i] == "FizzBuzz" if i is divisible by 3 and 5.
answer[i] == "Fizz" if i is divisible by 3.
answer[i] == "Buzz" if i is divisible by 5.
answer[i] == i (as a string) if none of the above conditions are true.
```

Gemini which refuses shut the fuck up and insists on giving me AI anwers to every google search I do, kindly drained water from Lake Tahoe to provide the following solution for fizz buzz in Python.

```
for i in range(1, 101):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
```

### Pytorch

My implementation can be found at `fizz_buzz_torch.py` but it's small enough to copy-paste here.

```{python}

import torch

class FizzBuzzPerceptron(torch.nn.Module):
    def __init__(self):
        super(FizzBuzzPerceptron, self).__init__()

    def _fizz_buzz(self, i):
        if i % 3 == 0 and i % 5 == 0:
            return "FizzBuzz"
        elif i % 3 == 0:
            return "Fizz"
        elif i % 5 == 0:
            return "Buzz"
        else:
            return i

    def forward(self, x):
        return self._fizz_buzz(x)

model = FizzBuzzPerceptron()
print(model)
for i in range(1, 16):
    out = model(i)
    print(out)

```

And running the code produces:
```
$ python fizz_buzz_torch.py 
FizzBuzzPerceptron()
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
```

# Notes & Observations

* There's no back propogation in this, so this is just a really dumb feed forward network.
* `torch.nn.Module` can turn a python class into a pytorch neural net.
* For the constructor I've noticed that you need to call `super` to instatiate torch configuration. For some reason I see two ways:
```
super().__init__()
super(SimpleModel, self).__init__()
```
I'm blanking if there's a difference in behavior between the two.

* I later added a `model.train()` line but nothing changed. I need to learn more on what this function does.

# Why?
I wanted to learn how to use the pytorch library. While this isn't really machine learning or AI in anyway it was actually not a bad hello world for getting something setup.

# Links
I tried as hard to not use AI and instead find links to base my answers off of.
The following where the links I used for references.

https://docs.pytorch.org/tutorials/beginner/blitz/neural_networks_tutorial.html

https://www.kaggle.com/code/ignazio/single-neuron-network-in-pytorch

https://machinelearningmastery.com/building-a-single-layer-neural-network-in-pytorch/


# Future
* Learn to implement an actual basic nueral network with backprop.