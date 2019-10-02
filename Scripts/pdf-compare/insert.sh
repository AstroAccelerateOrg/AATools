#!/bin/bash

number=0

for f in *.png; 
do 
	SIZE=$(du -k "$f" | cut -f1);
	if [ $SIZE != 0 ]; then
		echo "\\includegraphics[width=0.33\\linewidth]{$f}\\\\";
	else
		echo "\\includegraphics[draft,width=0.33\\linewidth]{output}\\\\";
	fi
	number=$((number+1));
	mod=$((number%3));
	if [ $mod = 0 ]; then
		echo '\\'"verb|$f|";
		echo '\\\\';
	fi
done;
echo "$number"
