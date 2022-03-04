#!/bin/bash

cd ~/Desktop
output=data.json

mem(){
  cat /proc/meminfo | grep MemFree | awk '{print $2, $3}'
}

# Remove existing "output" file. Ignore if not present.
rm $output || true

# Bracket for JSON array
echo '[' >> $output

# Iterate
for ((i = 0; i < 1000; ++i))
do
  # JSON format start
  echo '{' >> $output

  echo \"Date\":\"$(date +"%D")\" >> $output
  echo \"Time\":\"$(date +"%T.%N")\" >> $output
  echo \"MemFree\":\"$(mem)\" >> $output

  # JSON format end
  echo '}' >> $output

done

# JSON array end.
echo ']' >> $output
exit