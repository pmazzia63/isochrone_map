FROM python:3.9-slim

WORKDIR /usr/src/package_name

RUN apt-get update && apt-get install gcc g++ python3-pip -y && apt-get clean

COPY pyproject.toml ./

RUN pip3 install tomli
RUN python3 -c 'import tomli; t = tomli.load(open("pyproject.toml", "rb")); file = open("requirements.txt", "w"); file.write("\n".join(t["project"]["dependencies"])); file.close()'
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./package_name ./package_name

RUN pip3 install .
