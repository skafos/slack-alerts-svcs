# Syntax: ./deploy.sh
VERSION_TAG=$(<VERSION)
docker push skafos/slack-alerts-svcs:$VERSION_TAG