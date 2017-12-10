# Deployment Instructions

These are the deployment instructions for getting the web application up and running on an EC2 instance. 

## Prerequisites

### Git

`sudo yum install git`

### Docker

Install the most recent Docker Community Edition package.

`sudo yum install -y docker`

Start the Docker service.

`sudo service docker start`


Add the ec2-user to the docker group so you can execute Docker commands without using sudo.

`sudo usermod -a -G docker ec2-user`

Log out and log back in again to pick up the new docker group permissions.

Verify that the ec2-user can run Docker commands without sudo.

`docker info`

### Docker-Compose

Get latest version of docker compose

`sudo curl -L https://github.com/docker/compose/releases/download/1.17.0/docker-compose-\`uname -s\`-\`uname -m\` -o /usr/local/bin/docker-compose`

Apply executable permissions to the binary

`sudo chmod +x /usr/local/bin/docker-compose`

Test installation

`docker-compose --version`

## Setup App/Data

Clone github repo

`git clone https://github.com/winlingit/mids-w210-capstone.git`

Enter project driectoy and copy data from `data/app` and `data/general` in our VM

`cd mids-w210-capstone`

### Instructions for Filezilla EC2 Login With Key

https://stackoverflow.com/questions/16744863/connect-to-amazon-ec2-file-directory-using-filezilla-and-sftp

## Tweaks and Docker Startup

Need to change `SERVER_NAME` in `config/settings.py` to the name of the public dns for the server and set `debug=False`


Get site up and running with `docker-compose up` in the root directory of the application
	* The first time you do this, docker should have to build the images and download a bunch of things in order to do so
	* After that, it will skip these steps as it is just making new containers from the images

Once all models and data in the application have been solidified, you can comment out `populate_db(app)` from the `app.py` file so it doesn't reload the data everytime the web working is reloaded. The data is persisted in the Postgres container so this is unnecessary. It was just implemented so that we could iterate on the design and blow away the existing database models easily.