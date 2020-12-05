# Check if docker network is present (if this deployment is being done the first time)
DOCKER_NETWORK_ID=$(docker network inspect deployed-containers -f '{{ .Id }}')
if [[ "${DOCKER_NETWORK_ID}" == "" ]]; then 
    docker network create deployed-containers;
    docker-compose up -d reverse-proxy;
    touch ./.colors;
    echo "" >> .colors;
    echo -e "export DEPLOYED_COLOR=blue" > .colors;
    echo -e "export IDLE_COLOR=green" > .colors;
fi

# Get the latest colors config
source ./.colors

# Build and bring up new containers
git pull
docker-compose build --pull model
docker-compose -p $IDLE_COLOR up -d --scale model=$REPLICAS --force-recreate model

# Bring down old containers once new ones are working
while [ $(curl -s --location --request GET 'http://localhost/deployment_color' | tr -d \") != $IDLE_COLOR ]; do :; done
docker-compose -p $DEPLOYED_COLOR down

# Update the .colors config
echo "" >> .colors
echo -e "export DEPLOYED_COLOR="${IDLE_COLOR} > .colors
echo -e "export IDLE_COLOR="${DEPLOYED_COLOR} > .colors

# Prune unused images/layers (from old deployment)
docker image prune -f
