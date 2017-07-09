---
layout: post
title: Keeping on Detoxing
date: 2017-06-26 9:00
excerpt: Second GSoC blog post
tags: [shogun, shogun-toolbox, gsoc, rxcpp, machine learning, algorithms]
---

# Keeping on Detoxing

Here it is my second GSoC blog post! You'll find some updates and insights about
the past two weeks.

## Some Smart Pointers... (Part II)

In the last post I talked about replacing Shogun custom macros for memory
management with brand-new smart pointers (aka `shogun::Some<T>`). Unfortunately,
my mentor and I had some trouble because of SWIG, the tool Shogun uses
to offer multi-language APIs.

The first problem we faced was that SWIG wasn't able to understand when a member
variable was just a `Some<>` instance and that it had to treat it like a
"simple" raw pointer (thanks to `operator->` overloading). SWIG allows this feature
(as specified [here](http://www.swig.org/Doc1.3/SWIGPlus.html#SWIGPlus_nn34)),
but we weren't able to call Some-wrapped object from the interfaces
(for instance, when using python, calling `a=GaussinaKernel(); a.get_parallel().set_num_thread(2)`
would result in an error).

To solve this issue, we discovered we would have needed to define `%template` directives for
each of the Shogun classes and override also their `operator *`, for instance:
```
%rename(GaussianKernelPtr) operator shogun::GaussianParallel*;
%include <shogun/base/some.h>

%template(SomeGaussian) shogun::Some<shogun::GaussianKernel>;
```

However, the idea was to make these smart pointers completely transparent for the
final user, if he is using one of our interfaces. For instance, if somebody uses Python
and instantiates a Shogun's object, that object will be Some-wrapped:

| Python Interface | Under-the-hood C++ representation |
|------|------|
| ```a = GaussianKernel() ``` | ```Some<GaussianKernel> a = some<GaussianKernel>() ``` |


To achieve that, one idea was to wrap the `some` helper method with SWIG and rename it
(specializing it for all Shogun's classes):
```
%rename(GaussianKernel) some<GaussianKernel>
```
but SWIG 3.0 doesn't support C++ variadic arguments
(see the [docs](http://www.swig.org/Doc3.0/CPlusPlus11.html#CPlusPlus11_variadic_templates)),
which are needed to make this solution work.


## Premature Stopping Algorithms

While fighting with SWIG limitations, I started working on the premature stopping task.
I implemented an architecture to permit stopping/pausing/resuming of Shogun's algorithms.
As suggested by my mentor, I used the [RxCpp](https://github.com/Reactive-Extensions/RxCpp)
library, which offers numerous tools to implement the observer pattern and to
do asynchronous programs.

I extended `CMachine` with three new protected overridable methods, called `on_next`,
`on_pause` and `on_complete`, which permit to define an additional behaviour when
the user decides to stop/pause/resume an algorithm.

Here a snippet from the new `CMachine.h` file showing these methods:
```c++
/** The action which will be done when the user decides to
* premature stop the CMachine execution */
virtual void on_next()
{
	m_cancel_computation.store(true);
}

/** The action which will be done when the user decides to
* pause the CMachine execution */
virtual void on_pause()
{
	m_pause_computation_flag.store(true);
	/* Here there should be the actual code*/
	resume_computation();
}

/** The action which will be done when the user decides to
* return to prompt and terminate the program execution */
virtual void on_complete()
{
}
```
I also implemented two public methods, namely `cancel_computation` and `pause_computation`,
that can be used to check if an algorithm execution has to be stopped or paused.
I've added also a macro which gathers these two checks together:
```c++
#define COMPUTATION_CONTROLLERS                                                
	if (cancel_computation())                                                  
		continue;                                                              
	pause_computation();
```

To show you how these new features can be used, here there is a [gist](https://gist.github.com/geektoni/1afd2daf69a813de64252a296997a8ea)
with a possible implementation and a possible terminal output, in the case a user decides
to premature stop the execution of an algorithm.


## Merged PRs

* [[PrematureStopping] Add CMake support to search or install RxCpp.](https://github.com/shogun-toolbox/shogun/pull/3845)
* [[PrematureStopping] Add RxCpp to the Docker image.](https://github.com/shogun-toolbox/shogun/pull/3855)
* [[PrematureStopping] Refactor CSignal class to use RxCpp utilities.](https://github.com/shogun-toolbox/shogun/pull/3848)
* [[PrematureStopping] Add to CMachine premature stopping methods.](https://github.com/shogun-toolbox/shogun/pull/3858)
