### Lexical Analysis
```
(a|b)*(aa|bb)(a|b)*
```

### LR(0) & SLR(1)
```
4
S->aAcBe
A->Ab
A->b
B->d
abbcde
```

### LL(1)
```
3
E -> E + T | T
T -> T * F | F
F -> i | ( E )
i + i * i
```