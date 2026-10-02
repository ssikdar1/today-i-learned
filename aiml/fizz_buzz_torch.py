# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import torch
from torch import tensor

class FizzBuzzPerceptron(torch.nn.Module):
    def __init__(self):
        super(FizzBuzzPerceptron, self).__init__()

    def _fizz_buzz(self, i):
        if i % 3 == tensor([0]) and i % 5 == tensor([0]):
            return "FizzBuzz"
        elif i % 3 == tensor([0]):
            return "Fizz"
        elif i % 5 == tensor([0]):
            return "Buzz"
        else:
            return i

    def forward(self, x):
        w = tensor(1)
        return self._fizz_buzz(x * w)

model = FizzBuzzPerceptron()
model.train()
print(model)
for i in range(1, 16):
    out = model(tensor(i))
    print(out)
