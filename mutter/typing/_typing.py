import typing


def test_no_annotation():
    count: int = 0
    while count < 10:
        count += 1
    return "OK"


# def test_return_str_should_raise_error() -> int:
#     return "OK"


# def test_pass_str_should_raise_error() -> None:
#
#     def greeting(name: str) -> str:
#         return 'Hello ' + name
#
#     greeting(3)


class Person:

    def __init__(self, name: str) -> None:
        self.name = name

    def walk(self):
        print(self.name, "is walking")


def test_pass_person_object(human: Person) -> None:
    human.walk()


list_float = typing.List[float]


def custom_sum(total: list_float) -> float:
    return float(sum(total))


def test_list_type() -> None:
    custom_sum([1.4, 2.0])


def main() -> None:
    test_list_type()


if __name__ == '__main__':
    main()
