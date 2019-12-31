service elasticsearch start
service kibana start
service rabbitmq-server start
supervisord -c supervisord.conf
python3 app.py