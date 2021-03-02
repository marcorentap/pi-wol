FOR /f "tokens=*" %%i IN ('docker ps -q') DO docker stop %%i
docker build -t remote-wol .
docker run -p 80:5000 -v "D:\Projects\remote-wol:/app" remote-wol