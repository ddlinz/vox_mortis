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

RUN mkdir -p /app
WORKDIR /app

COPY vox ./vox
CMD ["python","-m","vox"]
EXPOSE 5000
