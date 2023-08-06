# Copyright 2014 Facebook, Inc.

# You are hereby granted a non-exclusive, worldwide, royalty-free license to
# use, copy, modify, and distribute this software in source code or binary
# form for use in connection with the web services and APIs provided by
# Facebook.

# As with any software that integrates with the Facebook platform, your use
# of this software is subject to the Facebook Developer Principles and
# Policies [http://developers.facebook.com/policy/]. This copyright notice
# shall be included in all copies or substantial portions of the software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from examples.docs import fixtures

ad_set_id = fixtures.create_adset().get_id_assured()

# !_DOC [duliomatos]
# _DOC open [ADSET_READ_WITH_DATE_FORMAT]
# _DOC vars [ad_set_id]
from facebookads.objects import AdSet

adset = AdSet(fbid=ad_set_id)
fields = [
    AdSet.Field.start_time,
]
params = {
    'date_format': 'U',
}
adset.remote_read(fields=fields, params=params)
print(adset[AdSet.Field.start_time])
# _DOC close [ADSET_READ_WITH_DATE_FORMAT]
