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
from facebookads import test_config

ad_account_id = test_config.account_id
post_id = fixtures.create_post()['id']

# _DOC open [ADCREATIVE_CREATE_URL_TAG]
# _DOC vars [ad_account_id:s, post_id]
from facebookads.objects import AdCreative

creative = AdCreative(parent_id=ad_account_id)
creative[AdCreative.Field.object_story_id] = post_id
creative[AdCreative.Field.name] = 'Ad Creative with URL tag'
creative[AdCreative.Field.url_tags] = 'key1=val1&key2=val2'

creative.remote_create()
print(creative)
# _DOC close [ADCREATIVE_CREATE_URL_TAG]

creative.remote_delete()
