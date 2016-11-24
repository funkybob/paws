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
