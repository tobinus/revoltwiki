############################################
# Dockerfile to run Revoltwiki
# Based on an Ubuntu Image and http://michal.karzynski.pl/blog/2015/04/19/packaging-django-applications-as-docker-container-images/
############################################

# Set the base image to use to Ubuntu
FROM debian:stable

# Set the file maintainer (your name - the file's author)
MAINTAINER Radio Revolt/Thorben Dahl

# Set env variables used in this Dockerfile (adding a unique prefix)
# Local directory with project source
ENV REVOLTWIKI_SRC=.
# Directory in container for all project files
ENV REVOLTWIKI_SRVHOME=/srv
# Directory in container for project source files (Warning: This is duplicated
# in the CMD line below; make sure you change both occurrences)
ENV REVOLTWIKI_SRVPROJ=/srv/revoltwiki

# Install the needed packages
RUN apt-get update && apt-get install -y \
	python3 \
	python3-pip

# Copy in the requirements.txt file separately, so the image can be cached
COPY $REVOLTWIKI_SRC/requirements.txt $REVOLTWIKI_SRVPROJ/

# Install the needed Python packages
RUN pip3 install -r $REVOLTWIKI_SRVPROJ/requirements.txt

# Copy in the revoltwiki source.
# This is likely to cause cache invalidation, so put this as late as possible
COPY $REVOLTWIKI_SRC $REVOLTWIKI_SRVPROJ

# Port to expose
EXPOSE 8000

# Initialize the database file and load testdata
RUN make -C $REVOLTWIKI_SRVPROJ prepare testdata

# Make a volume out of the data directory, in which the database is stored
VOLUME ["$REVOLTWIKI_SRVPROJ/data"]

# Default command to execute.
# By using CMD without ENTRYPOINT, it is possible for users to
# start up a shell to do debugging, manual changes and so on.
# The path to the installation folder is duplicated because variables are not
# supported by the exec form of CMD.
CMD ["/usr/bin/make","-C","/srv/revoltwiki","prepare","run"]
