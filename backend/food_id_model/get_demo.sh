#!/bin/bash


root_dir="/home/daviddu/CS130/backend/food_id_model/datasets/food-classification/val"


> paths.txt


for class_dir in "$root_dir"/*; do
    if [[ -d "$class_dir" ]]; then
        find "$class_dir" -maxdepth 2 -type f | head -n 1 >> paths.txt
    fi
done

echo "Paths written to paths.txt"
