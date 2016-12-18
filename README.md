# paws
Python helpers for using AWS API Gateway / Lambda "serverless"

*heavily WIP*

## Example

```
from paws import http_handler
from paws import response


@http_hander
def index(request):
    return response.Response('Hello, world!', headers={'Content-Type': 'text/plain'})
```

## Setup

When using this framework, there is one assumption made:

- In your API Gateway you have set "multipart/form-data" as a Binary mode content type.
