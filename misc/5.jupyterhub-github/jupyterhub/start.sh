# adduser --quiet --disabled-password --shell /bin/bash --home /home/jupyter --gecos "User" jupyter
# echo "jupyter:jupyter123" | chpasswd
#
# adduser --quiet --disabled-password --shell /bin/bash --home /home/admin --gecos "User" admin
# echo "admin:A5cwn9YVcqnekR6Y" | chpasswd
#
# mkdir /home/jupyter
# mkdir /home/admin
#
# chown -R jupyter /home/jupyter
# chown -R admin /home/admin
export GITHUB_CLIENT_ID=
export GITHUB_CLIENT_SECRET=
export OAUTH_CALLBACK_URL=
export CONFIGPROXY_AUTH_TOKEN=super-secret
chmod 777 -R /home
jupyterhub -f /app/jupyterhub_config_github.py
