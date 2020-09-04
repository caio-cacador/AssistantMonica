# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /AssistantMonica

# copy the dependencies file to the working directory
COPY . .

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx

# install dependencies
RUN pip install -r requirements.txt

# copy config file
#COPY configs.json .

# command to run on container start
CMD [ "python", "run.py" ]