---
layout: post
title: First GSoC Weeks!
date: 2017-06-12 9:00
excerpt: First blog post!
tags: [gsoc, shogun, shogn-toolbox, c++, progress bar, github, machine learning]
---
# First GSoC Weeks!

Here we are! The first amazing and intense GSoC weeks for the [Shogun Toolbox Organization](http://www.shogun-toolbox.org/)
are ended and my first GSoC blog post is here!

## Majestic Progress Bars
My first objective was to implement and create a new progress bar which would substitute the old macro ```SG_PROGRESS```, which was used to display elapsed time of algorithm's execution.
The new progress is a simple header only file and it was made to work with single or multi-threaded application (e.g within OpenMP's `#pragma`). It is also compliant with Windows terminals.

Here below some use cases:
```c++
// Create a progress bar object
auto pb = progress(range(0,10));

// Main Loop
for (int i=0; i<10; i++)
{
    // Magic stuff
    pb.print_progress();
}
pb.complete();
```
```c++
// It can be used also with the new range-based for loop
// introduced with C++11 standard.
for (auto i: progress(range(0, 10)))
{
    // Revolutionary code
}
```
Moreover, you can do also much complex things by exploiting the power of lambda expressions!
Let's say you have a complex `for` loop with custom endings conditions. With `progress`, you can write it easily this way:
```c++
int condition=1;
for (auto i : progress(
    range(0, 10),
    UTF8,
    "Prefix:",
    [&]{ return condition < 5;})
)
{
     // This will stop when condition >= 5;
}
```

If you arrived here, it means you're really interested in what I'm saying. Great! You earned a gif!

| ![progress]({{ site.url }}/assets/img/progress_bar.gif) |

## Some Smart Pointers...

The second task I started was focused on replace the `SG_REF` and `SG_REF` macros used all over Shogun codebase to do memory management with the Shogun's custom smart pointer `Some`.  

In contrast with standard memory management (provided by STL instrument like `std::shared_ptr`, `std::unique_ptr`),
in which the reference counter is stored outside the object, each of Shogun's classes maintain its personal counter.

There are two methods, called `ref()` and `unref()`, which take care of incrementing/decrementing the object referece counter. These methods are called by `SG_REF`/`SG_UNREF` macros.
```c++
CGaussianKernel k = new CGaussianKernel()
SG_REF(k);      // We increase k's counter
// We do something with the kernel
SG_UNREF(k);    // We decrease k's reference counter and if it is
                // less than 0, k will be deleted
```
Of course this is not an easy way to deal with memory management. I can assure you that placing one of these macros in the wrong place will surely lead to errors and unexpected result (which can become REALLY hard to fix).

With the `Some` pointer, things will become easier for the developers. `Some` will take care of memory management, by decreasing the reference counter (and deleting the object) when it is not used anymore (e.g when it goes out of scope).
```c++
Some<CGaussianKernel> k = some<CGaussianKernel>();
// Boom. Memory management done.
// When k will go out of scope, the Some destructor
// will free the memory occupied.
```

## Merged PRs

* [Add PRange class to replace old SG_PROGRESS (WIP)](https://github.com/shogun-toolbox/shogun/pull/3745)
* [[ProgressBar] Add multi threaded progress bar.](https://github.com/shogun-toolbox/shogun/pull/3828)
* [[ProgressBar] Add a boolean flag to the progress bar.](https://github.com/shogun-toolbox/shogun/pull/3829)
* [[ProgressBar] Refactor the progress bar code and add documentation.](https://github.com/shogun-toolbox/shogun/pull/3831)
* [[ProgressBar] Replace SG_PROGRESS with the new progress bar.](https://github.com/shogun-toolbox/shogun/pull/3836)
