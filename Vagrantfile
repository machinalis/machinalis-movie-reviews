# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/xenial64"

  config.vm.hostname = "movie-recommendations.local"

  config.vm.network "forwarded_port", guest: 80, host: 5000
  config.vm.network "forwarded_port", guest: 5000, host: 5001

  config.vm.synced_folder ".", "/home/ubuntu/movie_recommendations/"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = 2
    vb.name = "movie-recommendations"
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y git build-essential nginx supervisor python3 python3-dev python3-venv
  SHELL

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    pyvenv-3.5 --without-pip movie_recommendations_venv
    source movie_recommendations_venv/bin/activate
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python
    pip install -r movie_recommendations/requirements.txt
    cd movie_recommendations
    export FLASK_APP=movie_recommendations/__init__.py
    flask init_db
    flask generate_user_network
    flask import_movie_dataset imdb-5000-movie-dataset.zip
  SHELL

  config.vm.provision "shell", inline: <<-SHELL
    echo '
upstream movie_recommendations_upstream {
    server 127.0.0.1:5000 fail_timeout=0;
}
server {
    listen 80;
    server_name localhost;
    client_max_body_size 4G;
    access_log /home/ubuntu/movie_recommendations/nginx_access.log;
    error_log /home/ubuntu/movie_recommendations/nginx_error.log;
    location /static/ {
        alias /home/ubuntu/movie_recommendations/movie_recommendations/static/;
    }
    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        if (!-f $request_filename) {
            proxy_pass http://movie_recommendations_upstream;
            break;
        }
    }
}
    ' > /etc/nginx/conf.d/movie_recommendations.conf
    /bin/systemctl restart nginx.service
SHELL

  config.vm.provision "shell", inline: <<-SHELL
  echo '
[program:movie_recommendations]
environment=FLASK_APP="/home/ubuntu/movie_recommendations/movie_recommendations/__init__.py"
user = ubuntu
directory = /home/ubuntu/movie_recommendations/
command = /home/ubuntu/movie_recommendations_venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 movie_recommendations:app
autostart = true
autorestart = true
stderr_logfile = /home/ubuntu/movie_recommendations/gunicorn_stderr.log
stdout_logfile = /home/ubuntu/movie_recommendations/gunicorn_stdout.log
stopsignal = INT
  ' > /etc/supervisor/conf.d/movie_recommendations.conf
  /bin/systemctl restart supervisor.service
SHELL

end
