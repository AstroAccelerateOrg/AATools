# AATools

Collection of potential useful scripts (Gnuplot, python, R, etc.) for AstroAccelerate.

## Guides for the scripts
### Gnuplot/ts-box.gp
*Warning: this script can run long time depending on the provided candidate file*
This script provide four images  in a pdf format file with these specification:
* `ts-box.pdf`: a perspective view from top on a time (x-axis) vs DM trial (y-axis) plane width a changing color related to the pulse width.
* `ts-box`: connection between the DM trial (x-axis) and signal to noise ratio (y-axis). As before the color map shows the pulse width.
* `ts-hist-snr`: histogram showing the number of candidates scattered by the signal to noise ratio.
* `ts-hist-dm`: plot showing number of candidates scattered through the bins of DM trials.

To produce the plots please run the script as follows (gnuplot version => 4.6):
>`gnuplot -e "filename='aa_candidate_file'" ts-box.gp>`

where the `aa_candidate_file` is the output result file from AstroAccelerate (for examples: `peak_analysed-t_0.00-dm_0.00-152.00.dat`).

This script is using a supporting file `hist.fct` created by Hagen Wierstorf (for details see: [gnuplotting](http://www.gnuplotting.org/tag/histogram/)). 
