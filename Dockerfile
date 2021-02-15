FROM python:3.9.1-slim

ENV PYTHONUNBUFFERED 1
ENV PROJECT_DIR /greenhouse-api

ARG REQUIREMENTS_FILE=requirements.txt

ADD requirements*.txt $PROJECT_DIR/

RUN apt-get update && \
     ACCEPT_EULA=Y apt-get install -y g++ &&\
#     build-essential \
#     libssl-dev \
#     libffi-dev \
#     python3-dev &&\
    apt-get clean && \
    pip --no-cache-dir install -r $PROJECT_DIR/$REQUIREMENTS_FILE

ADD . $PROJECT_DIR/

WORKDIR $PROJECT_DIR

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
