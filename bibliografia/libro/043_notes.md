# Notes

[1](part0011_split_001.html#fn1x4-bk)We use the terms *agent*, *environment*, and *action* instead of the engineers’ terms *controller*, *controlled system* (or *plant*), and *control signal* because they are meaningful to a wider audience.

[2](part0011_split_001.html#fn2x4-bk)We restrict attention to discrete time to keep things as simple as possible, even though many of the ideas can be extended to the continuous-time case (e.g., see Bertsekas and Tsitsiklis, 1996; Doya, 1996).

[3](part0011_split_001.html#fn3x4-bk)To simplify notation, we sometimes assume the special case in which the action set is the same in all states and write it simply as 𝒜.

[4](part0011_split_001.html#fn4x4-bk)We use *R**t*+1 instead of *R**t* to denote the reward due to *A**t* because it emphasizes that the next reward and next state, *R**t*+1 and *S**t*+1, are jointly determined. Unfortunately, both conventions are widely used in the literature.

[5](part0011_split_002.html#fn5x4-bk)Better places for imparting this kind of prior knowledge are the initial policy or initial value function, or in influences on these.

[6](part0011_split_002.html#fn6x4-bk)Section 17.4 delves further into the issue of designing effective reward signals.

[7](part0011_split_003.html#fn7x4-bk)Episodes are sometimes called “trials” in the literature.
