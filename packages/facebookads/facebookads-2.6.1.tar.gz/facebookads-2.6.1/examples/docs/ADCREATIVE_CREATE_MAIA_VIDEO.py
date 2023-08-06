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
video_id = fixtures.create_video().get_id()
thumbnail_url = fixtures.wait_for_video_thumbnail(video_id)
app_id, app_store_url = fixtures.get_promotable_ios_app()

# _DOC oncall [pruno]
# _DOC open [ADCREATIVE_CREATE_MAIA_VIDEO]
# _DOC vars [video_id, thumbnail_url:s, app_store_url:s, page_id, ad_account_id:s]
from facebookads.objects import AdCreative
from facebookads.specs import ObjectStorySpec, VideoData

video_data = VideoData()
video_data.update({
    VideoData.Field.video_id: video_id,
    VideoData.Field.description: 'Creative description',
    VideoData.Field.image_url: thumbnail_url,
    VideoData.Field.call_to_action: {
        'type': 'INSTALL_MOBILE_APP',
        'value': {
            'link': app_store_url,
            'link_title': 'Link title',
        },
    },
})

story = ObjectStorySpec()
story.update({
    ObjectStorySpec.Field.page_id: page_id,
    ObjectStorySpec.Field.video_data: video_data,
})

creative = AdCreative(parent_id=ad_account_id)
creative[AdCreative.Field.object_story_spec] = story
creative.remote_create()
# _DOC close [ADCREATIVE_CREATE_MAIA_VIDEO]

creative.remote_delete()
