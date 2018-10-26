## How-to

1. Make sure you installed `Docker-machine` and registered AWS account.
```bash
env
# make sure you have AWS_SECRET_ACCESS_KEY=
# make sure you have AWS_ACCESS_KEY_ID=
```

2. Create 3 EC2 VPS. I live in Malaysia, so I spawned them at Singapore. You can supported regions [here](https://docs.aws.amazon.com/general/latest/gr/rande.html).
```bash
docker-machine create --driver amazonec2 --amazonec2-region ap-southeast-1 tf-master
docker-machine create --driver amazonec2 --amazonec2-region ap-southeast-1 tf-node-1
docker-machine create --driver amazonec2 --amazonec2-region ap-southeast-1 tf-node-2
```

3. SSH our master `tf-master` and install docker-compose,
```bash
docker-machine ssh tf-master
sudo curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

4. Init the swarm,
```bash
sudo docker swarm init
```

You can see it will returned, `docker swarm join --token`, paste this to your all nodes. `tf-node-1`, `tf-node-2`.

```bash
docker-machine ssh tf-node-1
sudo docker swarm join --token
```

Repeat above for all your nodes.

5. Spawn `Docker-Registry` in your master,

Create `/etc/docker/daemon.json` in all our master and nodes,
```text
{ "insecure-registries":["your-ip:5000"] }
```

Restart docker,
```bash
sudo service docker restart
```

Spawn `Docker-Registry`,
```bash
sudo docker service create --name registry --publish published=5000,target=5000 registry:2
```

Go get your Public DNS inside EC2 Panel and curl like this,
```bash
curl http://ec2.ap-southeast-1.compute.amazonaws.com:5000/v2/_catalog
```
```text
{"repositories":[]}
```

6. Build the image inside our local folder,
```bash
docker build .
```

and put tag on it, you required to get the `IMAGE ID`, in my case I got `f80e2d883c9c`
```bash
docker tag f80e2d883c9c ec2.ap-southeast-1.compute.amazonaws.com:5000/flask-inception
docker push ec2.ap-southeast-1.compute.amazonaws.com:5000/flask-inception
```

You can try to curl again,
```bash
curl http://ec2.ap-southeast-1.compute.amazonaws.com:5000/v2/_catalog
```
```text
{"repositories":["flask-inception"]}
```

7. Now create `docker-compose.yml`,
```text
version: '3'

services:
  flask-inception:
    image: your-ip:5000/flask-inception
    ports:
      - "7000:7000"
```

You can try to run it,
```bash
sudo docker-compose -f docker-compose.yml up --build
```
```text
flask-inception_1  |    WARNING: Do not use the development server in a production environment.
flask-inception_1  |    Use a production WSGI server instead.
flask-inception_1  |  * Debug mode: on
flask-inception_1  |  * Running on http://0.0.0.0:7000/ (Press CTRL+C to quit)
flask-inception_1  |  * Restarting with stat
```

Can try to curl it,
```bash
curl -POST -F file=@husein-tiger.jpg http://ec2.ap-southeast-1.compute.amazonaws.com:7000
```
```text
{"label": "soft-coated wheaten terrier", "computer-name": "1f559338678b"}
```

8. Spawn the stack,
```bash
sudo docker stack deploy --compose-file docker-compose.yml inception
```

Give few minutes, and try to request on our master and nodes,
```bash
curl -POST -F file=@husein-tiger.jpg http://master:7000
curl -POST -F file=@husein-tiger.jpg http://node1:7000
curl -POST -F file=@husein-tiger.jpg http://node2:7000
```

All of these should returned value.

Problem here, you want a single API point but has multiple back-ends on it, Nginx is our solution!

9. Deploy Nginx as load-balancer,

kill our stack first,
```bash
sudo docker stack rm inception
```

Get IPs of our nodes and master,
```bash
for NODE in $(sudo docker node ls --format '{{.Hostname}}'); \
do echo -e "${NODE} - $(sudo docker node inspect --format '{{.Status.Addr}}' "${NODE}")"; done
```
```text
tf-master - 172.31.40.167
tf-node-1 - 172.31.46.207
tf-node-2 - 172.31.36.4
```

Create a directory `nginx`,
```bash
mkdir nginx
```

Create a file `load-balancer.conf`,
```text
events { worker_connections 1024; }

http {
	upstream backend {
   		server 172.31.40.167:7000;
   		server 172.31.46.207:7000;
   		server 172.31.36.4:7000;
	}

	server {
   		listen 80;

   		location / {
      			proxy_pass http://backend;
   		}

	}
}
```

Create a file `Dockerfile`,
```text
FROM nginx
COPY load-balancer.conf /etc/nginx/nginx.conf
```

Build the image,
```bash
sudo docker build . -t nginx-inception
```

Now, back to folder where we put our `docker-compose.yml` and edit it,
```text
version: '3'

services:
  flask-inception:
    image: 172.31.40.167:5000/flask-inception
    ports:
      - "7000:7000"

  nginx:
    image: nginx-inception
    ports:
     - "80:80"
```

Stack it!
```bash
sudo docker stack deploy --compose-file docker-compose.yml inception
```

10. Try to request,
```bash
curl -POST -F file=@husein-tiger.jpg http://ec2.compute.amazonaws.com
