Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Description: ***************
        webtest-aiohttp
        ***************
        
        .. image:: https://badge.fury.io/py/webtest-aiohttp.png
            :target: http://badge.fury.io/py/webtest-aiohttp
            :alt: Latest version
        
        .. image:: https://travis-ci.org/sloria/webtest-aiohttp.png
            :target: https://travis-ci.org/sloria/webtest-aiohttp
            :alt: Travis-CI
        
        webtest-aiohttp provides integration of WebTest with aiohttp.web applications.
        
        Supports aiohttp>=0.21.0.
        
        
        .. code-block:: python
        
            import asyncio
        
            from aiohttp import web
            from webtest_aiohttp import TestApp
        
            loop = asyncio.get_event_loop()
            asyncio.set_event_loop(loop)
        
            app = web.Application(loop=loop)
        
            @asyncio.coroutine
            def hello(request):
                return web.Response(body=json.dumps(
                    {'message': 'Hello world'}
                ).encode('utf-8'), content_type='application/json')
        
            app.router.add_route('GET', '/', handler)
        
        
            def test_hello():
                client = TestApp(app)
                res = client.get('/')
                assert res.status_code == 200
                assert res.json == {'message': 'Hello world'}
        
        Installation
        ============
        ::
        
            pip install webtest-aiohttp
        
        Project Links
        =============
        
        - PyPI: https://pypi.python.org/pypi/webtest-aiohttp
        - Issues: https://github.com/sloria/webtest-aiohttp/issues
        
        Credits
        =======
        
        This code was adapted from Kirill Klenov's `muffin <https://github.com/klen/muffin>`_ library.
        
        License
        =======
        
        MIT licensed. See the bundled `LICENSE <https://github.com/sloria/webtest-aiohttp/blob/master/LICENSE>`_ file for more details.
        
Keywords: webtest-aiohttp webtest aiohttp testing wsgi asyncio
Platform: UNKNOWN
Classifier: Intended Audience :: Developers
Classifier: Environment :: Web Environment
Classifier: License :: OSI Approved :: MIT License
Classifier: Natural Language :: English
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.4
Classifier: Programming Language :: Python :: 3.5
Classifier: Topic :: Software Development :: Testing
