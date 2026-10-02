# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

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
model.train()
print(model)
for i in range(1, 16):
    out = model(i)
    print(out)
