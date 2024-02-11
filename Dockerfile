FROM harbor2.vantage6.ai/infrastructure/algorithm-base:latest

# install R debian repository
# See: https://cran.r-project.org/bin/linux/debian/#secure-apt
RUN apt update -y \
    && apt install -y --no-install-recommends gnupg \
    && gpg --keyserver keyserver.ubuntu.com \
           --recv-key '95C0FAF38DB3CCAD0C080A7BDC78B2DDEABC47B7' \
    && gpg --armor --export '95C0FAF38DB3CCAD0C080A7BDC78B2DDEABC47B7' > /etc/apt/trusted.gpg.d/cran_debian_key.asc \
    && echo 'deb http://cloud.r-project.org/bin/linux/debian bullseye-cran40/' > /etc/apt/sources.list.d/r-project.list

# install R
RUN apt update -y && apt install -y r-base


# Change this to the package name of your project. This needs to be the same
# as what you specified for the name in the `setup.py`.
ARG PKG_NAME="v6-average-r-py"

# This will install your algorithm into this image.
COPY . /app
RUN pip install /app

# This will run your algorithm when the Docker container is started. The
# wrapper takes care of the IO handling (communication between node and
# algorithm). You dont need to change anything here.
ENV PKG_NAME=${PKG_NAME}
CMD python -c "from vantage6.algorithm.tools.wrap import wrap_algorithm; wrap_algorithm()"
