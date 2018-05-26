# paws
Python helpers for using AWS API Gateway / Lambda "serverless"

*heavily WIP*

## Example

```
from paws import views


class IndexView(views.View):

    def get(request):
        return response.Response('Hello, world!', headers={'Content-Type': 'text/plain'})

index = IndexView()

```

## Setup

When using this framework, there is one assumption made:

- In your API Gateway you have set "multipart/form-data" as a Binary mode
  content type.


## Testing

To help with testing, `paws.wsgi` helps implement a WSGI to API-Gateway/Lambda
integration gateway.

```
from paws import wsgi

from .views import index

application = wsgi.Application([
    (r'^/$', index),
])
```

Any named regex groups will be passed as `\**kwargs` to dispatch.
