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
page_id = test_config.page_id
product_set_id = fixtures.create_product_set().get_id()
campaign_id = fixtures.create_campaign().get_id()
link = test_config.app_url

# _DOC open [ADCREATIVE_CREATE_DPA_CAROUSEL]
# _DOC vars [ad_account_id:s, page_id, link:s, product_set_id]
from facebookads.objects import AdCreative
from facebookads.specs import ObjectStorySpec

story = ObjectStorySpec()
story[story.Field.page_id] = page_id
story[story.Field.template_data] = {
    'message': 'Test {{product.name | titleize}}',
    'link': link,
    'name': 'Headline {{product.price}}',
    'description': 'Description {{product.description}}',
}

creative = AdCreative(parent_id=ad_account_id)
creative[AdCreative.Field.name] = 'Dynamic Ad Template Creative Sample'
creative[AdCreative.Field.object_story_spec] = story
creative[AdCreative.Field.product_set_id] = product_set_id
creative.remote_create()
# _DOC close [ADCREATIVE_CREATE_DPA_CAROUSEL]

creative.remote_delete()
