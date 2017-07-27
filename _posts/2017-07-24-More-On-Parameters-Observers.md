---
layout: post
title: More on parameters' observers
date: 2017-07-24 9:00
excerpt: More on parameters' observers
tags: [gsoc,shogun,toolbox,machine learning]
---

# More on parameters' observers

These last weeks, I've started implementing the feature I've realized on Shogun's
algorithms, so that they can be used in real life.
I've started by implementing a different series of parameters' observers
which will be used to retrieve information from algorithms, without serialize
them to files (like what it's done by Tensorboard). These parameters' observers
target the cross-validation algorithm.

## Cross-validation parameters' observers

The previous `CrossValidation` implementation used a series of custom listeners,
which could be added to the algorithm to watch over the execution. However, to
use these listeners, the code was bloated with many loops, which had also to be
guarded with `#pragma critical` calls during multi-threaded execution.

I've rebuilt Shogun's `CrossValidation` class to register and emit, for each run, all
folds partial results (the index used for training/test, evaluation result etc.), by
using the `observe()` method. I've coded two helper classes, `CrossValidationStorage`
and `CrossValidationFoldStorage`, which will allow us to do so.

The values emitted can then be caught by the new `ParameterObserverCV` class, which
will expose to the user an `std::vector` with all the measurements.

I've also ported the other `CrossValidation`'s listeners which were provided for
the previous implementation. Namely:
* `ParameterObserverCVMKL`: for storing MKL weights in every fold of cross-validation;
* `ParameterObserverCVMulticlass`: for storing multiclass evaluation information in every fold of cross-validation;

Here an example of a simple usage of the `ParameterObserverCV` class
(you can find the complete code at this [link](https://gist.github.com/geektoni/6b3bd3aafe70fbe477db485faa9cfe74)):
```c++
// We create the CrossValidation instance
CCrossValidation* cross=new CCrossValidation(machine, features, labels,
		splitting, eval_criterion);
cross->set_num_runs(100);

// Create the parameter's observer
// By setting false, we disable the observer verbosity
ParameterObserverCV par {false};
cross->subscribe_to_parameters(&par);

// We loops over the observations caught and
// we print the train indices used for each fold.
auto obs = par.get_observations();
for (auto o : obs)
{
    // For each of the observations folds we print the
    // train indices used.
    for (auto fold : o->get_folds_result()) {
	      f->get_train_indices().display_vector("Train indices ");
    }
}
```

## Pull Requests

* [[ParametersObservers] Update CrossValidation with parameters observers.](https://github.com/shogun-toolbox/shogun/pull/3953)
* [[ParametersObservers] Main refactor of the parameter's observers feature.](https://github.com/shogun-toolbox/shogun/pull/3939)
