# Singularity CLI

A CLI for the Singularity REST API with some opinionated configuration management for Singularity Requests and Deploys.

## Installation

If you don't use `pipsi`, you're missing out.
Here are [installation instructions](https://github.com/mitsuhiko/pipsi#readme).

After setting up `pipsi` you may need to add the following to your PATH environment variable:

`$HOME/bin:$HOME/.local/bin`

Simply run:

    $ pipsi install .

## Usage

To use it:

`singularity --help`

and

`$ singularity COMMAND --help`

## Global options

```
-h, --singularity-host TEXT  Singularity host url
-k, --insecure               Allow connections to SSL sites without certs (H)
```

## Environment variables

The `--singularity-host` and `--insecure` global options can also be specified and set with the following environment variables:

```
SINGULARITY_URL      Set to the Singularity url
SINGULARITY_INSECURE Set to a truthy/falsey value. (e.g. 0|1|true|false)
```

## Commands

### state

Get the overall state of Singularity in terms of the number of requests, tasks, racks, slaves each broken down various states

### request

Get or update Singularity requests.

#### sync

Synchronize requests and associated deploys from JSON files on the filesystem.  The sync
command can take either a specific file to sync with the `--file` option or a directory
containing a set of files to sync with the `--dir` option.  Each file that is processed
must be a valid JSON file with the following structure:

{
  "request": [SingularityRequest](https://github.com/HubSpot/Singularity/blob/master/Docs/reference/api.md#model-SingularityRequest),
  "deploy": [SingularityDeploy](https://github.com/HubSpot/Singularity/blob/master/Docs/reference/api.md#model-SingularityDeploy)
}


#### bounce

Restart the tasks for a given request

#### delete

Delete the request and stop all tasks associated with it

#### get

Get a request by id

#### list

Get a list of requests by their state

#### instances

Scale the number of tasks running for a given request

#### pause

Pause the request to disallow new deploys against it.  Optionally kill all tasks for the request while paused.

#### run

Run a on-demand or scheduled request now.

#### unpause

Unpause a request that was previously paused

# Examples

## Get the state of Singularity

```
$ singularity -k state
Requests

  Active    Paused    Cooling Down    Pending    Cleaning
--------  --------  --------------  ---------  ----------
       3         1               0          0           0
Tasks

  Active    Scheduled    Overdue    Cleaning    Load Balancer Cleanup
--------  -----------  ---------  ----------  -----------------------
       1            1          0           0                        0
Racks

  Active    Decommissioning    Inactive
--------  -----------------  ----------
       3                  0           0
Slaves

  Active    Decommissioning    Inactive    Unknown
--------  -----------------  ----------  ---------
       6                  0           0          0
```

## Get the list of all requests

```
$ singularity -k request list
Id                 State    Type         Instances    Deploy Id
-----------------  -------  ---------  -----------  -----------
yb-echo            ACTIVE   SERVICE              1            9
yb-on-demand-test  ACTIVE   ON_DEMAND            1            1
test.ondemand      PAUSED   ON_DEMAND            1            1
yb-scheduled-test  ACTIVE   SCHEDULED            1            3
```

## Get the list of all active requests

```
$ singularity -k request list -t active
Id                 State    Type         Instances    Deploy Id
-----------------  -------  ---------  -----------  -----------
yb-echo            ACTIVE   SERVICE              1            9
yb-on-demand-test  ACTIVE   ON_DEMAND            1            1
yb-scheduled-test  ACTIVE   SCHEDULED            1            3
```

## Get the state of a request

```
$ singularity -k request get yb-echo
--------------  ------------------------
Id              yb-echo
State           ACTIVE
Type            SERVICE
Instances       1
Rack Sensitive  False
Load Balanced   False
Owners          [u'dwhite@yieldbot.com']
Deploy Id       9
--------------  ------------------------
```

## Synchronize the state of a request (without a deploy change)

```
$ singularity -k request sync --file ~/src/skeeter/clusters/platform/prd/singularity/yb-echo.json 
syncronized request yb-echo
```

## Synchronize the state of a request (with a deploy change)

```
$ singularity -k request sync --file ~/src/skeeter/clusters/platform/prd/singularity/yb-echo.json 
syncronized request yb-echo
syncronized deploy 10 for request yb-echo
```

## Pause/unpause a request

```
$ singularity -k request pause yb-echo
paused request yb-echo with killTasks=False

$ singularity -k request get yb-echo
--------------  ------------------------
Id              yb-echo
State           PAUSED
Type            SERVICE
Instances       1
Rack Sensitive  False
Load Balanced   False
Owners          [u'dwhite@yieldbot.com']
Deploy Id       10
--------------  ------------------------

$ singularity -k request unpause yb-echo
unpaused request yb-echo

$ singularity -k request get yb-echo
--------------  ------------------------
Id              yb-echo
State           ACTIVE
Type            SERVICE
Instances       1
Rack Sensitive  False
Load Balanced   False
Owners          [u'dwhite@yieldbot.com']
Deploy Id       10
--------------  ------------------------
```

## Scale a request

```
$ singularity -k request instances yb-echo 2
setting instances to 2 for request yb-echo

$ singularity -k request get yb-echo
--------------  ------------------------
Id              yb-echo
State           ACTIVE
Type            SERVICE
Instances       2
Rack Sensitive  False
Load Balanced   False
Owners          [u'dwhite@yieldbot.com']
Deploy Id       10
--------------  ------------------------

$ singularity -k request instances yb-echo 1
setting instances to 1 for request yb-echo

$ singularity -k request get yb-echo
--------------  ------------------------
Id              yb-echo
State           ACTIVE
Type            SERVICE
Instances       1
Rack Sensitive  False
Load Balanced   False
Owners          [u'dwhite@yieldbot.com']
Deploy Id       10
--------------  ------------------------
```

## Bounce a request (restarts all tasks for the request)

```
$ singularity -k request bounce yb-echo
bounced request yb-echo
```

# TODO

- Tests, tests, tests...
- Flesh out remaining cli commands based on what's available in the [Singularity API](https://github.com/HubSpot/Singularity/blob/master/Docs/reference/api.md)
