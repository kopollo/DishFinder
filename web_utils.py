import requests
def get_request(server: str, params: dict[str, str] = None):
    """
    Make GET request to server with given params.

    :param server: full server address
    :param params: dict with params
    :return: response
    """
    try:
        response = requests.get(server, params)
        if not response:
            print('Server is sad with status code', response.status_code)
            print(response.reason)
            return response
        return response
    except requests.RequestException as exc:
        print('Oh ship :(')
        print(exc)
