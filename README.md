# Encryptly
An attempt to create an end-to-end encrypted messaging platform using Django and Channels, as well as lots of other extraneous stuff.

### Configuration for development:
* Make sure these are installed: `sudo apt-get update && sudo apt-get install -y libxml2-dev libxslt1-dev zlib1g-dev python3-pip memcached mysql-server python-dev python3-dev`
* Create a mysql database named 'encryptly_backend' if it doesn't already exist
* Now, create a file named "credentials.txt" with the username and password used for MySQL running on the localhost. For instance, the contents of the said file might be as follows: `root:password123` - make sure it's in the encryptly directory, as Django will read it on startup in order to try to access the database
* Just to make sure, type `git status` and make sure that the credentials.txt file hasn't been added to the locally changed files list; if it has then your MySQL details will be uploaded to GitHub. The .gitignore file should prohibit this
* Make sure you're in a virtualenv and that you're at the 'encryptly' directory, and type: `pip install -r requirements.txt`
* If you're editing the CSS, make sure you edit assets/encryptly.scss instead of the file in /static/css because your changes will be overwritten if you edit the latter. If you want changes to propogate to the website, run sass on the scss file: `sass --watch encryptly_backend/assets/encryptly.scss:static/css/encryptly.css`
* Take a look a TODO.md if you want to see what still needs to be done.

#### Optional stuff for development:
* File watchers can be configured in PyCharm to execute SCSS when any of the relevant files are modified, django-js-reverse is used to pull relative URLs from urls.py in JavaScript - the relavant JS file for this can be generated each execution using `python manage.py collectstatic_js_reverse` (for which you can add an additional build task, and configure your runserver task to execute it pre-build)
* If you want to compress the CSS so there aren't any duplicated media queries, install NodeJs and NPM, then cd to the encryptly directory, and execute: `npm install grunt --save-dev && npm install grunt-combine-mq --save-dev`. Media queries can then be compressed using `grunt combine_mq`. You can also configure a pre-build task to do this
* Each webpage is configured to use livereloadx in development mode - so if you want to use that, install the livereloadx package, and run it on the Django project root directory, it should work automatically.

### Running with docker:
* In order to test with docker, make sure docker is installed & that the daemon is running, and execute the following (note sudo isn't needed if you're added to the docker usergroup):
`sudo docker run -p 8000:8000 --name encryptly-run -t synchisis/encryptly-docker:latest`
* With this done, `docker start encryptly-run` and `docker stop encryptly-run` can be used respectively to start and stop the instance
* This is not a deployment image and uses the default python webserver instead of a WSGI & nginx proxy. Testing only.
