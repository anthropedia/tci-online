git_update="git fetch origin master && git reset --hard FETCH_HEAD"

help:
	return "Make tasks for deployment. Checkout the makefile content."

deploy:
	ssh epidaurus "cd ~/tci-online && " ${git_update}
	ssh epidaurus "cd ~/tci-compose && docker-compose -p tci restart online"
