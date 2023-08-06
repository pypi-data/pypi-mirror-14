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

from facebookads import test_config

ad_account_id = test_config.account_id

# _DOC oncall [pruno]
# _DOC open [ADACCOUNT_GET_CUSTOMAUDIENCES_DATA_SOURCE_SUBTYPE]
# _DOC vars [ad_account_id:s]
from facebookads.objects import AdAccount, CustomAudience

ad_account = AdAccount(ad_account_id)
custom_audiences = ad_account.get_custom_audiences(fields=[
    CustomAudience.Field.data_source,
    CustomAudience.Field.subtype,
])
# _DOC close [ADACCOUNT_GET_CUSTOMAUDIENCES_DATA_SOURCE_SUBTYPE]
