FROM mcr.microsoft.com/playwright:focal

COPY . ./app
WORKDIR /app
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install --default-timeout=100 -r requirements.txt
RUN python3 -m playwright install

CMD ["-u", "main.py"]
ENTRYPOINT ["python3"] 