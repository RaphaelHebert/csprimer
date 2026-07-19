#!/bin/bash

#!/bin/bash

echo "Press keys (q to quit)..."

while true; do
    read -rsn1 key

    case "$key" in
        q)
            echo "Quitting."
            break
            ;;
        0)
            ;;
        [1-9])
            for i in $(seq 1 $key);
                do
                    echo $i
                    echo -ne '\007' 
                    sleep 1
                done
            ;;
        *)
            echo "Press a number"
            ;;
    esac
done