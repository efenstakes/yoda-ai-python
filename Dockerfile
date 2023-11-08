FROM python:3.9

WORKDIR /yoda

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./main.py ./
COPY ./prompts /yoda

# start api
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
