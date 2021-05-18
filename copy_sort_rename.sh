#!/bin/bash

# create directories for each of the emotions
for SUBFOLDER in afraid angry disgusted happy neutral sad surprised
do
  mkdir -p "./KDEF_sorted/$SUBFOLDER"
done


# sort and move images by directories
find ./KDEF -type f -name "????AF*.JPG" -exec bash -c 'cp {} ./KDEF_sorted/afraid/$(basename {})' \;
find ./KDEF -type f -name "????AN*.JPG" -exec bash -c 'cp {} ./KDEF_sorted/angry/$(basename {})' \;
find ./KDEF -type f -name "????DI*.JPG" -exec bash -c 'cp {} ./KDEF_sorted/disgusted/$(basename {})' \;
find ./KDEF -type f -name "????HA*.JPG" -exec bash -c 'cp {} ./KDEF_sorted/happy/$(basename {})' \;
find ./KDEF -type f -name "????NE*.JPG" -exec bash -c 'cp {} ./KDEF_sorted/neutral/$(basename {})' \;
find ./KDEF -type f -name "????SA*.JPG" -exec bash -c 'cp {} ./KDEF_sorted/sad/$(basename {})' \;
find ./KDEF -type f -name "????SU*.JPG" -exec bash -c 'cp {} ./KDEF_sorted/surprised/$(basename {})' \;


# rename all images in each folder according to the emotion
for SUBFOLDER in afraid angry disgusted happy neutral sad surprised
do
  FILE_INDEX=0

  for FILE in ./KDEF_sorted/${SUBFOLDER}/*.JPG
  do
    mv "$FILE" "./KDEF_sorted/${SUBFOLDER}/${SUBFOLDER}_${FILE_INDEX}.jpg"
    FILE_INDEX=$((FILE_INDEX + 1))
  done
done
