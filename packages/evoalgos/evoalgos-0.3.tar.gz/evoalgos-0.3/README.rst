
evoalgos has been tested with Python 2.7 and 3.4. The recommended version is
Python 3.x, because compatibility is reached by avoiding usage of xrange. So,
the code has a higher memory consumption under Python 2.

Everything in this package is pure Python. For a description of the contents
see DESCRIPTION.rst.


Changes
=======

0.3
---
* Added BinaryIndividual for optimization in binary search spaces.
* Added convenience classes CommaEA and PlusEA, which are special cases of
  EvolutionaryAlgorithm. By default, they are intended for single-objective
  optimization.

0.2
---
* Implemented the NSGA2b (NSGA2 with extensions).
* Fixed bug when individuals with identical objective values should be sorted
  by HyperVolumeContributionSorting (led to "unorderable types" exception
  under Python 3).
* Changed default setting for parameter "prefer_boundary_points" of SMSEMOA
  to True.

0.1
---
* Initial version containing the SMS-EMOA.
