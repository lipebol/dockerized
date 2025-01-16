FROM ubuntu:22.04
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && apt upgrade -y && apt install wget gpg -y
RUN wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | \ 
gpg --dearmor -o /usr/share/keyrings/r-project.gpg && \ 
echo 'deb [signed-by=/usr/share/keyrings/r-project.gpg] https://cloud.r-project.org/bin/linux/ubuntu jammy-cran40/' | \ 
tee -a /etc/apt/sources.list.d/r-project.list
RUN apt update && apt install --no-install-recommends nano python3-pip python3-venv \ 
r-base r-cran-dplyr r-cran-magrittr r-cran-lubridate -y 
RUN pip install python-dotenv pysmb psycopg2-binary pymongo requests pyarrow \ 
pandas duckdb adbc_driver_manager adbc_driver_postgresql apache-airflow-providers-postgres \ 
'apache-airflow==2.10.3' \
--constraint 'https://raw.githubusercontent.com/apache/airflow/constraints-2.10.3/constraints-3.10.txt'
RUN airflow db init
RUN airflow users create --username snoopy --firstname Snoopy --lastname Buddy \ 
--role Admin --email snoopy@buddy.regard --password i_miss_you_friend
WORKDIR /root/airflow/
COPY start_scheduler.sh start_scheduler.sh
COPY start_webserver.sh start_webserver.sh
COPY run.sh run.sh
RUN chmod +x ./start_scheduler.sh ./start_webserver.sh ./run.sh && mkdir dags
CMD ["./run.sh"]
