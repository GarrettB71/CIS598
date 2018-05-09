#!/bin/bas
mysql -h mysql.cs.ksu.edu -u blehmg -p blehmg -e "CALL GetLangData('Kansas City');" | sed 's/\t/,/g' >  KC.csv