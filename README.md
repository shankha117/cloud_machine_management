
## **`Cloud Machine Management`**

## **`Description`**

There will be multiple clusters and each cluster will have zero or more machines. Each machine will have zero or more tags.

Also, each cluster will have a name and a cloud region, each machine will have a name, ip address, an instance-type.

The system should allow users to create clusters, create machines in a cluster, add tags to the machine when creating them, delete machines and clusters and perform operations like start, stop, reboot on a group of machines using tags.


## **`Available Operation`**


* examples

    :zap: Create, Modify, Delete Clusters
    
    :zap: Create Instances under clusters
    
    :zap: Modify the Tags of cluster and instances
    
    :zap: ON, OFF, REBOOT specific instances or multiple instances using tags
    


## :rocket:&nbsp;**`Run Project`**

* ###**`Manually`** -
    * install a virtual environment
    * install packages from reqirement.txt
        
        `pip install requirements.txt` 
    
    * simply run the start_app.sh file
    
        `sh start_app.sh`
        
* ###**`Docker`** -
    * install docker, docker-compose
    * run the compose file from root directory
    
        `docker-compose up`
        
## :detective:&nbsp;**`Validate the Project`**

* after gunicorn is running you can visit to get the api details

    :link: `http://localhost:8081/swagger/`
    

## **`Deploy in AWS`**
![Alt text](app/static/amazon-ec2.png?raw=true "Title")

We will deploy this in an AWS EC2 instance with Nginx and Gunicorn.

Things to do -

:heavy_check_mark: Create a  free AWS account

:heavy_check_mark: Select a AMI, configure server (security groups) :fire:   

:heavy_check_mark: SSH to the server

:heavy_check_mark: setup NGINX and systemd

:heavy_check_mark: test the app from your local browser


