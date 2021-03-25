# 教程大纲总结
### [tutorial-01](https://docs.djangoproject.com/en/3.1/intro/tutorial01/)
创建项目
```shell
# django-admin startproject mysite
```

创建app
```shell
python mysite/manage.py startapp polls
```

启动服务
```shell
# python mysite/manage.py runserver
``` 

MVC模型
> django采用 MVC 模型(设计模式)驱动代码的开发,     
> M: Model          对应 django.models   
> V: View           对应 polls.views 业务代码入口   
> C: Controller     对应 polls.urls  url映射入口   

View 和 Controller 配置
> mysite/urls.py     
> polls/urls.py   
> polls/views.py   

&nbsp;  
&nbsp;  

### [tutorial-02](https://docs.djangoproject.com/en/3.1/intro/tutorial02/)

数据库配置
> mysite/settings.py
```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

APP配置
> mysite/settings.py
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

内置迁移
> 这里的迁移针对 `INSTALLED_APPS` 中的应用, 它们是django内置提供的应用;  
> 由于它们已经预设好 migrations 目录及其内部指令文件, 所以不需要单独执行 makemigration 去生成这些目录和指令文件了.   
> 直接执行 migrate, 读取 migrations/指令文件, 同步到数据库中.  
```
# python mysite/manage.py migrate
```

应用迁移
> 1. 编辑 polls.models.py 文件, 创建(编码) models 对象.
> 2. 编辑 mysite/settings.py 文件, 将 polls 纳入到 INSTALLED_APPS 中.
> 3. 执行 python mysite/manage.py makemigrations, 生成 migration 目录和指令文件.
> 4. 执行 python mysite/manage.py migrate, 读取 migrations/指令文件, 同步到数据库中.

&nbsp;  
操作ORM(Playing with the API)

&nbsp;   
创建django的管理员账户
```shell
# python mysite/manage.py createsuperuser
```

&nbsp;  
将 polls 这个 app 显示到 admin 后台页面中
> polls/admin.py
```python
from django.contrib import admin

from .models import Question

admin.site.register(Question)
``` 

&nbsp;  
&nbsp;  

### [tutorial-03](https://docs.djangoproject.com/en/3.1/intro/tutorial03/)

动态的url配置
> polls/urls.py  
```python
from django.urls import path

from . import views

# 备注:
# django 从 2.0 版本开始就一直采用 path(非正则表达式), 在此之前采用的是 url(正则表达式).
# path是一种 DSL, 用于简化表达式, 但是其内部最终还是要转换回到标准的正则表达式.
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
```
> polls/views.py
```python
from django.http import HttpResponse

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
```

&nbsp;  

编写一个模板页面
> 1. 创建 polls/templates/polls/index.html 模板文件   
> 2. 编辑 polls/views.py 文件, 重构 def index 函数   
> 3. 在 def index 函数中使用 django.shortcuts.render 渲染模板文件   


&nbsp;  

关于报错
> All Django wants is that HttpResponse. Or an exception. 

&nbsp;
  
抛出一个404例子
> 1. 创建 polls/templates/polls/detail.html 模板文件   
> 2. 编辑 polls/views.py 文件, 重构 def detail 函数   
> 3. 在 def detail 函数中使用 orm 查询数据库:   
>    q = Question.objects.get(pk=question_id)   
>    如果q存在, 那么就返回正常的 detail 渲染结果;   
>    如果q不存在, 那么就主动抛出一个Http404异常.   

&nbsp;  

使用模板语言
> 模板语言支持变量引用, orm操作, for, if 等语法操作.  

&nbsp;  
urls中的命名空间
> 在 polls.urls.py 中添加 app_name = 'polls' 变量.    
> 在模板文件中使用 {% url 'polls.detail' question.id %},  
> 其中'polls.detail'对应的是 app_name 和 path中的name='detail',  
> question 是 def detail 中 render 提供的变量: render(request, 'polls/detail.html', {'question': question}) 


&nbsp;  
&nbsp;   
 
 ### [tutorial-04](https://docs.djangoproject.com/en/3.1/intro/tutorial04/)
 
 模板关语法介绍
```text
{% csrf_token %}            # Cross Site Request Forgeries(跨站请求伪造)
                            # Django 提供 csrf_token 防止跨站请求伪造机制, 
                            # post表单的模板中, 只要使用 {% csrf_token %} 就可以解决此问题.

{{ forloop }}               # 这是Django提供的一个template tag(数据对象), 用于记录循环统计信息.
                            # forloop.parentloop: 父循环对象.
                            # forloop.counter:    遍历次数, 从1开始.
                            # forloop.revcounter: 集合总数, 从总数开始递减.
                            # forloop.first:      是否第一次.
                            # forloop.last:       是否最后一次.
``` 

&nbsp;  
泛型试图介绍
> Django 提供了一组泛型试图(DetailView/ListView/FormView/CreateView/UpdateView/DeleteView/...), 用于简化特定场景的代码编写, 加速开发进度.      
> 
> DetailView: 显示一个详情页; DetailView 的理念是使用 ORM 的特性, 一条数据对象可以查询到一个关联表( model.relatetable1_set.all )的数据, 多个表的关联可以通过一条数据无限扩展开来.      
>    
> ListView: 显示一个列表页; ListView 的理念是也是使用 ORM 的特性, 返回一个列表给模板文件, 由模板文件通过关联查询来拉取需要的字段.   
>
> 经过简略的源码追踪发现:   
> 继承了泛型试图的对象的 model 属性和 get_queryset 方法必须提供至少二选一的定义, 也可以两者都定义.     
> 定义 model 属性是告诉泛型试图, 围绕这个model对象来提取数据;   
> 定义 get_queryset 方法是告诉泛型试图, 按照我定义的 get_queryset 查询数据集即可;   
> 如果两者都定义了, get_queryset将会优先执行来提取数据, 并且会忽略 model (即: 不会再automatically的去提取这个model的数据). 


&nbsp;  
&nbsp;  

### [tutorial-05](https://docs.djangoproject.com/en/3.1/intro/tutorial05/)

创建和运行一个测试用例
> 创建 polls/tests.py 文件
```python
import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


# django会找到所有继承了 django.test.TestCase 的对象, 
# 并执行那些 test_ 开头的方法的测试用例.
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        # time 是下个月的时间, 所以 future_question 是下个月的问题.
        # 断言期望: future_question.was_published_recently() == False
        # 当 future_question.was_published_recently() == False 时, 测试成功.
        # 当 future_question.was_published_recently() == True 时, 测试失败, 抛出异常.
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        # 边界值测试
        # 测试场景: 当 pub_date 是 1天零1秒前 时, 它不属于最近发布.
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        # 边界值测试
        # 测试场景: 当 pub_date 是 1天内时(即便时: 23:59:59秒之前), 它都属于最近发布.
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

```
> 运行测试
```shell
# python mysite/manage.py test polls
```

&nbsp;   
用于测试目的的http client
> django基于wsgi封装一个http client于django.test中, 
> 即:通过这个django.test.Client可以调用内部的urls快速的完成一些请求测试场景.   
> 
> 为什么要封装这个http client, 用 requests 不行吗?   
> 答案是: 不行, 因为 django 还做了很多封装, 尤其是 context 也封装出来了, 而 requests 则没有; 通过 context 可以验证渲染时传递的变量是否符合预期.
```shell
# python mysite/manage.py shell
>>> from django.test.utils import setup_test_environment
>>> setup_test_environment()
>>>
>>> from django.test import Client
>>> client = Client()
>>>
>>> from django.urls import reverse
>>> uri = reverse('polls:index')        # /polls/
>>> response = client.get(uri)
>>> response.status_code
200
>>> response.content
b'\n    <ul>\n    \n        <li><a href="/polls/1/">What&#x27;s up?</a></li>\n    \n    </ul>\n\n'
>>> response.context['latest_question_list']
<QuerySet [<Question: What's up?>]>
```

&nbsp;  
&nbsp;  
### [tutorial-06](https://docs.djangoproject.com/en/3.1/intro/tutorial06/)
静态文件
> 以 app 名 polls 为例, django 要求静态文件路径格式为: polls/static   
> 如果文件存放在: polls/static/style.css ; 那么在模板内引用为: {% static style.css %}    
> 如果文件存放在: polls/static/abc/style.css ; 那么在模板内引用为: {% static abc/style.css %}
> 


&nbsp;  
&nbsp;  

### [tutorial-07](https://docs.djangoproject.com/en/3.1/intro/tutorial07/)

自定义admin表单(新增/修改)
> django 提供了 django.contrib.admin.ModelAdmin 对象, 用于控制字段的显示顺序, 数据写入方式(支持填写关联表信息).

- [字段排序](https://docs.djangoproject.com/en/3.1/intro/tutorial07/#customize-the-admin-form)   
   对于那些字段很多表, 字段显示的顺序的重要性不言而喻.   
   django.contrib.admin.ModelAdmin.fields 的fields字段用于控制字段的顺序.

- [添加关联对象](https://docs.djangoproject.com/en/3.1/intro/tutorial07/#adding-related-objects)   
   在表单中可以将关联表的字段纳入到主表单中, 支持两种方式: 栈排列(StackedInline) , 表格排列(TabularInline) .

  ![自定义admin表单](mysite/imgs/custom_admin_form_01.jpg#pic_center)   

&nbsp;  

自定义admin列表
- 每行数据显示哪些字段
  ```shell
  # django.contrib.admin.ModelAdmin.list_display = (field1, field2, field3, ...)
  class QuestionAdmin(admin.ModelAdmin):
      # 列表每行显示哪些字段
      # django 除了支持显示字段信息, 也支持显示 model 的方法: was_published_recently.
      list_display = ('question_text', 'pub_date', 'was_published_recently')
  ```

- 定义列表字段头描述(默认情况是以大写的字段名显示)
  ```shell
  # django.contrib.admin.ModelAdmin.Field.verbose_name
  class Question(models.Model):
      # verbose_name: 列表头(column head)
      question_text = models.CharField(verbose_name='问题标题', max_length=200)
  
      # 特殊情况: 为方法设定字段头显示的信息
      # 给 was_published_recently 方法添加一些属性.
      was_published_recently.admin_order_field = 'pub_date'
      was_published_recently.boolean = True
      was_published_recently.short_description = '近期发布?'
  ```

- 搜索哪个字段
  ```shell
  # django.contrib.admin.ModelAdmin.search_fields = [field1, field2, field3, ...]
  class Question(models.Model):
      # 模糊查询: 根据给定的字段进行模糊查询.
      # 如果只给定 question_text 字段, 那么就只搜索question_text.
      # 如果给定 question_text 和 pub_date, 那么任意一个字段匹配命中都会显示该行数据.
      search_fields = ['question_text', 'pub_date']
  ```

- 按分类筛选
  ```shell
  class QuestionAdmin(admin.ModelAdmin):
      # 按类型筛选, bool(会有两个筛选条件), 时间(会有today/past 7 days/this month/this year筛选条件)
      list_filter = ['pub_date']
  ```
  
  ![自定义admin表单02](mysite/imgs/custom_admin_form_02.jpg#pic_center)
 

&nbsp;  

自定义admin页面的标语(默认是: Django Administration)
```shell
1. 创建文件夹 polls/templates/admin
2. 复制django模板文件: copy django/contrib/admin/templates/base_site.html to polls/templates/admin/
3. 编辑 polls/templates/admin/base_site.html 文件
4. 找到 <h1 id="site-name"><a href="{% url 'admin:index' %}">{{ site_header|default:_('Django administration') }}</a></h1>
5. 更改为 <h1 id="site-name"><a href="{% url 'admin:index' %}">管理页面</a></h1>
```