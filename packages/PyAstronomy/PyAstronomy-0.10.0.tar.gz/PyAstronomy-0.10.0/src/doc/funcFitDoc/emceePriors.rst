.. _emceePriors:

Ready-to-use priors for emcee sampling
==========================================

.. currentmodule:: PyAstronomy.funcFit
.. autoclass:: FuFPrior
   :members:
  
Example: Instantiating a prior
----------------------------------

::

  from PyAstronomy import funcFit as fuf
  
  # Instantiate prior
  gp = fuf.FuFPrior("gaussian", sig=0.1, mu=1.0)
  
  # Current values (arbitrary)
  cvals = {"a":1.4, "b":0.86, "c":1.1}
  
  # Get log(prior) for parameter "b"
  print gp(cvals, "b")
