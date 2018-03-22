================================================
		 NoSQL Cassandra project
			  Spotify clone
================================================

The source code is avaliable for both version of python 2.x and 3.x 

Source code included:
	add_metadata.py
	add_profile.py
	application_exception.py
	create_account.py
	currently_playing.py
	home.py
	last_played.py
	login.py
	play.py
	playlist.py
	search.py
	setup.py
	top_hits.py


Other files:
	songs
	todays_hits

################################################

Demo Link:  https://www.youtube.com/watch?v=_5tlgr4V5e8

################################################


Steps to run the application:

To start the application Cassandra must be insatalled in the machine along with the 
Cassandra python driver. 

To install Cassandra:
Mac - https://www.datastax.com/2012/01/working-with-apache-cassandra-on-mac-os-x
Windows - https://www.datastax.com/2012/01/getting-started-with-apache-cassandra-on-windows-the-easy-way
Linux - https://www.digitalocean.com/community/tutorials/how-to-install-cassandra-and-run-a-single-node-cluster-on-a-ubuntu-vps


Cassandra python driver : https://github.com/datastax/python-driver

################################################

To start the application:

Run setup.py to create keyspaces, tables and make initial setup (installation)

Then run login.py

Create a new account to login and explore the features like todays hits, last played, searching a song, creating playlist, 
adding song to playist and currently playing.

Refer Applciation_woking_example.txt  and demo for more details.
