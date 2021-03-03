docker build -t remote-wol .
docker run -p 80:5000 -v "/your/path/here" remote-wol