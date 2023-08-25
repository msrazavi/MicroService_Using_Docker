import requests

URL = 'http://localhost:5000/users'


def get_users():
    response = requests.get(URL)
    print(response.text)


def post_user(name, email):
    data = {'name': name, 'email': email}
    response = requests.post(URL, json=data)
    print(response.json())


if __name__ == '__main__':
    post_user('maryam', 'razavi.mst@gmail.com')
