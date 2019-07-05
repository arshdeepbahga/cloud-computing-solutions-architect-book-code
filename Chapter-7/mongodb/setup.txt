#Import the public key used by the package management system 
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10 
 
#Create a list file for MongoDB 
echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | 
sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list 
 
#Reload local package database 
sudo apt-get update 
 
#Install MongoDB 
sudo apt-get install -y mongodb-org 
 
#Start MongoDB service 
sudo service mongod start
