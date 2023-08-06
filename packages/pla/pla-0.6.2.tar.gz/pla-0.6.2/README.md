# Pla

Pla helps you automate workflows in a very simple way. Much like make, but with a yaml file structure.

It's a coder's simplest workflow automation tool.

[![Build Status](https://travis-ci.org/rtuin/pla.svg?branch=master)](https://travis-ci.org/rtuin/pla)

## Install

Pla requires Python 2.x. 
Use the pip installer to install Pla.

``` bash
$ (sudo) pip install pla
```

If pip is not present on your system:
```
$ sudo easy_install pip
```

_**Note:** OS X Users reported that [Homebrew](http://brew.sh/)'s version of Python works better than the stock one._

### Upgrade an existing installation

When installed with Pip you can upgrade to the latest version using:
```shell
$ (sudo) pip install pla --upgrade
```

### Install from git
To install Pla from git you first need to make sure Pla is uninstalled. Then you must clone the repository and install 
the development version:

```shell
$ pip uninstall pla
$ git clone git@github.com:rtuin/pla.git
$ cd pla
$ pip install -e .
```

## Usage

```shell
$ pla [target]
```

If you do not provide a target, the default target called `all` will run.

## Start working with Pla

Pla works similar to [Make](https://www.gnu.org/software/make/). You define the targets in a Yaml file called `Plafile.yml`
and run the targets from the command line.

Lets say we use Pla to kickstart our working day. We will make a Plafile which starts our local dev server, starts our IDE
 and opens the application we're working on in the browser.
 
First create the Plafile with a target called `dev`:

```yaml
# Plafile.yml
dev:
  - docker-compose up -d
  - pstorm .
  - open http://local.project.url/
```

Then simply run Pla from the command line:
```bash
$ pla dev
```

Pla will then run the shell commands you specified in the Plafile.

### About the current working directory

Pla will use the directory of the Plafile as its current working directory. As of v0.6 Pla looks for the
Plafile.yml in the parent directory if there is none in the directory that you're running Pla from.

For example, let's say this is your project file structure:
```
your-project/
├── Plafile.yml
└── subdirectory
    └── somefile
```

And this is your Plafile.yml:

```yaml
test:
  - echo $(pwd); exit 1
```

When you run Pla from the project root (where the Plafile.yml is), you will see this:

```
rtuin at localhost in ~/your-project
$ pla test
Pla master by Richard Tuin - Coder's simplest workflow automation tool.

Running target "test":
    ✘ echo $(pwd); exit 1:
        /Users/rtuin/projects/your-project
```

And when you run Pla from the subdirectory, you will see this:

```
rtuin at localhost in ~/your-project/subdirectory
$ pla test
Pla master by Richard Tuin - Coder's simplest workflow automation tool.

Running target "test":
    ✘ echo $(pwd); exit 1:
        /Users/rtuin/projects/your-project
```

## Features

### Linking targets

As of Pla v0.2 it is possible to let your targets call each other. This is simply done by refering to the target 
prepended with an `=` sign. Like so:

```yaml
# Plafile.yml
up:
  - docker-compose up -d
  - =updatecode
  - pstorm .
  - open http://local.project.url/
  
updatecode:
  - git submodule update --init --recursive
  - composer install
```

### Target parameters

Pla v0.3 gives you the ability to variables in target commands. This feature is called target parameters.
 
Simply define the parameters in the target definition, and put them in your command. Enclosing the parameters name with 
`%` signs. For example:

```yaml
# Plafile.yml
pr[number]:
  - git pr %number%
  - git pull upstream master
```

You can then call the target like this:

```bash
$ pla pr 123
```

  **Disclaimer** The current implementation of target parameters is built to work only when you directly call the
  parametrized target.
  
### Command OS filter

When you run the same Pla target on multiple operating systems you might want to specify which command to execute on what OS.
You can do this by prefixing your command with a filter that indicates the OS's family name.
 
```yaml
# Plafile
os:
  - (darwin) echo "Mac OS"
  - (redhat) echo "RedHat family"
  - (ubuntu|darwin) echo "Ubuntu or Mac OS"
  - (debian) echo "Debian"
```

If you run `pla os` on a Mac, you'll get the following output:
```
Running target "os":
    ✔ (darwin) echo "Mac OS"
    . (redhat) echo "RedHat family"
    ✔ (ubuntu|darwin) echo "Ubuntu or Mac OS"
    . (debian) echo "Debian"
```

**Operating systems matches**

| System/Family | Match   |
|---------------|---------|
| Linux         | linux   |
| Ubuntu        | ubuntu  |
| Red Hat       | redhat  |
| Mac OS        | darwin  |
| Windows       | windows |

### Target descriptions

Sometimes you want insight in which part of the Plafile is running. You can do this by giving targets descriptions.
A description can be added in the form of a comment on the same line as the target definition, like so:

```yaml
targetname: # Echo sleep and echo
  - echo "ohai"
  - sleep 1
  - echo "bar"
```

This will generate the following output:

```
$ pla targetname
Pla master by Richard Tuin - Coder's simplest workflow automation tool.

Running target "targetname":
  Echo sleep and echo
    ✔ echo "ohai"
    ✔ sleep 1
    ✔ echo "bar"
```

## Changelog

All notable changes are documented in the [changelog file](CHANGELOG.md).

## Credits

- [Richard Tuin](https://github.com/rtuin)
- [All Contributors](../../contributors)

## License

The MIT License (MIT). Please see the [license file](LICENSE) for more information.
