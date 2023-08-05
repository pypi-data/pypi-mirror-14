import requests
def getRealURL(args):
    if isinstance(args, str):
        try:
            return requests.get(args).url
        except Exception:
            return "Failed"
    if isinstance(args, list):
        results = []
        for arg in args:
            try:
                results.append(requests.get(arg).url)
            except Exception:
                results.append("Failed")
        return results