git_update="git fetch origin master && git reset --hard FETCH_HEAD"

help:
	return "Make tasks for deployment. Checkout the makefile content."

server_update:
	ssh anthropedia "cd ~/webapps/tci_online && " ${git_update}

deploy: server_update
