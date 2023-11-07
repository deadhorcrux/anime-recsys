docker build . -t rec_server
docker run --rm -it -p 80:80 rec_server
