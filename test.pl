/*
- Define family relationships father, mother, sister, brother, uncle, aunt, cousin, grandfather, grandmother, etc.
- Must provide parental and gender information.
*/ 
parent(a,b1).
parent(a,b2).
parent(b1,c).
parent(b1,d).
parent(b2,e).
female(a).
female(b1).
female(b2).
female(c).
male(d).
male(e).

human(X):- female(X);male(X).
mother(X,Y):- parent(X,Y),female(X).
father(X,Y):- parent(X,Y),male(X).
sibling(X,Y):- parent(Z,X),parent(Z,Y),X\==Y.
sister(X,Y):- sibling(X,Y),female(X).
brother(X,Y):- sibling(X,Y),male(X).
grandparent(X,Y):- parent(X,Z),parent(Z,Y).
grandmother(X,Z):- mother(X,Y),parent(Y,Z).
grandfather(X,Z):- father(X,Y),parent(Y,Z).
uncle(X,Z):- brother(X,Y), parent(Y,Z).
aunt(X,Z):- sister(X,Y), parent(Y,Z).
cousin(X,Y):- parent(Z,X), sibling(Z,W), parent(W,Y).