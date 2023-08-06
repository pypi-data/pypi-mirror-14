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
from facebookads.exceptions import DocsmithSkipTestError

# Excluded from runtime
raise DocsmithSkipTestError(
    "Requires a pre-existing"
    " custom audience with 100+ users in a country.")

ad_account_id = test_config.account_id
seed_audience_id = fixtures.create_custom_audience().get_id()

# _DOC oncall [ritu]
# _DOC open [LOOKALIKE_CREATE]
# _DOC vars [ad_account_id:s, campaign_id:s, seed_audience_id:s]
from facebookads.objects import CustomAudience

lookalike = CustomAudience(parent_id=ad_account_id)
lookalike.update({
    CustomAudience.Field.name: 'My lookalike audience',
    CustomAudience.Field.subtype: CustomAudience.Subtype.lookalike,
    CustomAudience.Field.origin_audience_id: seed_audience_id,
    CustomAudience.Field.lookalike_spec: {
        'type': 'similarity',
        'country': 'US',
    },
})

lookalike.remote_create()
print(lookalike)
# _DOC close [LOOKALIKE_CREATE]

lookalike.remote_delete()
