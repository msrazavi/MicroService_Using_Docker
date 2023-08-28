import requests

URL = 'http://localhost:5000/users'


def post_user(name, email):
    data = {'name': name, 'email': email}
    response = requests.post(URL, json=data)
    print(response.json())


def get_user(id):
    response = requests.get(f'{URL}/{id}')
    print(response.json())
    return response.json()


def update_user(id, name=None, email=None):
    if name:
        new_name = name
    else:
        new_name = get_user(id)['name']
    if email:
        new_email = email
    else:
        new_email = get_user(id)['email']
    data = {'name': new_name, 'email': new_email}
    response = requests.put(f'{URL}/{id}', json=data)
    print(response.json())


def delete_user(id):
    response = requests.delete(f'{URL}/{id}')
    print(response.json())


def get_all_users():
    response = requests.get(URL)
    print(response.json())


if __name__ == '__main__':
    # post_user('maryam', 'razavi.mst@gmail.com')
    # print(get_user(1)['name'])
    # update_user(1, name='reza')
    # delete_user(1)
    get_all_users()
