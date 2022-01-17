import hubspot
from django.conf import settings
from hubspot.crm.contacts import (
    ApiException,
    Filter,
    FilterGroup,
    PublicObjectSearchRequest,
    SimplePublicObjectInput,
    BatchInputSimplePublicObjectBatchInput
)
from sentry_sdk import capture_exception


# create an instance of hubspot to make requests with
class Hubspot:
    def __init__(self):
        self.client = hubspot.Client.create(api_key=settings.HUBSPOT_API_KEY)

    def get_hubspot_id(self, email):
        try:

            # from: https://github.com/HubSpot/hubspot-api-python/issues/49#issuecomment-811911302
            email_filter = Filter(property_name="email", operator="EQ", value=email)

            first_group = FilterGroup(filters=[email_filter])

            public_object_search_request = PublicObjectSearchRequest(
                filter_groups=[first_group]
            )

            api_response = self.client.crm.contacts.search_api.do_search(
                public_object_search_request=public_object_search_request
            )

            result = api_response.to_dict()

            if (
                result["total"] == 0
                or "results" not in result
                or len(result["results"]) == 0
            ):
                raise ValueError("no hubspot user email")

            return result["results"][0]["properties"]["hs_object_id"]
        except ApiException as e:
            capture_exception(e)
            raise ValueError("error getting hubspot user email")

    # hubspot api call

    def update_hubspot(self, user_hubspot_id, properties):
        simple_public_object_input = SimplePublicObjectInput(properties=properties)
        try:
            self.client.crm.contacts.basic_api.update(
                contact_id=user_hubspot_id,
                simple_public_object_input=simple_public_object_input,
            )

        except ApiException as e:
            capture_exception(e)
            raise ValueError("error updating hubspot")

    # update funnel status and basics_batch_num on registration

    def update_funnel_basics_apply(self, user_hubspot_id, batch_number):

        properties = {
            "bootcamp_funnel_status": "basics_apply;basics_register",
            "basics_batch_num": f"{batch_number}"
        }

        self.update_hubspot(user_hubspot_id, properties)

    # update funnel status on dropout from batch

    def update_funnel_status(self, user_hubspot_id, funnel_status):

        properties = {
            "bootcamp_funnel_status": f"basics_apply;basics_register;{funnel_status}"
        }

        self.update_hubspot(user_hubspot_id, properties)

    def bulk_update_funnel_completion(self, batch_users):

        property_list = []
        for user in batch_users:
            user_obj = {}
            user_obj['id'] = user.hubspot_id
            user_obj['properties'] = {'bootcamp_funnel_status': 'basics_apply;basics_register;basics_completion'}
            property_list.append(user_obj)

        batch_input_simple_public_object_batch_input = BatchInputSimplePublicObjectBatchInput(inputs=property_list)

        try:
            self.client.crm.contacts.batch_api.update(
                batch_input_simple_public_object_batch_input=batch_input_simple_public_object_batch_input)
        except ApiException as e:
            print(f"Exception when calling batch_api->update: {e}")
