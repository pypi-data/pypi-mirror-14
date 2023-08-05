# CLI

ObjDiff provides a simple cli program for comparison of 2 yaml files and 
providing the deltas between them. this is mainly for verification of the 
concept but may be useful in scripting or in validating changes.

to invoke this utility, ensure that the following modules are installed

 * objdiff
 * pyyaml
 * blessings

Color output is provided by the `blessings` module and is suppressed 
automatically if stdout is not a tty for use in scripting.

Python can now be told to invoke the CLI program via the `-m` flag as so

    $ python -m objdiff file1.yml file2.yml

Argument validation is minimal due to its status as a test program but should 
work as expected with 2 file arguments of valid yaml

The source repository contains 2 test yaml files from another project that can 
be used to see the library in action: infrastructure-1.yml and 
infrastructure-2.yml

    $ python -m objdiff infrastructure-1.yml infrastructure-2.yml
    ! url_base: http://jayc.beta.anchortrove.com.au => http://images.pocketnix.org
    ! long_name: test cluster => Pocketnix.org test cluster
    ! short_name: test_cluster => pocketnix
    ! environ.ENVIROMENT: staging => production
    ! instances.elasticsearch_lb.overlays: ['images/debian-2014030301.tar.gz', 'images/elasticsearch.tar.gz', 'keys/ssh.tar.gz', 'setup/elasticsearch_setup.tar.gz', 'setup/debian.tar.gz'] => ['images/debian-2014030301.tar.gz', 'images/elasticsearch.tar.gz', 'keys/ssh.tar.gz', 'setup/elasticsearch_lb_setup.tar.gz', 'setup/debian.tar.gz']
    + instances.elasticsearch_lb.count 2
    + instances.webservers {'count': 3, 'overlays': ['images/debian-2014030301.tar.gz', 'images/nginx.tar.gz', 'keys/ssh.tar.gz', 'setup/nginx.tar.gz', 'setup/debian.tar.gz'], 'mem': '300MB', 'long_name': 'Pocketnix.org Webservers', 'cpus': 4}
    + instances.elasticsearch_data {'count': 10, 'overlays': ['images/debian-2014030301.tar.gz', 'images/elasticsearch.tar.gz', 'keys/ssh.tar.gz', 'setup/elasticsearch_setup.tar.gz', 'setup/debian.tar.gz'], 'mem': '300MB', 'long_name': 'Elastic Search Data nodes', 'cpus': 4}
    
