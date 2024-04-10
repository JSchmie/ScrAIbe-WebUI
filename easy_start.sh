#!/bin/bash
cname="scraibe_base"
ports="7860 80"


echo "Searching for container.."

# container name not found -> start new container
if [ ! "$(docker ps -a -q -f name=$cname)" ]; then
    echo "Start new container"
    # check for free port, first free port gets it
    for PORT in $ports ; do
        nc -z -w5 0.0.0.0 $PORT
        port_stat=$?
        if [ $port_stat == 1 ]; then
            port=$PORT
            break
        fi
    done
    if [ $port_stat == 0 ]; then
        echo "No free port available! Checked ports: $ports."
    else
        docker run -i -p $port:7860 --name $cname --gpus 'all' hadr0n/scraibe:0.1.1.dev-base-de
    fi
else
    # container only found in inactive list (no -a here) -> start container
    if [ ! "$(docker ps -q -f name=$cname)" ]; then
        for PORT in $ports ; do
            nc -z -w5 0.0.0.0 $PORT
            port_stat=$?
            if [ $port_stat == 1 ]; then
                port=$PORT
                break
            fi
        done
        echo "Found container"
        docker start $cname
    # container found and already running -> echo ports
    else
        blocked_port=$(docker ps --format '{{.Ports}}' -f name=$cname)
        echo "Container already running on port $blocked_port"
        # find first occurence of ":" followed by 2 to 4 numbers -> find oprt number in container output
        port_nr="$(echo $blocked_port | grep -oP ':\K([[:digit:]]{2,4})' | head -1)"

    fi
fi  