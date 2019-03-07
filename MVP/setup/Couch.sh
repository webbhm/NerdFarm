# Installation of CouchDB
# Set up repository
echo "deb https://apache.bintray.com/couchdb-deb stretch main" | sudo tee -a /etc/apt/sources.list
# Install repository key
curl -L https://couchdb.apache.org/repo/bintray-pubkey.asc | sudo apt-key add -
# Update repository cache
sudo apt-get update 
# install CouchDB
sudo apt-get install couchdb
# install dependencies
sudo apt-get --no-install-recommends -y install build-essential pkg-config erlang libicu-dev libmozjs185-dev libcurl4-openssl-dev

./configure

# Finish Customization of Couch
/home/pi/MVP/CouchInit.sh