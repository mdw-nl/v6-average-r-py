## Notes

### Base images

#### `harbor2.vantage6.ai/infrastructure/algorithm-ohdsi-base:4.2`

* R installed on it
* OHDSI R packages
* Java
* OHDSI python wrappers

#### `r-base:4.3.2`
* It's an "official docker image". \
  See: https://docs.docker.com/trusted-content/official-images/
* Dockerfile actually probably comes from the Rocker project. \
  See: https://github.com/rocker-org/rocker/blob/master/r-base/4.3.2/Dockerfile
* It's however based in debian:testing and installs sid repositories. \
  I'm guessing this is due to its maintainer also maintaining the R packages
  at debian (guess) \
  See:
  https://cran.r-project.org/bin/linux/debian/#debian-sid-unstable-and-experimental

### R dependencies

Installing R seems to pull in a lot more pacakges that we need here (e.g. we
don't need graphical interface capabilities). It also needs a fortran compiler,
g++, gcc, ...  I guess this is the norm in the world of R?
