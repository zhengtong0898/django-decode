# 类型注解
从`Python 3.5`就开始提供`typing`模块用于标注[类型注解](https://www.python.org/dev/peps/pep-0484/), `typing`库只做标注而不对类型做校验, 若需要校验目前第三方库 [mypy](https://mypy.readthedocs.io/en/stable/introduction.html) 可以满足这个需求.  

&nbsp;  
# mypy校验原则
当代码中声明了类型注解, 它才会追踪`调用`来匹配类型是否一致.   
那些没有声明类型注解的`函数/变量`, 不会进行校验.  
因此`mypy`可以认为是可选校验, 不像`c++`语言那样强行校验所有代码.
   
备注: 如果函数返回值没有定义, 那么`mypy`就会将它当作是动态类型, 而忽略掉检查, 因此每个函数都应该填写一个返回值.

&nbsp;
# mypy安装和使用
```shell script
pip install mypy
venv\Script\mypy.exe _typing.py
```

&nbsp;   
# mypy不校验的情况
如果代码中没有声明类型注解, 即便使用了`mypy`也不会做任何校验. 
```python

def test_no_annotation():
    count: int = 0
    while count < 10:
        count += 1
    return "OK"


def main():
    test_no_annotation()


if __name__ == '__main__':
    main()


# 运行
# venv\Script\mypy.exe _typing.py
#
# 输出
# Success: no issues found in 1 source file
```

&nbsp;  
# 校验返回值类型
```python
def test_return_str_should_raise_error() -> int:
    return "OK"


def main() -> None:
    test_return_str_should_raise_error()


if __name__ == '__main__':
    main()


# 运行
# venv\Script\mypy.exe _typing.py
#
# 输出
# mutter\typing\_typing.py:11: error: Incompatible return value type (got "str", expected "int")
# Found 1 error in 1 file (checked 1 source file)

```

&nbsp;
# 校验参数类型
```python
def test_pass_str_should_raise_error() -> None:

    def greeting(name: str) -> str:
        return 'Hello ' + name

    greeting(3)


def main() -> None:
    test_pass_str_should_raise_error()


if __name__ == '__main__':
    main()


# 运行
# venv\Script\mypy.exe _typing.py
#
# 输出
# mutter\typing\_typing.py:19: error: Argument 1 to "greeting" has incompatible type "int"; expected "str"
# Found 1 error in 1 file (checked 1 source file)
```

&nbsp;  
# 校验自定义类型
```python

class Person:

    def __init__(self, name: str) -> None:
        self.name = name

    def walk(self) -> None:
        print(self.name, "is walking")


def test_pass_person_object(human: Person) -> None:
    human.walk()


def main() -> None:
    p = Person("zhangsan")
    test_pass_person_object(p)


# 运行
# venv\Script\mypy.exe _typing.py
#
# 输出
# Success: no issues found in 1 source file
```

&nbsp;  
# 数据集校验
```python
import typing


list_float = typing.List[float]


def custom_sum(total: list_float) -> float:
    return float(sum(total))


def test_list_type() -> None:
    custom_sum([1.4, 2.0])


def main() -> None:
    test_list_type()


if __name__ == '__main__':
    main()


# 运行
# venv\Script\mypy.exe _typing.py
#
# 输出
# Success: no issues found in 1 source file
```