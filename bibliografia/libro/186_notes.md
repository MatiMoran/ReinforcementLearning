# Notes

[1](part0024_split_001.html#fn1x17-bk)What control means for us is different from what it typically means in animal learning theories; there the environment controls the agent instead of the other way around. See our comments on terminology at the end of this chapter.

[2](part0024_split_003.html#fn2x17-bk)Comparison with a control group is necessary to show that the previous conditioning to the tone is responsible for blocking learning to the light. This is done by trials with the tone/light CS but with no prior conditioning to the tone. Learning to the light in this case is unimpaired. Moore and Schmajuk (2008) give a full account of this procedure.

[3](part0024_split_004.html#fn3x17-bk)The only differences between the LMS rule and the Rescorla–Wagner model are that for LMS the input vectors **x***t* can have any real numbers as components, and—at least in the simplest version of the LMS rule—the step-size parameter *α* does not depend on the input vector or the identity of the stimulus setting the prediction target.

[4](part0024_split_006.html#fn4x17-bk)In our formalism, there is a different state, *S**t*, for each time step *t* during a trial, and for a trial in which a compound CS consists of *n* component CSs of various durations occurring at various times throughout the trial, there is a feature, *x**i*, for each component CS*i*, *i* = 1, …, *n*, where *x**i*(*S**t*) = 1 for all times *t* when the CS*i* is present, and equals zero otherwise.

[5](part0024_split_006.html#fn5x17-bk)In our formalism, for each CS component CS*i* present on a trial, and for each time step *t* during a trial, there is a separate feature *x**i**t*, where *x**i**t*(*S**t*′) = 1 if *t* = *t*′ for any *t*′ at which CS*i* is present, and equals 0 otherwise. This is different from the CSC representation in Sutton and Barto (1990) in which there are the same distinct features for each time step but no reference to external stimuli; hence the name complete serial compound.
