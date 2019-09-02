#!/bin/bash

inFile="$2"
regcount=0

rm -rf profile_results

mkdir profile_results

while IFS='' read -r line || [[ -n "$line" ]]; do
        echo "Text read from file: $line"
        export $line
					cd ../build/
					pwd
					rm ../include/aa_params.hpp
					cat ../lib/header > ./params.txt
					echo "#define UNROLLS $unroll" >> ./params.txt
					echo "#define SNUMREG $acc" >> ./params.txt
					echo "#define SDIVINT $divint" >> ./params.txt
					echo "#define SDIVINDM $divindm" >> ./params.txt
					echo "#define SFDIVINDM $divindm.0f" >> ./params.txt
					echo "} // namespace astroaccelerate" >> ./params.txt
					echo "#endif" >> ./params.txt
					mv params.txt ../include/aa_params.hpp
	
#					make clean

									
					make -j 2

					cd ../scripts/
					pwd

					cp ../include/aa_params.hpp profile_results/u"$unroll"_a"$acc"_t"$divint"_dm"$divindm"_r"$regcount".h

					../build/astro-accelerate $inFile > profile_results/u"$unroll"_a"$acc"_t"$divint"_dm"$divindm"_r"$regcount".dat
			
					echo "unrolls: $unroll	acc: $acc    divint: $divint    divindm: $divindm    reg: $regcount"
done < "$1"

optimum=$(grep "Real" profile_results/* | awk -F" " '{print $4" "$1}' | sort -n | tail -1 | awk -F" " '{print $2}' | awk -F"." '{print $1".h"}')

cp $optimum ../include/aa_params.hpp
pwd
cd ../build
make clean
make -j 16
cd ../scripts/

echo "FINISED OPTIMISATION"
