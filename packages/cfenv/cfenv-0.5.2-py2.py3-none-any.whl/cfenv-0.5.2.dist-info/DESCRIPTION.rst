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

Description: ========
        py-cfenv
        ========
        
        .. image:: https://img.shields.io/pypi/v/cfenv.svg
            :target: http://badge.fury.io/py/cfenv
            :alt: Latest version
        
        .. image:: https://img.shields.io/travis/jmcarp/py-cfenv/master.svg
            :target: https://travis-ci.org/jmcarp/py-cfenv
            :alt: Travis-CI
        
        **py-cfenv** is a tiny utility that simplifies interactions with Cloud Foundry environment variables, modeled after node-cfenv_.
        
        Quickstart
        ----------
        
        .. code-block:: python
        
            from cfenv import AppEnv
        
            env = AppEnv()
            env.name  # 'test-app'
            env.port  # 5000
        
            redis = env.get_service('redis')
            redis.credentials  # {'url': '...', 'password': '...'}
            redis.get_url(host='hostname', password='password', port='port')  # redis://pass:host
        
        .. _node-cfenv: https://github.com/cloudfoundry-community/node-cfenv/
        
Keywords: cloud foundry
Platform: UNKNOWN
Classifier: Development Status :: 2 - Pre-Alpha
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: MIT License
Classifier: Natural Language :: English
Classifier: Programming Language :: Python :: 2
Classifier: Programming Language :: Python :: 2.7
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.3
Classifier: Programming Language :: Python :: 3.4
Classifier: Programming Language :: Python :: 3.5
