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

- In your API Gateway you have set "multipart/form-data" as a Binary mode content type.
