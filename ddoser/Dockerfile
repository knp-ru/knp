FROM python:3.7.3-stretch

WORKDIR /usr/src/app
COPY . .
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --upgrade pip && \
    pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
ENTRYPOINT ["python", "main.py"]
