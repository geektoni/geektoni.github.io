---
layout: post
title: Shogun + Tensorboard = &#10084
date: 2017-07-10 9:00
excerpt: Some fun with data visualization
tags: [gsoc,tensorboard,tensorflow,shogun,toolbox,data visualization]
---

# Shogun + Tensorboard = &#10084;

In the last post I talked about the premature stopping features I implemented
for enhancing Shogun's algorithms. To achieve that objective, I've used the fantastic RxCpp framework,
which can be used to easily build dynamic applications. That framework has come handy for other exciting purposes, in fact,
today I'll talk about monitoring algorithm's parameter values.

## Observable Parameters

During these weeks I spent some time building another architecture, based on
RxCpp, that will permit to observe the evolution of algorithm's parameters.
For instance, we would like to monitor how the weights of a LARS algorithm change
during the model training.

I've implemented a series of new observables object. These will emit values
which contain a parameter observation. Since these measurements can theoretically
be done on various objects (like vectors, primitive types or other,) these
observable emits `Any` wrapped objects. This means that these parameter's
observable are type-agnostic.

The new observable signature is the following:
```c++
rxcpp::observable<std::pair<int64_t, std::pair<string, Any>>>
```
We can notice how this observable emits an `std::pair`, which consists of an
`int64_t`, that is the measurement's number and of another `std::pair`, which contains
a `string` value (the parameter name), and an `Any` value which stores the measured value at that instant.

To measure and emit a parameter's value, I've added a new method to the `CSGObject` class:
```c++
void observe_scalar(const int64_t step, const std::string& name, const Any& value);
```
This method can be used by the algorithm's developers to emit parameter's values
at regular intervals (for instance, every loop's iterations).

The observers of these observable are derived from an interface called
`ParameterObserverInterface`. This interface implements
only the basic methods and it doesn't specify how the data will be used/written to a file.  

## Tensorboard

The only parameter observers that are currently implemented into Shogun's codebase
are the ones which take the measurements and print them into a file, which
can be later given to [Tensorboard](https://www.tensorflow.org/get_started/summaries_and_tensorboard).   

Tensorboard is a tool provided by [Tensorflow](https://www.tensorflow.org/) which provide beautiful data visualization
and it is mostly used for neural networks. It works by reading files which contain summary data,
generated when running Tensorflow. It supports many data visualizations (scalars, histogram, images etc.).
Currently, Shogun supports only scalar and histogram ones (the other maybe will be added in
the future. Who knows).

My mentor [Viktor](https://github.com/vigsterkr/) built (aka carved out from Tensorflow codebase) an amazing C++ library called
[TFLogger](https://github.com/shogun-toolbox/tflogger) which can serialize the `tensorflow::Event`
objects to files. It enables us to generate our custom `Event` instances and files from Shogun,
which can be easily read from Tensorboard.

## Code Example

[Here](https://gist.github.com/geektoni/c3e2b3802ca5910737c6dd68665c1fb5) you can find some
code samples which shows how to use the ParameterObservers (scalar and histogram case) to record
the weights of a LARS model.


## Merged Pull Requests

*  [[ShogunBoard] Add parameter observable and observe_param() method.](https://github.com/shogun-toolbox/shogun/pull/3877)  
