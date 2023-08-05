set -ex
DATA=$(pwd)/data
mkdir -p $DATA
sudo docker run --name=test-redis -d sameersbn/redis:latest
sudo rm -fr $DATA/mysql
mkdir -p $DATA/mysql
sudo docker run --name=test-mysql -d -e 'DB_NAME=gitlabhq_production' -e 'DB_USER=gitlab' -e 'DB_PASS=Wrobyak4' -v $DATA/mysql/data:/var/lib/mysql sameersbn/mysql:latest
sudo rm -fr $DATA/gitlab
mkdir -p $DATA/gitlab
sudo docker run --name='test-gitlab' -it -d --link test-mysql:mysql --link test-redis:redisio -e 'GITLAB_SIGNUP=true' -e 'GITLAB_PORT=80' -e 'GITLAB_HOST=localhost' -e 'GITLAB_SSH_PORT=8022' -p 8022:22 -p 8181:80 -e GITLAB_SECRETS_DB_KEY_BASE=4W44tm7bJFRPWNMVzKngffxVWXRpVs49dxhFwgpx7FbCj3wXCMmsz47LzWsdr7nM -v /var/run/docker.sock:/run/docker.sock -v $DATA/gitlab/data:/home/git/data -v $(which docker):/bin/docker sameersbn/gitlab
success=false
for delay in 15 15 15 15 15 30 30 30 30 30 30 30 30 60 60 60 60 120 240 512 ; do
    sleep $delay
    if wget -O - http://127.0.0.1:8181/users/sign_in | grep -q 'About GitLab' ; then
        success=true
        break
    fi
done
$success
