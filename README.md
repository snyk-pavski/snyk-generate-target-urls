# Get Last Successful Scan date

Outputs projects across multiple Snyk Organisations in a Group together with the date of the last time issue count was updated.

## Features

`get_targets.py` - gathers project information for entire Snyk Orgnisation. Uses [Snyk's REST API](https://apidocs.snyk.io/).


## Configuration

Install dependencies
```sh
pip install -r requirements.txt
```

Update variables in `get_targets.py`. Get the latest API Version from [Snyk's REST API](https://apidocs.snyk.io/)
```py
API_VERSION = "2024-08-15"
RATE_LIMIT_DELAY = 0.2 (in seconds)
```

## Usage

### Gather project information 

Run the script locally

```sh
python3 get_targets.py --group YOUR_GROUP_ID --token your_api_token
```

Script will output multiple json files split by individual Snyk Organisations e.g.`SnykOrg1.json` 



