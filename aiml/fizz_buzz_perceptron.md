# Pytorching Fizz Buzz

The Astoria Tech meetup does 5 minute lightning rounds every month. I really don't have anything to present so I came up with this dumb thing so that I could have something to present next month to practice public speaking. Enjoy!


## Academic Background

With the recent AI hype the past few years it's often easy to forget that some of the techniques we use in AI/ML go way back to the 50's and 60's.

Take the perception for example, one of the simplest types of nueral networks. The concept of a "neuron" and "network" was formed in 1943 with actual simulations happening by the late 50's. ([source](https://en.wikipedia.org/wiki/Perceptron)).

## A Single Layer Network

Deep diving into the architecture of specific neuron in a neural network, we can simplfy the architecture to:

```
x_0 \
     \
      \ w_1 
        \    _ _ __ _ _ _ _ 
...         |               |
            |     f         | - - - - > output
            | _ _ __ _ _ _ _|
           /
         / w_n
        /
x_n 
```

Basically take your inputs x_0 to x_n, multiply them by a weights w_0 to w_n and put them in a fancy function. Or as wikipedia writes in vector notation:

f(x) = h ( w * x + b).

( b is just a small bias factor. I'm going to ignore it for now. )
[source](https://en.wikipedia.org/wiki/Perceptron)

The fancy function inside that box I drew is usually a function like sigmoid.

However, it recently occured to me though this function could probably be implemented to be any find of function I want in practice.

So then I had the dumb idea what if we:

1. Limit all x to be just one input of a single number.
2. Set the corresponding weight for this one input to just be 1.
3. Make f just be an implementation of fizzbuzz.

Could I then implement fizz buzz in pytorch?


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

Gemini which gives me AI anwers to every google search I do, kindly drained water from Lake Tahoe to provide the following solution for fizz buzz in Python.

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

  3 import torch
  4 from torch import tensor
  5 
  6 class FizzBuzzPerceptron(torch.nn.Module):
  7     def __init__(self):
  8         super(FizzBuzzPerceptron, self).__init__()
  9 
 10     def _fizz_buzz(self, i):
 11         if i % 3 == tensor([0]) and i % 5 == tensor([0]):
 12             return "FizzBuzz"
 13         elif i % 3 == tensor([0]):
 14             return "Fizz"
 15         elif i % 5 == tensor([0]):
 16             return "Buzz"
 17         else:
 18             return i
 19 
 20     def forward(self, x):
 21         w = tensor(1)
 22         return self._fizz_buzz(x * w)
 23 
 24 model = FizzBuzzPerceptron()
 25 model.train()
 26 print(model)
 27 for i in range(1, 16):
 28     out = model(tensor(i))
 29     print(out)

```

And running the code produces:
```
$ python fizz_buzz_torch.py 
FizzBuzzPerceptron()
tensor(1)
tensor(2)
Fizz
tensor(4)
Buzz
Fizz
tensor(7)
tensor(8)
Fizz
Buzz
tensor(11)
Fizz
tensor(13)
tensor(14)
FizzBuzz

```

# Notes & Observations

* There's no back propogation in this, so this is just a really dumb feed forward network.
* `torch.nn.Module` can turn a python class into a pytorch neural net.
* `model(i)` implicitly calls `forward`. This is probably how in the real world you would use your model to produce predictions.
* For the constructor I've noticed that you need to call `super` to instatiate torch configuration. For some reason I see two ways:
```
super().__init__()
super(SimpleModel, self).__init__()
```                       
I'm blanking if there's a difference in behavior between the two.

* torch.tensor(i) could have just been an `int` I just wanted to try playing around with tensors. 
TODO: whats the difference between a*b, a@b and torch.matmul?

* I later added a `model.train()` line but nothing changed. I need to learn more on what this function does.

# Why?
* I wanted to learn how to use the pytorch library. While this isn't really machine learning or AI in anyway it was actually not a bad hello world for getting something setup.

* I often find myself overwhelemed when trying to learn machine learning. This example reminds me that the libraries themseleves need not be scary and there's always a simple place to start.

# Links
I tried as hard to not use AI and instead find links to base my answers off of.
The following where the links I used for references.

https://docs.pytorch.org/tutorials/beginner/blitz/neural_networks_tutorial.html

https://www.kaggle.com/code/ignazio/single-neuron-network-in-pytorch

https://machinelearningmastery.com/building-a-single-layer-neural-network-in-pytorch/


# Future
* Learn to implement an actual basic nueral network with backprop.