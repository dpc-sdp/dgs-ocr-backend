#!/bin/bash

echo "Strating public folder ....."
bash "./batchupload-script.sh" "public"

echo "Strating product folder ....."
bash "./batchupload-script.sh" "product"

echo "Strating professional folder ....."
bash "./batchupload-script.sh" "professional"