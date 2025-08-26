### Never send your "passwords" in Production ###

FROM azul/zulu-openjdk:21
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && apt upgrade -y && apt install wget gpg -y
RUN wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | \
    gpg --dearmor -o /usr/share/keyrings/r-project.gpg && \
    echo 'deb [signed-by=/usr/share/keyrings/r-project.gpg] https://cloud.r-project.org/bin/linux/ubuntu jammy-cran40/' | \ 
    tee -a /etc/apt/sources.list.d/r-project.list
RUN apt update && apt install --no-install-recommends nano python3-pip python3-venv \
    r-base r-cran-dplyr r-cran-magrittr r-cran-lubridate r-cran-rjava r-cran-dbi -y 
RUN pip install --upgrade flask-appbuilder python-dotenv pysmb psycopg2-binary pymongo requests cryptography \
    google-api-python-client google-auth-httplib2 google-auth-oauthlib \
    beautifulsoup4 lxml pillow pyarrow unidecode pandas duckdb adbc_driver_manager adbc_driver_postgresql \
    apache-airflow-providers-postgres JayDeBeApi apache-airflow-providers-samba \
    apache-airflow-providers-jdbc \
    'apache-airflow==3.0.4' \
    --constraint 'https://raw.githubusercontent.com/apache/airflow/constraints-3.0.4/constraints-3.10.txt'
RUN R -e 'install.packages(c("dotenv", "RJDBC"))' \
    && mkdir -p /opt/user \
    && groupadd --system airflow \
    && useradd --base-dir /opt/user --system --gid airflow dockerized \
    && chown -R dockerized:airflow /opt/user
USER dockerized
RUN airflow db migrate