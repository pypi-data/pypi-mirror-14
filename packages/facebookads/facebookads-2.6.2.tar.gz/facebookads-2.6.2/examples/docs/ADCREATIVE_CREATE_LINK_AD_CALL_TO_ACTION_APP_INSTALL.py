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
campaign_id = fixtures.create_campaign().get_id()
app_id, app_store_url = fixtures.get_promotable_ios_app()
image_hash = fixtures.create_image().get_hash()

# _DOC open [ADCREATIVE_CREATE_LINK_AD_CALL_TO_ACTION_APP_INSTALL]
# _DOC vars [app_store_url:s, page_id, ad_account_id:s, image_hash:s]
from facebookads.objects import AdCreative
from facebookads.specs import ObjectStorySpec, LinkData

link_data = LinkData()
link_data[LinkData.Field.message] = 'try it out'
link_data[LinkData.Field.link] = app_store_url
link_data[LinkData.Field.caption] = 'My caption'
link_data[LinkData.Field.image_hash] = image_hash

call_to_action = {
    'type': 'INSTALL_MOBILE_APP',
    'value': {
        'link': app_store_url,
        'link_caption': 'Facebook',
    },
}

link_data[LinkData.Field.call_to_action] = call_to_action

object_story_spec = ObjectStorySpec()
object_story_spec[ObjectStorySpec.Field.page_id] = page_id
object_story_spec[ObjectStorySpec.Field.link_data] = link_data

creative = AdCreative(parent_id=ad_account_id)
creative[AdCreative.Field.name] = 'Sample Creative'
creative[AdCreative.Field.object_story_spec] = object_story_spec
creative.remote_create()
print(creative)
# _DOC close [ADCREATIVE_CREATE_LINK_AD_CALL_TO_ACTION_APP_INSTALL]

creative.remote_delete()
