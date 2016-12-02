from faker import Faker

faker = Faker()


def get_fake_user_data():
    return {
        'name': faker.name(),
        'username': faker.user_name(),
        'email': faker.email(),
        'password': 's3cr4t$'
    }
