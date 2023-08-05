import requests
def getRealURL(args):
    if isinstance(args, str):
        return requests.get(args).url
    if isinstance(args, list):
        results = []
        for arg in args:
            results.append(requests.get(arg).url)
        return results