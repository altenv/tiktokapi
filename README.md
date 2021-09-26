#### Docker Installation

Clone this repository onto a local machine then run the following commands.

```sh
docker build . -t tiktokapi:latest
docker run --rm -p 8080:5000 tiktokapi:latest 
```

## Quick Start Guide

Here's a quick bit of code to get the most recent trending on TikTok. There's more examples in the examples directory.

```py
from TikTokApi import TikTokApi
api = TikTokApi.get_instance()
results = 10

# Since TikTok changed their API you need to use the custom_verifyFp option. 
# In your web browser you will need to go to TikTok, Log in and get the s_v_web_id value.
trending = api.by_trending(count=results, custom_verifyFp="")

for tiktok in trending:
    # Prints the id of the tiktok
    print(tiktok['id'])

print(len(trending))
```

To run the example scripts from the repository root, make sure you use the
module form of python the interpreter

```sh
python3 -m examples.get_trending
python3 api.py
```