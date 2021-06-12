# deep-piping
Inversion of Control ([IoC](https://en.wikipedia.org/wiki/Inversion_of_control)) / Dependency Injection ([DI](https://en.wikipedia.org/wiki/Dependency_injection)) - (not only) for Deep Learning

Paraphrasing Wikipedia - in traditional programming, the custom code that expresses the purpose of the program calls into reusable libraries to take care of generic tasks. In [IoC](https://en.wikipedia.org/wiki/Inversion_of_control), custom-written portions of a computer program receive the flow of control from a generic framework.

In the context of Deep Learning (DL) the IoC approach can be illustrated by libraries such as [mmdetection](https://github.com/open-mmlab/mmdetection/blob/master/configs/_base_/models/faster_rcnn_r50_fpn.py) or [Detectron2](https://github.com/facebookresearch/detectron2/blob/master/configs/COCO-Detection/faster_rcnn_R_50_FPN_1x.yaml).

The goal of _deep-piping_ is to provide an IoC/DI framework for DL independent of a particular machine learning task or algorithm. To this end, _deep-piping_ focuses on providing:

- the best possible syntax
- useful primitives such as:
  - flexible models and trainers
  - dataset transformers
  - data access objects
- automatic command line interface for all experiments
- a well-defined and sensible multiple inheritance mechanism able to merge repeated keys

The syntax supported by _deep-piping_ is a slightly abused YAML notation where [unquoted strings](https://yaml.org/spec/1.2/spec.html#style/flow/plain) are evaluated as Python expressions. On top of that, _deep-piping_ supports autoimporting of Python modules. These capacities combined allow for a clean and concise style demonstrated in the following example:

```yaml
arguments:
  learning_rate:
    type: float
    default: 0.001

dl_model:
  class: torch.nn.Sequential
  0:
    class: torch.nn.Linear
    in_features: 32
    out_features: 64
  1:
    class: torch.nn.ReLU
  2:
    class: torch.nn.Linear
    in_features: 64
    out_features: 2
    
dataset:
  class: my_custom.Dataset
  
opt:
  class: torch.optimizer.AdamW
  parameters: dl_model.parameters()
  learning_rate: args.learning_rate
    
model:
  class: deep_piping.lightning.LitFlexibleClassifier
  dl_model: dl_model
  dataset: dataset
  optimizer: opt
  
logger:
  class: pytorch_lightning.loggers.MLFlowLogger
   
trainer:
  class: pytorch_lightning.Trainer
  model: model
  logger: logger
  max_epochs: 50
  callbacks:
    - class: pytorch_lightning.callbacks.EarlyStopping
      monitor: "val_loss"
```

Assuming that the above code is saved in a file named _example.yaml_, ideally it should just be runnable via the following command line:

```bash
python ./script/train.py example.yaml --learning-rate 2e-5
```

Although the [example/](https://github.com/sadaszewski/deep-piping/tree/master/example) section is still very much a work in progress, you can take a peek there to get a better idea about the capacities of the framework. Stay tuned for more news and training materials. Hope you find _deep-piping_ useful.
