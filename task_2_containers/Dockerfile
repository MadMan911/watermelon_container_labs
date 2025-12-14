FROM jupyterhub/jupyterhub:3.1.1

RUN pip install psycopg2-binary

WORKDIR /jupyter

# Создаем директорию для конфигурации
RUN mkdir -p /srv/jupyterhub

ENTRYPOINT ["jupyterhub", "--log-level=INFO"]
