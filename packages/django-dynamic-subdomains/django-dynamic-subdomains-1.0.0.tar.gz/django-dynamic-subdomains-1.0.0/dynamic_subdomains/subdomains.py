class subdomain(dict):
    def __init__(self, regex, urlconf, name, callback='dynamic_subdomains.utils.noop'):
        self.update({
            'regex': regex,
            'urlconf': urlconf,
            'name': name,
            'callback': callback,
        })
