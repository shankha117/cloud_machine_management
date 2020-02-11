





server {
    listen 80;
    server2 13.235.8.67;
location / {
  include proxy_params;
  proxy_pass http://unix:/home/ubuntu/cloud_machine_management/app/flask_app.sock;
    }
}





[Unit]
#  specifies metadata and dependencies
Description=Gunicorn instance to serve myproject
After=network.target


# tells the init system to only start this after the networking target has been reached
# We will give our regular user account ownership of the process since it owns all of the relevant files
[Service]
# Service specify the user and group under which our process will run.
User=ubuntu

# give group ownership to the www-data group so that Nginx can communicate easily with the Gunicorn processes.
Group=www-data
# We'll then map out the working directory and set the PATH environmental variable so that the init system knows where our the executables for the process are located (within our virtual environment).
WorkingDirectory=/home/ubuntu/cloud_machine_management
Environment="PATH=/home/ubuntu/cmmvenv/bin"


# We'll then specify the commanded to start the service
ExecStart=/home/ubuntu/cmmvenv/bin --workers 3 --bind unix:app.sock -m 007 app.flask_app:api --reload
# This will tell systemd what to link this service to if we enable it to start at boot. We want this service to start when the regular multi-user system is up and running:
[Install]
WantedBy=multi-user.target
