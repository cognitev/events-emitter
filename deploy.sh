    #!/bin/sh

    echo "Start build docker file"
    echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
    docker build -f Dockerfile --pull=true -t $PROJECT --network=host  . || exit 123
    PROJECT_IMG=$(docker images -q $PROJECT)
    docker tag $PROJECT_IMG $DOCKER_USERNAME/$PROJECT:latest
    docker tag $PROJECT_IMG $DOCKER_USERNAME/$PROJECT:build-$TRAVIS_BUILD_NUMBER
    docker push $DOCKER_USERNAME/$PROJECT:build-$TRAVIS_BUILD_NUMBER 
    docker push $DOCKER_USERNAME/$PROJECT:latest
    echo "Finish build docker file"
