for i in test-gitlab test-mysql test-redis ; do sudo docker stop $i || true ; sudo docker rm $i || true ; done
for i in postgresql-redmine redmine ; do sudo docker stop $i || true ; sudo docker rm $i || true ; done
sudo rm -fr data
