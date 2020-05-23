# AutoPy
A simple script to automate the creation of a project directory with remote GitHub repository

# Getting Started
You will need [PyGithub](https://github.com/PyGithub/PyGithub) installed. Run
```
    $ pip install -r requirements.txt
```
Once you've installed PyGithub you will be able to run the code through running
```
    python autopy.py NAME-OF-YOUR-PROJECT-DIRECTORY
```
Upon running Autopy for the first time you will need to provide you're GitHub username and password along with the default directory that will be used to create your future projects. 
Make sure to insert '/' when providing the deafult director or else an exception will be raised.

# Support
AutoPy currently runs only on MacOS

## Authors
* **George Hanna** - *Initial work* - [GJHanna](https://github.com/GJHanna)

## License
This project is licensed under the Apache 2.0 - see the [LICENSE.md](LICENSE.md) file for details