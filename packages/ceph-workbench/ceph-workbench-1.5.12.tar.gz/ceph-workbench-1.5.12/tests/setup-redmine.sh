set -xe
sudo docker run --name=postgresql-redmine -d --env='DB_NAME=redmine_production' --env='DB_USER=redmine' --env='DB_PASS=password' --volume=$(pwd)/data/postgresql:/var/lib/postgresql   quay.io/sameersbn/postgresql:9.4-5
sudo docker run --name=redmine -d --link=postgresql-redmine:postgresql --publish=10080:80 --env='REDMINE_PORT=10080' --volume=$(pwd)/data/redmine:/home/redmine/data quay.io/sameersbn/redmine:3.1.1-3
success=false
for delay in 15 15 15 15 15 30 30 30 30 30 30 30 30 60 60 60 60 120 240 512 ; do
    sleep $delay
    if python tests/redmine-init.py http://127.0.0.1:10080 admin admin ; then
        success=true
        break
    fi
done
$success
