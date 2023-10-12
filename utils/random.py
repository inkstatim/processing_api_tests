import random
import faker


class RandomDataGenerator:
    """
    Name methods should ends on field_name (but snake_case).
    Example: generate_random_middle_name and middleName (in data)
    """
    # toDo check equal types input and output values

    def __init__(self):
        self.faker = faker.Faker()

    def generate_random_sum(self):
        value = random.uniform(0.01, 99999)
        return f"{value:.2f}"

    def generate_random_name(self) -> str:
        return self.faker.first_name()

    def generate_random_middle_name(self) -> str:
        return self.faker.first_name()

    def generate_random_surname(self) -> str:
        return self.faker.last_name()

    def generate_random_email(self) -> str:
        return self.faker.email()

    def generate_random_phone(self) -> str:
        first_two_digits = random.randint(10, 99)
        remaining_digits = ''.join(str(random.randint(0, 9)) for _ in range(6))
        return f"+357 {first_two_digits} {remaining_digits}"
