import pybrain

from pybrain.tools.shortcuts import buildNetwork

net = buildNetwork(2, 3, 1)
print net
#net.activate([1, 1])

from pybrain.datasets import SupervisedDataSet
ds = SupervisedDataSet(2, 1)

ds.addSample((0, 0), (0,))
ds.addSample((0, 1), (1,))
ds.addSample((1, 0), (1,))
ds.addSample((1, 1), (0,))

from pybrain.supervised.trainers import BackpropTrainer
trainer = BackpropTrainer(net, ds)
trainer.train()
