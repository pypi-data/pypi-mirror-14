set -xe
sudo docker run --name=postgresql-redmine -d --env='DB_NAME=redmine_production' --env='DB_USER=redmine' --env='DB_PASS=password' --volume=$(pwd)/data/postgresql:/var/lib/postgresql   quay.io/sameersbn/postgresql:9.4-5
sudo docker run --name=redmine -d --link=postgresql-redmine:postgresql --publish=10080:80 --env='REDMINE_PORT=10080' --volume=$(pwd)/data/redmine:/home/redmine/data quay.io/sameersbn/redmine:3.1.1-3
sleep 120
python tests/redmine-init.py http://127.0.0.1:10080 admin admin
