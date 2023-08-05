fail
====

run a program until it fails and gather statistics

Elaborations from a favorite bash one-liner::

    I=0; while ./do_some_things.py --param $arg; do I=$((I+1)); echo Iteration ${I}; sleep 1; done

fun things to try
----------------

Russian roulette (with two chambers)::

    fail 'exit $(expr $RANDOM % 2)'

----

Jeff Hammel



