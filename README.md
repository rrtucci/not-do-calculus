# Not Do Calculus

<img src="pics/jigsaw.jpg" alt="jigsaw" height="250">
An adjustment formula is like jigsaw puzzle where the
pieces come from another jigzsaw puzzle


## Code History
The software in this repo was inspired by
my earlier software at 

[https://github.com/rrtucci/dag_iden_detector/blob/master](https://github.com/rrtucci/dag_iden_detector/blob/master)

This software can do everything that the earlier
software can do plus much more. Whereas the 
earlier software could only verify
whether a given adjustment formula
was valid, this software can also
search for and discover adjustment formulae.

The code in this repo is written
in a fully object oriented style.
I feel this is appropriate, because,
if in the future, I or someone else comes
up with a better adjustment search
method (the software currently 
has 2 search methods, **search1** and **search2**), 
then all 
I will need to do to add it to this 
software is to subclass a few classes.

The code in this repo 
pertaining to the data structures
such as "BayesNet" and "Potential" 
comes from my much earlier 
quantum-fog repo

https://github.com/artiste-qb-net/quantum-fog

The names of all classes that don't
come from the quantum-fog repo
and were written fresh for this repo,
start with the prefix "NDC_" (for Not Do Calculus)
Here is their class tree:

<img src="pics/class-tree.jpg" alt="class-tree" height="250">


## Do Calculus Background
Judea Pearl has defined 
the concept of "identifiability" for
a do-query $P(y|do(\underline{x})=x)$
with respect to a Bayesian Network that I like to 
call the Original Promise (OP). Pearl has
also given 3 rules of "Do Calculus"
which can be applied to 
the OP to decide whether a
do-query for the OP is identifiable or not.
If it is identifiable, the 3 Rules
also yield a so called "adjustment formula".

An adjustment formula is
a formula that equals $P(y|do(\underline{x})=x)$
but 

* it contains no do operators 
* it contains no probabilities
of hidden variables, even when the OP has some. 
* It can be calculated from DATA
OBTAINED WITHOUT CONDUCTING AN RCT 
(Randomized Controlled Trial).

## What this code can and cannot do

Not-Do-Calculus (NDC) can be used

1. to test for validity, a given adjustment formula for a 
given OP (Original Promise bnet)
2. (search mode) to test for validity, 
every member of a "plausible set" of 
   adjustment formulae for a given OP

We provide 2 search algorithms: **search1** and **search2**

1. **search1**: The adjustment considered here 
replaces all hidden nodes of the
OP bnet by observed nodes, and then amputates that (i.e. removes arrows 
   entering node "x")

2. **search2**: The adjustment considered here is of the form

    $$P(y|do(\underline{x})=x) = \frac{1}{\sum_y numer} \sum_{u, v} P(x,y|u, 
   v) P(u)P(v)$$

    where we are assuming there are two hidden nodes h1 and h2 which are
    replaced by observed nodes u and v, respectively 


## Our Findings

Both **search1** and **search2** are
hardwired to find the backdoor adjustment
formula so that is no big feat. If in the OP,  there is no arrow from a 
hidden node to "x",
the backdoor adjustment formula is obviously valid.


* **search1** finds the front-door adjustment
formula but not the napkin adjustment one.

* **search2** finds the napkin adjustment
formula but not the front-door adjustment one.

All this is illustrated by
the numerous jupyter notebooks
included in this repo.(see the jupyter-notebooks folder)

