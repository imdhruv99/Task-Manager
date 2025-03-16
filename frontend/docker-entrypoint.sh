#!/bin/bash
set -e

# env specific file
env_file="/usr/share/nginx/html/env-config.js"
echo "window.ENV = {" > $env_file

# Only export variables starting with VITE_ or REACT_APP_
for var in $(printenv | grep -E "^(VITE_|REACT_APP_)")
do
  key=$(echo $var | cut -d"=" -f1)
  value=$(echo $var | cut -d"=" -f2-)
  echo "  \"$key\": \"$value\"," >> $env_file
done

echo "};" >> $env_file

exec "$@"
