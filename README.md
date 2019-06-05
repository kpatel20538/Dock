# Dock

Dock manages build environments and persistence for x11docker.

Note: This tool will invoke sudo on an as needed basis. 

## Build Instructions
You can install this package with setup.py

```bash
$ python setup.py install
```

## Quick Start
This example generates a working environment for the non-existent image `example/basic`, builds it with docker, 
run it with x11docker. X11docker will spawn an X11 Client to view the newly created image's desktop. 

```bash
$ dock - touch example/basic
$ dock - run example/basic
``` 

To exit from the image desktop, simply log off the desktop as you would for x11docker. 

## Configure Docker Images

To dive into the an image's environment folder (preferred file manager is resolved with xdg-open): 

```bash
$ dock - image example/basic
``` 

Within this folder, the build folder is used as the build context for docker and is the place where the image's 
Dockerfile and image_config.json files are stored.
image_config.json file stores the build/run flags used for the image.
The home folder is default location of where image's home is persisted. 
This can be modified in image_config.json. 

The following are shortcuts to configure Dockerfile and image_config.json, preferred text editor is resolved with xdg-open. 

```bash
$ dock - dockerfile example/basic
$ dock - configfile example/basic
``` 

To dive into the an folder where all environment folder are stored: 

```bash
$ dock - repository
``` 

### Format of image_config.json

image_config.json is an object with three fields

```
x11dockerFlags   :: A list of flags for 'x11docker'
dockerRunFlags   :: A list of flags for 'docker run'
dockerBuildFlags :: A list of flags for 'docker build'  
```

Each flag in image_config.json is subject to python3 templating, meaning curly braces must be escaped as followed

```
{ -> {{
} -> }}
```

and that following values will substituted in. 

```
{image_dir}     :: The path to the image's enviroment directory
{user_home}     :: The path to the current users home directory
{image_tag}     :: The tag of the selected docker image
{default_label} :: The "built-by-dock" label for docker images built by dock  
```

### After Configuration
 
 After configuration, you can simply re-invoke the `run` subcommand to build and run your image.
 Builds are ran on a as-needed basis, and typically invoked if a change in the build files was noted.
 Should the file change occur to quickly for the cache invalidator to notice, one can `--suggest` a new build and throw away 
 the cached version only if necessary.  
 
 ```bash
$ dock - run --suggest example/basic
``` 

## Listing Images
To list all available environments 

```bash
$ dock - images
```

## Move and Copy Images
To Copy/Move from source to destination: 

```bash
$ dock - copy example/srcImage example/targetImage [--only-build]
$ dock - move example/srcImage example/targetImage [--only-build]
```

## Deleting Images
To remove a single image completely: 

```bash
$ dock - remove example/basic
``` 

To prune any dangling images or exited containers:
```bash
$ dock - prune
```  
## Archive and Restore Images
To Archive/Restore from source to destination: 

```bash
$ dock - backup example/basic basic_image
$ dock - restore example/basic2 basic_image.tar.gz
```

## Custom Image Repository
To change the default location where images `$HOME/.local/share/dock`, you can specify from a the new folder through either `--repo` option or the `DOCK_DESKTOP_X11_HOME` environmental variable.  

```bash
$ dock --repo ~/Documents touch example/basic
$ DOCK_DESKTOP_X11_HOME=/opt/repo dock - touch example/basic
```  
