#!/bin/sh

# Check if config.yaml exists
if [ ! -f /data/config.yaml ]; then
    cp /app/src/scraibe_webui/misc/config.yaml /data/config.yaml
    sed -i 's/^\([[:space:]]*\)\([^#]\)/\1# \2/' /data/config.yaml
    sed -i 's/#\{1\}[[:space:]]\{1,3\}#/##/' /data/config.yaml
    sed -i '1i## In this config file you can set your custom configuration. To use a configuration, uncomment the line and change the value.\n## Lines that start with ## are comment lines.\n' /data/config.yaml
fi

# Run the application
exec "$@"