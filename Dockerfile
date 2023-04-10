# Official python docker image
FROM python:3.11.2

# Work directory
WORKDIR /code

# Copy requirements to /WORKDIR
COPY ./requirements.txt /code/

# Install dependencies
RUN python3 -m pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the API source code to WORKDIR
COPY ./src /code/src
CMD [ "python3", "-m", "src" ]
