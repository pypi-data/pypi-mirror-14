import requests
def decodeURL(args):
    if type(args) is str:
        return requests.get(args).url
    if type(args) is list:
        results = []
        for arg in args:
            results.append(requests.get(arg).url)
        return results