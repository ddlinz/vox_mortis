FROM ubuntu:focal

# run updates 
RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y gnupg2

# Install miniconda 
RUN curl -LO https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -p /miniconda
RUN rm Miniconda3-latest-Linux-x86_64.sh
ENV PATH=$PATH:/miniconda/condabin:/miniconda/bin
RUN conda update -y conda

# create the app directory
RUN mkdir -p /app
WORKDIR /app

# copy over the conda settings 
COPY vox_environment.yml ./vox_environment.yml
RUN conda env create -f vox_environment.yml
##RUN conda init bash
##RUN echo "conda activate vox_environment" >> ~/.bashrc

# launch the application 
COPY vox ./vox
CMD ["python","-m","vox"]
EXPOSE 5000
