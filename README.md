# wad2-teamproject

Before running the application from PyCharm, a few things are required:
* Precursor: make sure you're in your virtualenv and that you're using python3.
* Firstly, open a terminal, focus to the 'encryptly' directory, and type: `pip install -r requirements.txt`
* Next, MySQL must be running on the local machine. To do this, install MySQL: `sudo apt-get update && sudo apt-get install mysql-server`
* Now, create a file named "credentials.txt" with the username and password used for MySQL running on the localhost. For instance, the contents of the said file might be as follows:
`root:password123` - make sure it's in the encryptly directory, as Django will read it on startup in order to try to access the database.
* Just to make sure, type `git status` and make sure that the credentials.txt file hasn't been added to the locally changed files list; if it has then your MySQL details will be uploaded to GitHub. The .gitignore file should prohibit this.
Side note: GitHub, why the fuck can't I write this fucking readme in LaTeX? Jesus christ. Markdown sucks.
