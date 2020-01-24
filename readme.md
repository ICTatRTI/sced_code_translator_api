## SCED Course Code Translator API

This is a flask app that provides an interface to a translate SCED codes from previous SCED versions into their version 7.0 equivalents                                                  .

## Local Use

The API is available through a docker container. 

1. You'll first have to build the container with `$ docker build -t self/sced-code-translator <repository-folder>`
2. Run the container with `docker run -d -p 8080:8080 self/sced-code-translator`. Change the second port `8080` to whatever port you want to expose the API on.
3. Test with curl:

 ```bash
 curl -d '{"sced_code":"00108"}' -H "Content-Type: application/json" -X POST http://localhost:8080/sced-v7-translate/
 ```

## Response Structure

```json
{
    "description" : "This description",
    "submitted_data" : {
        "structure" : {
            "sced_code" : "5 digit SCED code to translate to SCED v7"
        }
    },
    "info" : {
        "structure" : {
            "time_elapsed" : "time it took to calculate prediction and build response",
            "warning": "A warning if archived SCED code could not be crosswalked to v7"
        }
    },
    "translated_codes" : {
        "description" : "Array of equivalent SCED v7 codes, each with structure below",
        "structure" : {
            "sced_code": "SCED course code",
            "course_title": "SCED course title/name",
            "course_description": "SCED course description",
            "archive_status": "Whether code is archived or not",
            "v7_subsitutes": "For archived codes, list of v7 codes that are equivalent",
            "archived_versions": "For active v7 codes, list of equivalent archived codes from previous SCED versions",
            "warnings": "warns when archived code could not be crosswalked to a SCED v7 code"
        }
    }
}
```
## OLD Local Use (Python Environment)

Create a virtual environemnt, activate it, and install requirements from pip.

`$ pip install -r requirements.txt`

Then, startup the application with:

`$ flask run` 

Then, test with `curl`:

`$ curl -d '{"sced_code"":"50779"}' -H "Content-Type: application/json" -X POST http://localhost:23432/sced-v7-translate/`

Or use something like [Insomnia](https://insomnia.rest/).

## Tests

To run tests use:

`$ python tests.py`

## Misc

Set environment variables by doing the following (assuming your .env contains the right variables):

`$ set -a; source .env`