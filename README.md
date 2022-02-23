# Indigestion

## About
Indigestion containerized solution for automatically ingesting files from one server to another. The indigestion container runs a Python script on a 10 minute loop scanning for new files in a directory, sending them to a remote server, verifying their integrity with a sha256 comparison, and then cleans the files out of the host directory. This works really great for people who run home media servers and procure media from various places and want to automate the ingestion to one centralized location. (i.e. ripping multiple non-copyrighted disks to a folder, pointing the indigestion container to the folder, and letting it transfer them for you as they finish ripping)

**SECURE**, _FAST_, AND ACCURATE

## Requirements

Docker, and ssh thats it :-)

## Setup

### SSH Keys
You will first want to establish a connection between the container host and the server you will be sending the data to with an ssh key.

```
ssh-keygen -t rsa -b 4096
```

You will then want to authenticate the key with the remote server.

```
ssh-copy-id user@remote_server_address
```

### TOML
You will want to edit the toml file provided with appropriate values for the paths for sending, ingestion, and for remote server information. Follow the examples set in the config.toml as a template.

### Docker
When building the Docker image with docker build, it is important you pass in the remote_destination user and address exactly like you wrote it in the ssh key setup.

```
sudo docker build -t indigestion --build-arg remote_destination=user@127.0.0.1 .
```

Then you will run the container.

```
sudo docker run -d \
    -it \
    --name=indigestion_container \
    --mount type=bind,source="/path/to/local_files/",target=/root/ingest \
    --mount type=bind,source="/path/to/.ssh/id_rsa",target=/root/.ssh/id_rsa \
    indigestion
```

Where /path/to/local_files/ is the path to the directory of the files that you are sending
And
where /path/to/.ssh/id_rsa is the path to generate ssh key you will be passing to ther docker image for easier and more secure ssh-ing.

### Running
At this point the Docker container will be running and ingesting your files in batches and then waiting a period of time for the next batch of ingesting to begin.

# Final Notes

Good luck and happy indigestion!
