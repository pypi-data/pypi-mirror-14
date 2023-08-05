========
Usage
========

To use zuup::

    zuul --help      
    usage: zuul [-h] [-D] [-d] [-w DELAY] [-e EXPIRATION] [-u USERNAME]
                [-p PROJECTS] [-c CHANGES] [-l] [-r] [-s] [-j JOB]

    optional arguments:
      -h, --help     show this help message and exit
      -D             Daemonize and exit if no more reviews
      -d             Daemonize
      -w DELAY       refresh delay
      -e EXPIRATION  review expiration in deamon mode
      -u USERNAME    Username
      -p PROJECTS    Projects
      -c CHANGES     changes
      -l             local changes
      -r             current repo changes
      -s             short output
      -j JOB         show log of a job of a change

