# Magnus
Word Problem solver for One Relator Groups using Magnus' Method.

# Example
For instance to solve the Word Problem for the Baumslag Solitar Group BS(2,3) given by the presentation

BS(2,3) = &#8826; a, b &#8739; a<sup>-1</sup>b<sup>2</sup>a b <sup> -3 </sup> &#8827;

for the word b<sup>−1</sup>a<sup>−1</sup>bab<sup>−1</sup>a<sup>−1</sup>bab<sup>−1</sup>

run <code> python3 magnus.py </code>

And enter

<code> S = a b </code>


<code> r = aI b b a bI bI bI </code>


<code> w = bI aI b a bI aI b a bI </code>

# References
The program is an implementation of the inductive proof for the decidabilty of one-relator groups found in
<em>Putman, Andrew. "One-relator groups." preprint (2018)</em>.

It uses the special case where T is equal to the empty set.
