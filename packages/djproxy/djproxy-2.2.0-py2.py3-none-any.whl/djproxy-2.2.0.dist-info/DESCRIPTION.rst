djproxy is a simple reverse proxy class-based generic view for Django apps.

If your application depends on proxies provided by a web server in production,
djproxy can be used to duplicate that functionality during local development.

Home-page: https://github.com/thomasw/djproxy
Author: Thomas Welfley
Author-email: thomas.welfley+djproxy@gmail.com
License: MIT
Description: # djproxy
        
        [![Build Status](https://img.shields.io/travis/thomasw/djproxy.svg)](https://travis-ci.org/thomasw/djproxy)
        [![Coverage Status](https://img.shields.io/coveralls/thomasw/djproxy.svg)](https://coveralls.io/r/thomasw/djproxy)
        [![Latest Version](https://img.shields.io/pypi/v/djproxy.svg)](https://pypi.python.org/pypi/djproxy/)
        [![Downloads](https://img.shields.io/pypi/dm/djproxy.svg)](https://pypi.python.org/pypi/djproxy/)
        
        
        djproxy is a class-based generic view reverse HTTP proxy for Django.
        
        ## Why?
        
        If your application depends on a proxy (to get around Same Origin Policy issues
        in JavaScript, perhaps), djproxy can be used to provide that functionality in
        a web server agnostic way. This allows developers to keep local development
        environments for proxy dependent applications fully functional without needing
        to run anything other than the django development server.
        
        djproxy is also suitable for use in production environments and has been proven
        to be performant in large scale deployments. However, your web server's proxy
        capabilities will be *more* performant in many cases. If you need to use this in
        production, it should be fine as long as upstream responses aren't large.
        Performance can be further increased by aggressively caching upstream responses.
        
        Note that djproxy doesn't currently support websockets because django doesn't
        support them. I will investigate adding websocket support as soon as django
        has it.
        
        ## Installation
        
        ```
        pip install djproxy
        ```
        
        djproxy requires requests >= 1.0.0, django >= 1.4.0 and python >= 2.6.
        
        ## Usage
        
        Start by defining a new proxy:
        
        ```python
        from djproxy.views import HttpProxy
        
        class LocalProxy(HttpProxy):
            base_url = 'https://google.com/'
        ```
        
        Add a url pattern that points at your proxy view. The `url` kwarg will be
        urljoined with base_url:
        
        ```python
        urlpatterns = patterns(
            '',
            url(r'^local_proxy/(?P<url>.*)$', LocalProxy.as_view(), name='proxy')
        )
        ```
        
        `/local_proxy/some/content` will now proxy `https://google.com/some/content/`.
        
        Additional examples can be found here: [views][3], [urls][4].
        
        
        ### HttpProxy configuration:
        
        * `base_url`: The proxy url is formed by
           `urlparse.urljoin(base_url, url_kwarg)`
        * `ignored_upstream_headers`: A list of headers that shouldn't be forwarded
          to the browser from the proxied endpoint.
        * `ignored_request_headers`: A list of headers that shouldn't be forwarded
          to the proxied endpoint from the browser.
        * `proxy_middleware`: A list of proxy middleware to apply to request and
          response data.
        * `pass_query_string`: A boolean indicating whether the query string should be
          sent to the proxied endpoint.
        * `reverse_urls`: An iterable of location header replacements to be made on
          the constructed response (similar to Apache's `ProxyPassReverse` directive).
        * `verify_ssl`: This option corresponds to [requests' verify parameter][1]. It
          may be either a boolean, which toggles SSL certificate verification on or off,
          or the path to a CA_BUNDLE file for private certificates.
        
        ## Adjusting location headers (ProxyPassReverse)
        
        Apache has a directive called `ProxyPassReverse` that makes replacements to
        three location headers: `URI`, `Location`, and `Content-Location`. Without this
        functionality, proxying an endpoint that returns a redirect with a `Location`
        header of `http://foo.bar/go/cats/` would cause a downstream requestor to be
        redirected away from the proxy. djproxy has a similar mechanism which is
        exposed via the `reverse_urls` class variable. The following proxies are
        equivalent:
        
        Djproxy:
        
        ```python
        
        class ReverseProxy(HttpProxy):
            base_url = 'https://google.com/'
            reverse_urls = [
                ('/google/', 'https://google.com/')
            ]
        
        urlpatterns = patterns(
            '',
            url(r'^google/(?P<url>.*)$', ReverseProxy.as_view(), name='gproxy')
        
        ```
        
        Apache:
        
        ```
        <Proxy https://google.com/*>
            Order deny,allow
            Allow from all
        </Proxy>
        ProxyPass /google/ https://google.com/
        ProxyPassReverse /google/ https://google.com/
        ```
        
        ### HttpProxy dynamic configuration and route generation helper:
        
        If you'd like to specify the configuration for a set of proxies, without
        having to maintain specific classes and url routes, you can use
        `djproxy.helpers.generate_routes` as follows:
        
        In `urls.py`, pass `generate_routes` a `configuration` dict to configure a set
        of proxies:
        
        ```python
        from djproxy.urls import generate_routes
        
        configuration = {
            'test_proxy': {
                'base_url': 'https://google.com/',
                'prefix': '/test_prefix/',
            },
            'service_name': {
                'base_url': 'https://service.com/',
                'prefix': '/service_prefix/',
                'verify_ssl': False,
                'append_middlware': ['myapp.proxy_middleware.add_headers']
            }
        }
        
        urlpatterns += generate_routes(configuration)
        ```
        
        Using the snippet above will enable your Django app to proxy
        `https://google.com/X` at `/test_prefix/X` and
        `https://service.com/Y` at `/service_prefix/Y`.
        
        These correspond to the following production Apache proxy configuration:
        ```
        <Proxy https://google.com/*>
            Order deny,allow
            Allow from all
        </Proxy>
        ProxyPass /test_prefix/ https://google.com/
        ProxyPassReverse /test_prefix/ https://google.com/
        
        
        <Proxy https://service.com/*>
            Order deny,allow
            Allow from all
        </Proxy>
        ProxyPass /service_prefix/ http://service.com/
        ProxyPassReverse /service_prefix/ http://service.com/
        ```
        
        `verify_ssl`  and `csrf_exempt` are optional (and default to True), but
        base_url and prefix are required.
        
        `middleware` and `append_middleware` are also optional. If neither are present,
        the default proxy middleware set will be used. If middleware is specified,
        then the default proxy middleware list will be replaced. If
        append_middleware is specified, the list will be appended to the end of
        the middleware set. Use `append_middleware` if you want to add additional
        proxy behaviors without modifying the default behaviors.
        
        ## Proxy middleware
        
        HttpProxys support custom middleware for preprocessing data from downstream
        to be sent to upstream endpoints and for preprocessing response data before
        it is sent back downstream. `X-Forwarded-Host`, `X-Forwarded-For`,
        `X-Forwarded-Proto` and the `ProxyPassRevere` functionality area all implemented
        as middleware.
        
        HttProxy views are configured to execute particular middleware by setting
        their `proxy_middleware` attribute. The following HttpProxy would attach XFF and
        XFH headers, but not preform the ProxyPassReverse header translation or attach
        an XFP header:
        
        ```python
        class ReverseProxy(HttpProxy):
            base_url = 'https://google.com/'
            reverse_urls = [
                ('/google/', 'https://google.com/')
            ]
            proxy_middleware = [
                'djproxy.proxy_middleware.AddXFF',
                'djproxy.proxy_middleware.AddXFH'
            ]
        ```
        
        If you need to write your own middleware to modify content, headers, cookies,
        etc before the content is sent upstream of if you need to make similar
        modifications before the content is sent back downstream, you can write your own
        middleware and configure your view to use it. djproxy contains a [middleware
        template][2] to help you with this.
        
        ## Terminology
        
        It is important to understand the meaning of these terms in the context of this
        project:
        
        **upstream**: The destination that is being proxied.
        
        **downstream**: The agent that initiated the request to djproxy.
        
        ## Contributing
        
        To run the tests, first install development dependencies:
        
        ```
        pip install -r requirements.txt
        ```
        
        If you'd like to test this against a version of Django other than the latest
        supported on your Python version, wipe out the `requirements.txt` installation
        by pip installing your desired version.
        
        Run `nosetests` to execute the test suite.
        
        To automatically run the test suite, flake8, frosted, and pep257 checks whenever
        python files change use testtube by executing `stir` in the top level djproxy
        directory.
        
        To run a Django dev server that proxies itself, execute the following:
        
        ```
        django-admin.py runserver --settings=tests.test_settings --pythonpath="./"
        ```
        
        Similarly, to run a configure Django shell, execute the following:
        
        ```
        django-admin.py shell --settings=tests.test_settings --pythonpath="./"
        ```
        
        See `tests/test_settings.py` and `tests/test_urls.py` for configuration
        information.
        
        [1]:http://docs.python-requests.org/en/latest/user/advanced/?highlight=verify#ssl-cert-verification
        [2]:https://github.com/thomasw/djproxy/blob/master/djproxy/proxy_middleware.py#L32
        [3]:https://github.com/yola/djproxy/blob/master/tests/test_views.py
        [4]:https://github.com/yola/djproxy/blob/master/tests/test_urls.py
        
Platform: UNKNOWN
Classifier: Development Status :: 5 - Production/Stable
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: MIT License
Classifier: Topic :: Software Development :: Libraries
Classifier: Framework :: Django :: 1.4
Classifier: Framework :: Django :: 1.5
Classifier: Framework :: Django :: 1.6
Classifier: Framework :: Django :: 1.7
Classifier: Framework :: Django :: 1.8
Classifier: Framework :: Django :: 1.9
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 2.6
Classifier: Programming Language :: Python :: 2.7
Classifier: Programming Language :: Python :: 3.4
Classifier: Programming Language :: Python :: 3.5
Classifier: Programming Language :: Python :: Implementation :: PyPy
