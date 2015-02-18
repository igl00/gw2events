#GW2 Events


![](gw2events_thumb.png)
    
Guild Wars 2 Events is a "World Boss" event timer for your desktop. It strives to maintain the GW2 style while providing
and easy to use timer interface.

You can find a working 64x build here: >Link goes here< 


## To Build the Project

This project will require Python 3 and optionally virtualenv==1.11 and virtualenvwrapper-win==1.1.5


* Create a new virtualenv folder:

```
mkvirtualenv <project_name>
```

* Activate it:

```
workon <project_name>
```

* Clone the GW2Events repository:

```
git clone https://github.com/igl00/gw2events.git
```

* Install the requirements:

```
# pywin32==219 may need to be downloaded manually from:
pip install -r requirements.txt
```

###Compiling the project

* Run pyinstaller(is should be in your PATH):
```
pyinstaller gw2events.spec
```


##Software used

* [PySide](http://qt-project.org/wiki/PySide)
* [PyInstaller](https://github.com/pyinstaller/pyinstaller/wiki)
* [PsUtil](https://pypi.python.org/pypi/psutil)