Emperical Analysis of Errors
============================
- Filter doesn't smooth transients out enough, causing errorneous detection of transients in the echos
- Extraneous transients that are too far or too close to be possible with speeding up/slowing down scratching should be filtered out in transient discrimination with thresholding.

after some tweaking+additional discrimination....

transient detection is pretty bad. it doesn't discriminate between echoes/extraneous transients that have small peaks (after filtering) and the actual ones.

the nature of errors is either none or almost all.

This also brings into question how to properly handle additions and deletions to prevent the bit stream from getting completely messed up after one error.
