 FROM python:3.9.17

 WORKDIR /usr/src/app

 COPY requirements.txt ./

 RUN pip install --no-cache-dir -r requirements.txt

 COPY . .

 CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]


# After docker-compose up -d
# Run in cmd docker exec -it "python image"
# run this command
# /usr/local/bin/alembic upgrade head
 