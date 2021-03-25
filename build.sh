# Syntax: ./build.sh
# Use --no-cache=true  when necessary
VERSION_TAG=$(<VERSION)
docker build -t skafos/slack-alerts-svcs:$VERSION_TAG .