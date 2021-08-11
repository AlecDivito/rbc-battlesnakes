#!/bin/bash

SNAKE_COUNT=2
ITERATIONS=1
MAX_EVOLVES=1

i=1
until [ $i -gt $SNAKE_COUNT ]
do
    PORT="808$i";
    echo "Starting http://localhost:$PORT";
    MULTI_SNAKE_TRAINING=$SNAKE_COUNT SNAKE_NETWORK="./network/gen42-fitness:3816" ITERATIONS=$ITERATIONS SAVE_FOLDER="./network/snake_${i}" PORT=$PORT python3 server.py &
    ((i=i+1))
done

for var in {1..$SNAKE_COUNT}
do
done

sleep 1000

for evolves in {0..$MAX_EVOLVES}
do
    for iterations in {0..$ITERATIONS}
    do
        ./battlesnake play -W 11 -H 11 -d 1000 \
            --name snake_1 --url http://localhost:8081 \
            --name snake_2 --url http://localhost:8082 \
            -v
            # --name snake_3 --url http://localhost:8083 \
            # --name snake_4 --url http://localhost:8084 \
            # --name snake_5 --url http://localhost:8085 \
            # --name snake_6 --url http://localhost:8086 \
            # --name snake_7 --url http://localhost:8087 \
            # --name snake_8 --url http://localhost:8088 \
    done
done

print "done"