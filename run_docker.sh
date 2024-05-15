#!/bin/bash

file=/app/scraibe_webui/misc/config.yaml
dest=/data/config.yaml
# copy only if target file is not present
if [ ! -e "$dest" ]; then
    cp -n "$file" "$dest"
    # comment in every line, indenting the #
    sed -i 's/^\([[:space:]]*\)\([^#]\)/\1# \2/' "$dest"
    # remove whitespaces between # # for lines that are comment lines
    sed -i 's/#[[:space:]]\{1,3\}#/##/' "$dest"
    # insert information line at the beginning of file.
    sed -i -e '1i\
## In this config file you can set your custom configuration. To use a configuration, uncomment the line and change the value.\n## Lines that start with ## are comment lines.' -e '1i\'$'\n' $dest
fi
python3 -m scraibe_webui.cli --start-server
