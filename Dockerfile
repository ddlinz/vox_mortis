FROM ubuntu:focal

# run updates #
RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y gnupg2

# Install miniconda #
RUN curl -LO https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -p /miniconda
RUN rm Miniconda3-latest-Linux-x86_64.sh
ENV PATH=$PATH:/miniconda/condabin:/miniconda/bin
RUN conda update -y conda

# create the app directory #
RUN mkdir -p /app
WORKDIR /app

# copy over the conda settings #
COPY vox_environment.yml ./vox_environment.yml
RUN conda env create -f vox_environment.yml
RUN conda install gunicorn
RUN conda install flask
RUN conda install -c conda-forge flask-sqlalchemy
RUN conda init bash
RUN echo "conda activate vox_environment" >> ~/.bashrc
SHELL ["conda", "run", "-n", "vox_environment", "/bin/bash", "-c"]

RUN pip install --upgrade flask-sqlalchemy

# launch the application #
COPY vox ./vox
# CMD ["python","-m","vox"]
# EXPOSE 5000

COPY start_gunicorn.sh .
#RUN bash start_gunicorn.sh
ENTRYPOINT ["bash", "/app/start_gunicorn.sh" ]