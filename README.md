# ppp_splitter
Script for splitting on pppoker app

Use:
```
$ python ppp_splitter.py James -1 Carl 7 Tony -20
Rake Earned:
Tony: 14.00
 
James      pays Carl           1.00
Tony       pays Carl           6.00
```
Gives rake to biggest loser, until they are no longer the biggest loser, then give to the 2 biggest losers, and so on.
