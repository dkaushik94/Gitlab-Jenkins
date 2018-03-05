# List of all resources we have referred and a quick guide to set things up

### Installing gitLab as a docker image

[GitLab Documentation on docker image](https://docs.gitlab.com/omnibus/docker/README.html)

```
sudo docker run --detach \
    --hostname gitlab.example.com \
    --publish 443:443 --publish 80:80 --publish 22:22 \
    --name gitlab \
    --restart always \
    --volume /srv/gitlab/config:/etc/gitlab \
    --volume /srv/gitlab/logs:/var/log/gitlab \
    --volume /srv/gitlab/data:/var/opt/gitlab \
    gitlab/gitlab-ce:latest
```

> Replace srv with a path on the filesystem of your choice on mac as the OS prevents the path srv to be created and used.


### Installing Jenkins as a docker image

[An article guiding the setup of jenkins in docker](https://engineering.riotgames.com/news/putting-jenkins-docker-container)

```
docker pull jenkins
docker run -p 8080:8080 --name=jenkins-master jenkins
```

