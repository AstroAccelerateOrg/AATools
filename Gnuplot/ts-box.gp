reset
set terminal pdf colour font 'Times-New-Roman,12'

load "hist.fct"

set grid
set print "-"

set boxwidth 0.8
set style fill solid 1.0


# branches {} works from gnuplot version 4.6
if (!exists("filename")) {
	print "No filename provided. Launch as:\n\t gnuplot <script> -e \"filename='<your_filename>'\""
	exit
}

#data='global.dat'
data=filename
#data='~/global_analysed_frb.dat'
if (!exists("each")) each=1

stats data binary format="%f%f%f%f" every each using 1 nooutput

around=STATS_max*0.1
dm_min=STATS_min
dm_max=STATS_max
#set yrange[STATS_min-around:STATS_max+around]

stats data binary format="%f%f%f%f" every each using 3 nooutput
snr_min=STATS_min
snr_max=STATS_max
#set cbrange[STATS_lo_quartile:STATS_up_quartile]

stats data binary format="%f%f%f%f" every each using 2 nooutput
time_min=STATS_min
time_max=STATS_max

set yrange[dm_min-around:dm_max+around]
set xrange[time_min:time_max]
set xlabel "Times (s)"
set ylabel "DM channel"
set y2label "Pulse width"
set output "ts-box.pdf"
	plot data binary format="%f%f%f%f" every each  using 2:1:4 title "" pt 7 ps 0.4 palette
unset output
print "done with ts-box"
#set yrange[snr_min:1.2*snr_max]
#set xrange[time_min:0.01*time_max]
#set xlabel "Times (s)"
#set ylabel "SNR"
#set output "ts-box-snr.pdf"
#        plot data binary format="%f%f%f%f" every 1 using 2:3:1 title "" pt 7 ps 0.4 lc rgb "black" #palette
#unset output
#print "done with ts-box-snr"

set xrange[dm_min:dm_max]
set yrange[0.95*snr_min:1.1*snr_max]
set xlabel "DM channel"
set ylabel "SNR"
set y2label "Pulse width"
set output "ts-box-dm.pdf"
	plot data binary format="%f%f%f%f" every each using 1:3:4 title "" pt 7 ps 0.3 palette
unset output
print "done with ts-box-dm"

binwidth=0.1
binstart=-0.05

set xrange[dm_min-0.05*dm_max:1.05*dm_max]
set yrange[0:*]
set ylabel "Number of candidates"
set xlabel "DM channel"
unset y2label
set output "ts-hist-dm.pdf"
	plot  data binary format="%f%f%f%f" @hist ls 1 lc rgb "black" title ""
unset output
print "done with hist-dm"

binwidth=1
binstart=-0.5

set xrange[snr_min-1.5:snr_max+1.5]
set logscale y
set xlabel "SNR"
set output "ts-hist-snr.pdf"
	plot  data binary format="%f%f%f%f" @hist2 ls 1 lc rgb "red" title ""
unset output
print "done hist-snr"
