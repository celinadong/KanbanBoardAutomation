#!/bin/bash

for FILE in *.ipynb
do 
	jupyter nbconvert --to script  "${FILE}"
done
