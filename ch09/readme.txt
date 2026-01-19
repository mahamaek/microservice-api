# Run graphql-faker with docker

docker ps

cd ch09 && docker run -p 9002:9002 -v $(pwd):/workdir apisguru/graphql-faker schema.graphql