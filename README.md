<h1 align="center">
  <br>
  <a href="https://vantage6.ai"><img src="https://github.com/IKNL/guidelines/blob/master/resources/logos/vantage6.png?raw=true" alt="vantage6" width="400"></a>
</h1>

<h3 align=center> A privacy preserving federated learning solution</h3>

--------------------


# What's this?

This is a simple example of an algortihm using R and python. The goal is to demo a few ways of interacting with R within a vantage6 algorithm. This is a (workaround) stepping stone to (hopefully) future versions of vantage6-algorithm-tools, where running R code will be better supported.

It's based on the example [average algorithm available here](https://github.com/IKNL/v6-average-py).

# :warning: Proof of concept. Use with care! :warning:

Vantage6 in recent versions has somewhat deprecated support for R scripts. This
repository is *not* indented to show a production-ready replacement of that
support. Merely a starting point to work towards some way of running R scripts
again in vantage6.

Albeit these workarounds do work, you must be careful when trying to implement
something similar in your algorithm. Taking care of vetting user input, etc.

Also note that some features (like using multiple datasets concurrently) would
be unsupported in this simple proof-of-concept code.


## Two methods

TODO: Explain work around here

------------------------------------
> [vantage6](https://vantage6.ai)
