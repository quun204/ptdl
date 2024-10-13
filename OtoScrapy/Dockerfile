FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "-m", "scrapy", "runspider", "OtoScrapy/spiders/Oto.py"]
