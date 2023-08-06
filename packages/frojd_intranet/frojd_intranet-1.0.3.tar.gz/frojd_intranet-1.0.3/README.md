# Frojd-Intranet

This is a cli tool for working with the Fröjd Intranet.

## Requirements

- Python 2.7
- Pip


## Installation

Frojd-Intranet can be installed through pip.

### Stable

`sudo pip install frojd-intranet`


## Getting started

1. Create a config file called .frojd-intranet in your home directory:
	
	```
	{
	    'base_url': 'https://url.to.intranet.se',
	    'username': 'Ernest',
	    'password': 'Hemingway'
	}
	```
2. Now run a test command: `frojd-intranet search --project="My project`
2. Done!


## Usage

#### Search after project:

```
frojd-intranet search --project="My project"
```

Returns:

```
Demo
Stage
Prod
```


#### List all stages containing to project

```
frojd-intranet search --project="My project"
```


Prints:

```
My project
My project 1
```

#### Show stage values

```
frojd-intranet search --project="My project" --stage="Prod"
```

Prints:

```
### SSH
Host: 127.0.0.1
```


### Find field on stage

```
frojd-intranet search --project="My project" --stage="Prod" --search="SSH:Host"
```

Prints:

```
Host: 127.0.0.1
```


## Versioning

We use semantic versioning.


## Contributing

Want to contribute? Awesome. Just send a pull request.


## License

Frojd-Intranet is released under the MIT License.
