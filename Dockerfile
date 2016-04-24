FROM ubuntu:latest
RUN apt-get -y -q update; \
    apt-get -y -q install wget make ant g++ software-properties-common
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y wget
RUN apt-get install -y autoconf build-essential cmake docbook-mathml docbook-xsl libboost-dev libboost-thread-dev libboost-filesystem-dev libboost-system-dev libboost-iostreams-dev libboost-program-options-dev libboost-timer-dev libcunit1-dev libgdal-dev libgeos++-dev libgeotiff-dev libgmp-dev libjson0-dev libjson-c-dev liblas-dev libmpfr-dev libopenscenegraph-dev libpq-dev libproj-dev libxml2-dev xsltproc git build-essential wget 
# Install gdal dependencies provided by Ubuntu repositories
RUN apt-get install -y -q \
    mysql-server \
    mysql-client \
    python-numpy \
    libpq-dev \
    libpng12-dev \
    libjpeg-dev \
    libgif-dev \
    liblzma-dev \
    libcurl4-gnutls-dev \
    libxml2-dev \
    libexpat-dev \
    libxerces-c-dev \
    libnetcdf-dev \
    netcdf-bin \
    libpoppler-dev \
    gpsbabel \
    swig \
    libhdf4-alt-dev \
    libhdf5-serial-dev \
    libpodofo-dev \
    poppler-utils \
    libfreexl-dev \
    unixodbc-dev \
    libwebp-dev \
    libepsilon-dev \
    liblcms2-2 \
    libpcre3-dev \
    python-dev

#install geos
RUN wget -O - http://download.osgeo.org/geos/geos-3.4.2.tar.bz2 | tar -jx
RUN cd /geos-3.4.2; ./configure --enable-python && make && make install

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]