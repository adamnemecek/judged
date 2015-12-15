JudgeD: Probabilistic Datalog
=============================

_You are on the montecarlo branch: this branch is the Monte Carlo version of
JudgeD. You can switch to either the `exact` or `master` branches for a
probabilistic and deterministic variant, respectively.._

JudgeD is a proof-of-concept implementation of a probabilistic variant of
[Datalog](https://en.wikipedia.org/wiki/Datalog). JudgeD is available under the
MIT license.

JudgeD requires [Python 3.4](https://www.python.org/) or newer.


Quick Start
-----------

  1. Clone this repository
  2. Switch to the `montecarlo` or `exact` branch
  3. Have a look at the examples in `examples/`, or play with the interactive
     interpreter: `./datalog.py`


Variants
--------

The JudgeD repository currently has three branches: `master`, `exact` and
`montecarlo`.

The `master` branch is the deterministic basis of JudgeD. It is an SLDNF based
implementation of Datalog with negation in Python.

The `exact` and `montecarlo` branches are two proof-of-concept implementations
of probabilistic datalog. The `exact` version does not (yet) calculate
probabilities but determines the exact sentence describing the validity of the
answers. The `montecarlo` version calculate answer probabilities through Monte
Carlo simulation fo multiple answering runs.


Syntax
------

The syntax of JudgeD program closely resembles traditional datalog, with the
addition of the descriptive sentences. Additionally, the probabilities attached
to the labels are included in the syntax. An example of a simple coin-flip
would be:

    heads(c1) [x=1].
    tails(c1) [x=2].
    
    @P(x=1) = 0.5.
    @P(x=2) = 0.5.

The first two lines establish simple facts and attach sentences to make them
mutually exclusive. The third line contain annotations that attach
probabilities to the labels to allow the calculation of answer probabilities.
When presented with the query `heads(C)?` the answer `heads(c1)` has a
probability of 0.5.

The descriptive sentences are propositional logic expressions that use labels
of the form `partition=value` as atoms. It is allowed to use non-numeric
values, i.e., labels like `x=heads` or `choice=opens_door_1` are valid. Complex
dependencies between clauses can be given through the combination of these
labels with the `and`, `or` and `not` operations leading to sentences like
`(x=1 and y=2) or z=1`.

For the Monte Carlo simulation, the probabilities for each label have to be
defined. This can be done manually per label:

    @P(x=1) = 0.333.
    @P(x=2) = 0.333.
    @P(x=3) = 0.333.

Or, if a uniform distribution is desired, with:

    @uniform(x).

Note that the `@uniform` annotation should be placed after all values for the
given partition have been defined.


Interpreter
-----------

Extensive help can be produced by invoking `datalog.py` with the `--help` flag.
For ease of use, some useful combinations are given here.

`datalog.py -v`: runs an interactive datalog prompt in verbose mode, showing
each statement is it is processed.

`datalog.py -f color -v -i examples/power.dl`: `-f color` Explicitly declares
colored output formatting, `-v` runs in verbose mode to show each statement as
it is processed, and `-i` switches to interactive mode after the given files
are processed.

`datalog.py -d examples/ancestor.dl`: Runs the ancestor.dl example file with a
debugging trace of the query answering process.

`datalog.py -m examples.demosql examples/demosql.dl`: Loads the external data
module `examples.demosql` (note that this is loaded according to Pyhton's
module path), and runs the example file that uses the externally defined
`triple` predicate.

`datalog.py --help`: Gets the full list of options for the current variant of
JudgeD.
