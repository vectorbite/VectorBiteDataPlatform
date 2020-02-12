# VectorByTE WebApp and Database Admin Documentation 

## Getting started: installing software on your Ubuntu Installation and setting up VectorBite Data Platform web-app and database locally (ordinal) 

### Install the following software:

- Python 2.7 (Programming language)
- PyCharm Professional  (Integrated programming development environment for web2py)
- Postgres 9.6 (Relational database management system) inc. Pgadmin4 
- KeepSafe2 (Password manager)
- Git (Version control system)
- Gitkraken (Git GUI Client for managing version control system)
- Filezilla (FTP client for uploading / downloading files to and from server)

### Special installation instructions

You will need to install the most up to date version of filezilla to ensure it works smoothly with AWS. At the time of writing the current release is FileZilla 3.46.3. You will need to adapt this tutorial accordingly for later releases.  

#### Build and install latest version of Filezilla from source:

Install the prerequisites for installing from source:

```
sudo apt install build-essential wx-common libpugixml-dev libsqlite3-dev libwxgtk3.0-dev nettle-dev gnutls-bin libgnutls28-dev
```

Download `libfilezilla-0.19.3` that is needed from https://lib.filezilla-project.org/download.php. *NOTE: Only `libfilezilla-0.11.0` is available in the Ubuntu 18.04 LTS repositories.*

Then extract, build and install:

```
tar -xvjf libfilezilla-0.19.3.tar.bz2 
cd libfilezilla-0.19.3/
./configure
make
sudo make install
```

Now get the source for Filezilla 3.46.3 from https://filezilla-project.org/download.php?show_all=1

Then extract, build and install:

```
tar -vxjf FileZilla_3.46.3_src.tar.bz2 
cd filezilla-3.46.3/
./configure
make
sudo make install
```

With the lib installs you might get the following message if it doesn't start:

> filezilla: error while loading shared libraries: libfilezilla.so.0: cannot open shared object file: No such file or directory

To fix it, simply run

```
sudo ldconfig 
```

You may also find you need to install missing packages before the "make" command will execute,  this is will because you need to install additional packages. You will be informed of which packages are missing after running the "./configure" command. 

### Accounts

Create a GitHub account

### Pycharm:  Create Web2Py project

1. From the main menu, choose File | New Project..., or click the New Project button in the Welcome screen. New Project dialog opens.
2. In the New Project dialog, do the following:
3. Specify project type Web2Py.
4. Specify project location, make the final entry ‘vectorbite’, for example  ‘home/user/PycharmProjects/vectorbite’
5. Next, click Expand the node to expand the Project Interpreter node, and select the new environment or existing interpreter, by clicking the corresponding radio-button.
6. The following steps depend on your choice:
7. New environment using: if this option has been selected, choose the tool to be used to create a virtual environment. To do that, click the list and choose Virtualenv, Pipenv, or Conda.
8. Next, specify the location and base interpreter of the new virtual environment. If necessary, click the Inherit global site-packages and Make available to all projects check boxes.
9. When you configure a project Python interpreter, you need to specify the path to the Python executable in your system. So, before configuring a project interpreter, you need to ensure that you've downloaded Python and installed it in your system and you're aware of a path to it. You can create several project interpreters based on the same Python executable. This is helpful when you need to create different virtual environments for developing different types of applications. For example, you can create one virtual environment based on Python 3.6 to develop Django applications and another virtual environment based on the same Python 3.6 to work with scientific libraries.
10. Existing interpreter: if this option has been selected, choose the desired interpreter from the list, or (if the desired interpreter is not found), click Open and choose the interpreter. See Configure a Python interpreter for details.
11. When PyCharm stops supporting any of the outdated Python versions, the corresponding project interpreter is marked as unsupported Python interpreter
12. Click More settings (More Settings), and specify the following:
13. Application name (leave lank)
14. If necessary, select the Use local Web2Py checkbox. With this checkbox selected, the text field next to this checkbox become enabled. Click the browse button to select Web2Py source folder from your file system.
15. Click Create.
16. PyCharm creates an application and produces specific directory structure, which you can explore in the Project tool window. If there are unsatisfied requirements, PyCharm suggests to resolve or ignore them.

### Install python plugins via pycharm 

To manage Python packages for the project interpreter, select the Project Interpreter page in the project Settings/Preferences or select Interpreter Settings in the Python Interpreter widget.

| Required Packages | Version |
| ----------------- | ------- |
| PyYAML            | 5.1.1   |
| mkdocs            | 1.0.4   |
| psycopg2-binary   | 2.7.    |

### Open Passwords & certificates in KeepSafe2

***TODO: Write a section on syncing Keepsafe database file with AWS and how to access the file***

1. Open KeepSafe
2. Go to file > open and select the ‘**Vectorbyte_KP_Database.kdbx**’ file
3. Log in with provided password
4. Don’t close the app! you’ll need access entries in the next steps

### Grant your personal Github account admin rights from the so you can access/edit the VectorBiteDataPlatform

1. Log in to https://github.com/ using the details found in Keepsafe  ‘GitHub’ > ‘Vectorbite GitHub account’ 
2. In github, go to vectorbite/VectorBiteDataPlatform/settings/access.
3. Click on ‘Invite teams or People’.
4. Add your personal GitHub user name and set to admin.
5. You may need to accept a notification in your own Git-hub account. Log back in to your account and check if you have any notifications pending. If so accept the invitation.   

### Download Vectorbite webapp and initialise git in GitKracken

1. Open Gitkraken and go to -  file > Clone Repo

2. Select GitHub.com

3. In ‘where to clone to’ click on ‘Browse’ to locate the web2py ‘vectorbite’  folder you set up (using pycharm) in previous steps, then navigate to and select the applications folder e.g. 

   ```
   '/home/user/PycharmProjects/vectorbite/web2py/applications/
   ```

4. In ‘Repository to clone’ select ‘VectorBiteDataPlatform’. The Full URL is https://github.com/vectorbite/VectorBiteDataPlatform.

5. Hit ‘Clone this repo’!

### Copy config files to application folder

1. In Keepass2, locate the appconfig.ini file in **Web2py > VectorbiteApplication configuration > advanced – file attachments.**

2. Open the file and save to the private folder located in the ‘VectorBiteDataPlatform’ application folder e.g. 

   ```
   /home/user/PycharmProjects/vectorbite/web2py/applications/VectorBiteDataPlatform/private/
   ```

### Get database dump (back-up) files: Connect to Amazon EC2 file directory using FileZilla and SFTP

You need to set up your connection so you can upload and download files to the AWS server  (database backup files are stored here).

1. Open up Filezilla and KeePass2

2. In Keepass2, locate the  "VectorBite.pem" file in  AWS > "AWS logon,  Public DNS + PEM" >  advanced > file attachments

3. Open the file and save to the private folder in the ‘VectorBiteDataPlatform’ application folder e.g. 

   ```
   '/home/user/PycharmProjects/vectorbite/web2py/applications/VectorBiteDataPlatform/private/' 
   ```

4. In Filezilla, go to Edit (Preferences) > Settings > Connection > SFTP, Click "Add key file”

5. Browse to the location of the "VectorBite.pem" file you just saved and select it.

6. A message box will appear asking your permission to convert the file into ppk format. Click Yes, then give the file a name and store it somewhere.

7. If the new file is shown in the list of Keyfiles, then continue to the next step. If not, then click "Add keyfile..." and select the converted file.

8. File > Site Manager Add a new site with the following parameters:
   - Host: Your public dns name of ec2 instance, or the public ip address of the server. This is found in 

     ```
     Keeppass2 > AWS > "AWS logon,  Public DNS + PEM" >  URL.
     ```

   - Protocol: SFTP

   - Logon Type: Normal

   - User: ubuntu
     
  - Note from the docs: "For Amazon Linux, the default user name is ec2-user. For RHEL5, the user name is often root but might be ec2-user. For Ubuntu, the user name is ubuntu. For SUSE Linux, the user name is root. For Debian, the user name is admin. Otherwise, check with your AMI provider."

9. Press Connect Button - If saving of passwords has been disabled, you will be prompted that the logon type will be changed to 'Ask for password'. Say 'OK' and when connecting, at the password prompt push 'OK' without entering a password to proceed past the dialog.

Note: FileZilla automatically figures out which key to use. You do not need to specify the key after importing it as described above.

### Download Postgres database dump file to load / restore databases 

Next we need to download the database back up files (known as dump files) so we can load the database onto your local machine. 

1. Open Filezilla
2. Connect to the AWS server using log-on details outlined in the previous step
3. Navigate  to /home/ubuntu/vdbp_installation on the remote site. 
4. Download the latest version entitled "fulldump.pgdump". 
5. Search for the latest version of the database  by clicking on last modified. Note that some of the filename  [?] endings will end with slightly different words or letters but will always contain  "fulldump" at the beginning of the file name. 

### Load/restore Postgres database

Required applications: pgAdmin & KeePass2*

You need to create the following group roles before you can restore the databases. 

1. ​	In the left hand pane, go to: ***Servers > PostgreSQL 9.6 > Login/Group Roles***
2. ​	Right click ***> Login/Group Role***
3. ​	General > Name enter username found in ***PostgreSQL 9.6 / pgAdmin 4 > vecdyn login / group role***
4. ​	Definition > Password found in ***PostgreSQL 9.6 / pgAdmin 4 > vecdyn login / group role***
5. ​	Privileges > set all icons to yes
6. ​	Membership > Roles **> add  *"admin" & "postgres"***
7. ​	Hit save
8. ​	Repeat the same step and create a ***"vectraits" login / group role.*** 

Restore Databases (either vecdyn or vectraits)

1. ​	In the left hand pane, go to: ***Servers > PostgreSQL 9.6 > Databases***
2. ​	Right click and ***create > Database***
3. ​	Under the *general >* Database Field write "**vectorbitedb**" and hit save. 
4. ​	Right click on the "**vectorbitedb**" and select Restore.
5. ​	Under file name select the "**vecdyn.dump**" or "**vectraits.dump**" file (you may need to change the format to All Files)
6. ​	Hit **Restore



## Common Tasks and operations

### Connecting to AWS server via SSL using Ubuntu terminal

Open the Keepass2 and adapt the code found in "*AWS SSH connection details > Notes*" to work with your personal paths and directories. 

Example code:

```
sudo ssh -i '/home/matt/web2py/applications/yourapp/yourpem.pem'  ubuntu@ec2-198-51-100-1.compute-1.amazonaws.com 
```

Enter the code in the Ubuntu terminal, if connection has been successful you will receive the following welcome message in the terminal. 

    Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.4.0-1084-aws x86_64)
    
    - Documentation:  https://help.ubuntu.com
    - Management:     https://landscape.canonical.com
    - Support:        https://ubuntu.com/advantage
    
      Get cloud support with Ubuntu Advantage Cloud Guest:
    http://www.ubuntu.com/business/services/cloud

### Backup database (create dump of current version)

To create a backup of the entire database use the following example: 

- Move into the installation folder:

  ```
  cd vdbp_installation/
  ```

- Create the backup

  ```
  /usr/bin/pg_dump --dbname=vectorbitedb --format=c --file=fulldump_[enter-current-date-here].pgdump --username=vbadmin --host=127.0.0.1 --port=5432
  ```

- Confirm the file has been created in the installation folder

  ```
  zip -9 fulldump_120220.zip fulldump_120220.pgdump 
  ```

- You can download all archived files from ec2 to using FileZilla.

### Update local copy of Postgres database

Required applications: pgAdmin & KeePass2*

If they are not already created, you need to create the following group roles

1. ​	In the left hand pane, go to: ***Servers > PostgreSQL 9.6 > Login/Group Roles***
2. ​	Right click ***> Login/Group Role***
3. ​	General > Name enter username found in ***PostgreSQL 9.6 / pgAdmin 4 > vecdyn login / group role***
4. ​	Definition > Password found in ***PostgreSQL 9.6 / pgAdmin 4 > vecdyn login / group role***
5. ​	Privileges > set all icons to yes
6. ​	Membership > Roles **> add  *"admin" & "postgres"***
7. ​	Hit save
8. ​	Repeat the same step and create a ***"vectraits" login / group role.*** 

Restore Databases (either vecdyn or vectraits)

1. ​	In the left hand pane, go to: ***Servers > PostgreSQL 9.6 > Databases***
2. ​	Right click and ***create > Database***
3. ​	Under the *general >* Database Field write "**vectorbitedb**" and hit save. 
4. ​	Right click on the "**vectorbitedb**" and select Restore.
5. ​	Under file name select the "**vecdyn.dump**" or "**vectraits.dump**" file (you may need to change the format to All Files)
6. ​	Hit **Restore**