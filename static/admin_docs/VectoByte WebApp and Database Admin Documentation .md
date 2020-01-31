# VectoByte WebApp and Database Admin Documentation 

## First steps: installing software on your Ubuntu Installation and setting up VectorBiteDataPlatform webapp and database locally (ordinal) 

### Install the following software

- Python 2.7 (Programming language)
- PyCharm Professional  (Integrated programming development environment for web2py)
- Postgres 9.6 including Pgadmin4 (Relational database management system)
- KeepSafe2 (Password manager)
- Filezilla (FTP client for uploading / downloading files to and from server)
- Git (Version control system)
- Gitkraken (Git GUI Client for managing version control system)

### Accounts

- Create a GitHub account

### Pycharm:  create Web2Py project

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

    ​

### Open Passwords & certificates in KeepSafe2

1. Open KeepSafe
2. Go to file > open and select the ‘Vectorbyte_KP_Database.kdbx’ file
3. Log in with provided password
4. Don’t close the app! you’ll need access entries in the next steps

### Grant your personal Github account admin rights so you can access/edit the VectorBiteDataPlatform

1. Log in to https://github.com/ using the details found in Keepsafe  ‘GitHub’ > ‘Vectorbite GitHub account’ 
2. In github, go to vectorbite/VectorBiteDataPlatform/settings/access.
3. Click on ‘Invite teams or People’.
4. Add your personal github user name and set to admin.
5. You may need to accept a notification in your own Github account. Log back in to your account and check if you have any notifications pending. If so accept the intivitation.   

### Download Vectorbite webapp and initialise git in GitKracken

1. Open Gitkraken and go to -  file > Clone Repo
2. Select GitHub.com
3. In ‘where to clone to’ click on ‘Browse’ to locate the web2py ‘vectorbite’  folder you set up (using pycharm) in previous steps, then navigate to and select the applications folder e.g. '/home/user/PycharmProjects/vectorbite/web2py/applications/. 
4. In ‘Repository to clone’ select ‘VectorBiteDataPlatform’. The Full URL is https://github.com/vectorbite/VectorBiteDataPlatform.
5. Hit ‘Clone this repo’!

### Copy config files to application folder

1. In Keeppass2, locate the appconfig.ini file Web2py > VectorbiteApplication configuration > advanced – file attachments.
2. Open the file and save to the private folder in the ‘VectorBiteDataPlatform’ application folder e.g. '/home/user/PycharmProjects/vectorbite/web2py/applications/VectorBiteDataPlatform/private/' 

### Connect to Amazon EC2 file directory using FileZilla and SFTP

You need to set up your connection so you can upload and download files to the AWS server  (database backup files are stored here).

Open up Filezilla and KeePass2

In Keeppass2, locate the appconfig.ini file Web2py > VectorbiteApplication configuration > advanced – file attachments.

Open the file and save to the private folder in the ‘VectorBiteDataPlatform’ application folder e.g. '/home/user/PycharmProjects/vectorbite/web2py/applications/VectorBiteDataPlatform/private/' 

In Filezilla, go to Edit (Preferences) > Settings > Connection > SFTP, Click "Add key file”

Browse to the location of your .pem file and select it.

A message box will appear asking your permission to convert the file into ppk format. Click Yes, then give the file a name and store it somewhere.

If the new file is shown in the list of Keyfiles, then continue to the next step. If not, then click "Add keyfile..." and select the converted file.

File > Site Manager Add a new site with the following parameters:

Host: Your public dns name of ec2 instance, or the public ip address of the server

Protocol: SFTP

Logon Type: Normal

User: From the docs: "For Amazon Linux, the default user name is ec2-user. For RHEL5, the user name is often root but might be ec2-user. For Ubuntu, the user name is ubuntu. For SUSE Linux, the user name is root. For Debian, the user name is admin. Otherwise, check with your AMI provider."

Press Connect Button - If saving of passwords has been disabled, you will be prompted that the logon type will be changed to 'Ask for password'. Say 'OK' and when connecting, at the password prompt push 'OK' without entering a password to proceed past the dialog.

Note: FileZilla automatically figures out which key to use. You do not need to specify the key after importing it as described above.

### Download postgres database dump file to load databases 

Next we need to download the database back up files (known as dump files) so we can load the database onto your local machine. 

Open up 

### Load/restore postgres database

