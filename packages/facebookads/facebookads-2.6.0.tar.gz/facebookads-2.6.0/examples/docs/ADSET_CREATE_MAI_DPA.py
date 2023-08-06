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
from facebookads.objects import Campaign

ad_account_id = test_config.account_id
product_catalog_id = fixtures.create_product_catalog().get_id()
campaign_id = fixtures.create_campaign({
    Campaign.Field.objective: Campaign.Objective.mobile_app_installs,
    Campaign.Field.promoted_object: {
        'product_catalog_id': product_catalog_id,
    },
}).get_id()
app_id, app_store_url = fixtures.get_promotable_ios_app()
product_set_id = fixtures.create_product_set(product_catalog_id).get_id()
product_audience_id = fixtures.create_product_audience(
    product_set_id, product_catalog_id,
).get_id()

# _DOC oncall [ttho]
# _DOC open [ADSET_CREATE_MAI_DPA]
# _DOC vars [campaign_id, ad_account_id:s, app_id, product_audience_id, app_store_url:s]
from facebookads.objects import AdSet, TargetingSpecsField

adset = AdSet(parent_id=ad_account_id)
adset.update({
    AdSet.Field.name: 'Mobile App Installs Ad Set with Dynamic Product Ads',
    AdSet.Field.promoted_object: {
        'product_set_id': product_set_id,
        'application_id': app_id,
        'object_store_url': app_store_url,
    },
    AdSet.Field.campaign_id: campaign_id,
    AdSet.Field.daily_budget: 15000,
    AdSet.Field.optimization_goal: AdSet.OptimizationGoal.app_installs,
    AdSet.Field.billing_event: AdSet.BillingEvent.impressions,
    AdSet.Field.bid_amount: 3000,
    AdSet.Field.targeting: {
        TargetingSpecsField.geo_locations: {
            'countries': ['US'],
        },
        TargetingSpecsField.page_types: [
            'mobileexternal',
            'mobilefeed',
        ],
        TargetingSpecsField.user_os: [
            'IOS',
        ],
        TargetingSpecsField.dynamic_audience_ids: [
            product_audience_id,
        ],
    },
})

adset.remote_create(params={
    'status': AdSet.Status.paused,
})
# _DOC close [ADSET_CREATE_MAI_DPA]

adset.remote_delete()
