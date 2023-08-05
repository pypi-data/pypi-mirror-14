README

TODO


Development:

#create virtaul machine and provision it
vagrant up
#reload to apply new kernel with aufs support
vagrant reload
vagrant ssh
cd source
#build docker-in-docker images for tests
. dev/build_dockers.sh
#run tests
py.test -v -r a tests/
#run test with different pythons
tox
