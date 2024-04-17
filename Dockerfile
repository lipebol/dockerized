FROM ubuntu:22.04
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && apt upgrade -y && apt install wget gpg -y
RUN wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | \ 
gpg --dearmor -o /usr/share/keyrings/r-project.gpg && \ 
echo 'deb [signed-by=/usr/share/keyrings/r-project.gpg] https://cloud.r-project.org/bin/linux/ubuntu jammy-cran40/' | \ 
tee -a /etc/apt/sources.list.d/r-project.list
RUN apt update && apt install --no-install-recommends nano python3-pip r-base r-cran-dplyr r-cran-httr \ 
r-cran-jsonlite r-cran-reticulate r-cran-magrittr r-cran-dotenv -y && pip install 'apache-airflow==2.9.0' \
--constraint 'https://raw.githubusercontent.com/apache/airflow/constraints-2.9.0/constraints-3.10.txt'
RUN mkdir /airflow && export AIRFLOW_HOME=/airflow
RUN airflow db init
RUN airflow users create --username admin --firstname firstname --lastname lastname --role Admin --email admin@domain.org --password ogc48ef
RUN airflow config list --defaults > /airflow/airflow.cfg
COPY start_scheduler.sh start_scheduler.sh
COPY start_webserver.sh start_webserver.sh
COPY run.sh run.sh
RUN chmod +x /start_scheduler.sh /start_webserver.sh /run.sh
CMD ./run.sh