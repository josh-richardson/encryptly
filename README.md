# wad2-teamproject

Before running the application from PyCharm, a few things are required:
* Make sure these are installed: `sudo apt-get install -y libxml2-dev libxslt1-dev zlib1g-dev python3-pip`
* Make sure you're in a virtualenv and that you're at the 'encryptly' directory, and type: `pip install -r requirements.txt`
* Next, MySQL must be running on the local machine. To do this, install MySQL: `sudo apt-get update && sudo apt-get install mysql-server`
* Create a database named 'encryptly_backend' if it doesn't already exist
* Now, create a file named "credentials.txt" with the username and password used for MySQL running on the localhost. For instance, the contents of the said file might be as follows: `root:password123` - make sure it's in the encryptly directory, as Django will read it on startup in order to try to access the database.
* Just to make sure, type `git status` and make sure that the credentials.txt file hasn't been added to the locally changed files list; if it has then your MySQL details will be uploaded to GitHub. The .gitignore file should prohibit this.
* If you're editing the CSS, make sure you edit assets/encryptly.scss instead of the file in /static/css because your changes will be overwritten if you edit the latter. If you want changes to propogate to the website, run SCSS on the scss file.
* If you want to compress the CSS so there aren't any duplicated media queries, install NodeJs and NPM, then cd to the encryptly directory, and execute: `npm install grunt --save-dev && npm install grunt-combine-mq --save-dev`
* You'll now be able to run grunt which will optimize the css according to the routine in gruntfile.js. Optionally, afterwards, you can configure a pre-build task to run grunt 
