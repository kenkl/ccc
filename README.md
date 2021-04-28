#  Cert Checker CLI (CCC)

Whilst working on another project that sweeps through a list of SSL/TLS endpoints, I had the need to exercise the calls I was making in isolation from all the other preamble in the project - just give it a hostname/port and see what it returns (I was chasing an interesting bug). It turned out to be more generally useful, independent of the project that inspired it, so I decided to make it a standalone utility.

ccc.py uses pyOpenSSL (see requirements.txt) to retrieve a certificate presented by an endpoint and shows its issuer, issue date, and expiration date. 

Also present is a BASH script - ccc - that serves as a wrapper for ccc.py, setting the working directory, activating the Python venv (which lives in .venv, but not included here, of course), and passing all parameters to ccc.py

For context: on my workstation, I symlink the ccc directory where it lives to /usr/local/bin/ccc and then add it to $PATH, making the utility always available.
