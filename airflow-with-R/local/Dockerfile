### Never send your "passwords" in Production ###

FROM ubuntu:22.04
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && apt upgrade -y && apt install wget gpg -y
RUN wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | \ 
gpg --dearmor -o /usr/share/keyrings/r-project.gpg && \ 
echo 'deb [signed-by=/usr/share/keyrings/r-project.gpg] https://cloud.r-project.org/bin/linux/ubuntu jammy-cran40/' | \ 
tee -a /etc/apt/sources.list.d/r-project.list
RUN apt update && apt install --no-install-recommends nano python3-pip python3-venv openjdk-21-jdk \ 
r-base r-cran-dplyr r-cran-magrittr r-cran-lubridate r-cran-rjava r-cran-dbi -y 
RUN pip install python-dotenv pysmb psycopg2-binary pymongo requests pyarrow unidecode \ 
pandas duckdb adbc_driver_manager adbc_driver_postgresql apache-airflow-providers-postgres \ 
JayDeBeApi apache-airflow-providers-samba apache-airflow-providers-jdbc \ 
'apache-airflow==2.10.5' \
--constraint 'https://raw.githubusercontent.com/apache/airflow/constraints-2.10.5/constraints-3.10.txt'
RUN R -e 'install.packages(c("dotenv", "RJDBC"))'
WORKDIR /root/airflow/
COPY ./scripts/scheduler.sh scheduler.sh
COPY ./scripts/webserver.sh webserver.sh
COPY ./scripts/run.sh run.sh
RUN airflow db init
RUN chmod +x scheduler.sh webserver.sh run.sh && mkdir dags