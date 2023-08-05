import datetime
import time

import requests

from cloudsight import errors


BASE_URL = "https://api.cloudsightapi.com"
REQUESTS_URL = BASE_URL + "/image_requests"
RESPONSES_URL = BASE_URL + "/image_responses/"

DEFAULT_LOCALE = "en-US"
DEFAULT_POLL_TIMEOUT = 10 * 60
INITIAL_POLL_WAIT = 4
USER_AGENT = "cloudsight-python v1.0"


# Possible values for current job status.

# Recognition has not yet been completed for this image. Continue polling until
# response has been marked completed.
STATUS_NOT_COMPLETED = 'not completed'

# Recognition has been completed. Annotation can be found in Name and Categories
# field of Job structure.
STATUS_COMPLETED = 'completed'

# Token supplied on URL does not match an image.
STATUS_NOT_FOUND = 'not found'

# Image couldn't be recognized because of a specific reason. Check the
# SkipReason field.
STATUS_SKIPPED = 'skipped'

# Recognition process exceeded the allowed TTL setting.
STATUS_TIMEOUT = 'timeout'


# The API may choose not to return any response for given image. SkipReason type
# includes possible reasons for such behavior.

# Offensive image content.
REASON_OFFENSIVE = 'offensive'

# Too blurry to identify.
REASON_BLURRY = 'blurry'

# Too close to identify.
REASON_CLOSE = 'close'

# Too dark to identify.
REASON_DARK = 'dark'

# Too bright to identify.
REASON_BRIGHT = 'bright'

# Content could not be identified.
REASON_UNSURE = 'unsure'


class API(object):
    def __init__(self, auth):
        """
        API instance constructor.
        :param auth: instance of Auththorization handler (SimpleAuth or OAuth)
        """
        self.auth = auth

    def _init_data(self, params=None):
        data = {}

        if params:
            data.update(params)

        if 'image_request[locale]' not in data:
            data['image_request[locale]'] = DEFAULT_LOCALE

        return data

    def _unwrap_error(self, response):
        json_response = response.json()

        if 'error' in json_response:
            raise errors.APIError(json_response['error'])

        return json_response

    def image_request(self, image, filename, params=None):
        """
        Send an image for classification. The image is a file-like object. The
        params parameter is optional.
        
        On success this method will immediately return a job information. Its
        status will initially be "not completed" as it usually takes 6-12
        seconds for the server to process an image. In order to retrieve the
        annotation data, you need to keep updating the job status using the
        image_response() method until the status changes. You may also use the
        wait() method which does this automatically.
        """
        data = self._init_data(params)
        response = requests.post(REQUESTS_URL, headers={
            'Authorization': self.auth.authorize('POST', REQUESTS_URL, params),
            'User-Agent': USER_AGENT,
        }, data=data, files={'image_request[image]': (filename, image)})
        return self._unwrap_error(response)

    def remote_image_request(self, image_url, params=None):
        """
        Send an image for classification. The imagewill be retrieved from the
        URL specified. The params parameter is optional.
        
        On success this method will immediately return a job information. Its
        status will initially be "not completed" as it usually takes 6-12
        seconds for the server to process an image. In order to retrieve the
        annotation data, you need to keep updating the job status using the
        image_response() method until the status changes. You may also use the
        wait() method which does this automatically.
        """
        data = self._init_data(params)
        data['image_request[remote_image_url]'] = image_url
        response = requests.post(REQUESTS_URL, headers={
            'Authorization': self.auth.authorize('POST', REQUESTS_URL, data),
            'User-Agent': USER_AGENT,
        }, data=data)
        return self._unwrap_error(response)

    def image_response(self, token):
        """
        Contact the server and update the job status.
        
        After a request has been submitted, it usually takes 6-12 seconds to
        receive a completed response. We recommend polling for a response every
        1 second after a 4 second delay from the initial request, while the
        status is "not completed". wait() method does this automatically.
        """
        url = RESPONSES_URL + token
        response = requests.get(url, headers={
            'Authorization': self.auth.authorize('GET', url),
            'User-Agent': USER_AGENT,
        })
        return self._unwrap_error(response)

    def repost(self, token):
        """
        Repost the job if it has timed out (STATUS_TIMEOUT).
        """
        url = '%s/%s/repost' % (REQUESTS_URL, token)
        response = requests.post(url, headers={
            'Authorization': self.auth.authorize('POST', url),
            'User-Agent': USER_AGENT,
        })
        return self._unwrap_error(response)

    def wait(self, token, timeout=DEFAULT_POLL_TIMEOUT):
        """
        Wait for the job until it has been processed. This method will block for
        up to timeout seconds.
        
        This method will wait for 4 seconds after the initial request and then
        will call image_response() method every second until the status changes.
        """
        delta = datetime.timedelta(seconds=timeout)
        timeout_at = datetime.datetime.now() + delta
        time.sleep(min(timeout, INITIAL_POLL_WAIT))
        response = self.image_response(token)

        while response['status'] == STATUS_NOT_COMPLETED \
              and datetime.datetime.now() < timeout_at:
            time.sleep(1)
            response = self.image_response(token)

        return response
