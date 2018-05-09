#!/bin/bas
mysql -h mysql.cs.ksu.edu -u blehmg -p blehmg -e "CALL GetLangData('New York');" | sed 's/\t/,/g' >  NY.csv