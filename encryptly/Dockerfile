#PyCharm is telling me I suck at dockerfiles. It's probably true.
from python:3.5
run apt-get update
RUN ["/bin/bash", "-c", "debconf-set-selections <<< 'mysql-server mysql-server/root_password password test123'"]
RUN ["/bin/bash", "-c", "debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password test123'"]
EXPOSE 8000
EXPOSE 47466
RUN apt-get install -y libxml2-dev libxslt1-dev zlib1g-dev mysql-server mysql-server memcached
ADD . /
RUN pip install -r requirements.txt
RUN /bin/bash
RUN ls
CMD ["/bin/bash", "-c", "/initiate.sh"]
