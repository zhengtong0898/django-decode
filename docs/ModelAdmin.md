### list_display
[admin.ModelAdmin.list_display](../follow-tutorial/mysite/polls/admin.py#L36) 
该属性用于控制字段显示, 即`change`列表的每行显示几个字段.   
<p align="center">
  <img src="follow-tutorial/mysite/imgs/list_display.jpg" alt="list_display"/>
</p>

&nbsp;  
&nbsp;  
### list_display_links
[admin.ModelAdmin.list_display_links](admin-tutorial/AdminFilter/filter_horizontal_/admin.py#L11) 
该属性用于将编辑数据的链接显示在指定字段, 默认是显示在第一个字段.
<p align="center">
  <img src="admin-tutorial/AdminFilter/filter_horizontal_/imgs/list_display_links.jpg" alt="list_display_links"/>
</p>


&nbsp;  
&nbsp;   
### list_filter
[admin.ModelAdmin.list_filter](follow-tutorial/mysite/polls/admin.py#L39) 
该属性用于指定字段分类筛选, 最佳实践适用于`bool`类型字段, 时间类型字段, 和少量`choices`类型字段.  
<p align="center">
  <img src="follow-tutorial/mysite/imgs/list_filter.jpg" alt="list_filter"/>
</p>


&nbsp;  
&nbsp;  
### list_select_related
当访问 `chang` 列表页面时, `Django`默认不会去提取关联表信息(select_related);     
只有一种情况会主动去查询关联表信息, 即: 当`list_display` 集合中包含了外键字段时, 才会主动去查询关联表信息(select_related).   
另外一种情况那就是当 `list_select_related` 属性是 `True` 时, `Django`也会主动去查询关联表信息(select_related).   

`select_related`方法回归到原始`sql`是采用了 `inner join` 把两张表的字段都提取出来;


&nbsp;   
&nbsp;   
### list_per_page
[admin.ModelAdmin.list_per_page](admin-tutorial/AdminFilter/filter_horizontal_/admin.py#L13) `change`列表页面, 每页显示多少条数据.     
[admin.ModelAdmin.list_max_show_all](admin-tutorial/AdminFilter/filter_horizontal_/admin.py#L14) 列表页面下方的分页最右侧的`Show all`, 显示多少条数据.      
<p align="center">
  <img src="admin-tutorial/AdminFilter/filter_horizontal_/imgs/list_per_page.jpg" alt="list_per_page"/>
</p>


&nbsp;  
&nbsp;  
### list_editable
[admin.ModelAdmin.list_editable](admin-tutorial/AdminFilter/ordering_/admin.py#L18) 
`Django`允许在`change`列表页面一次性编辑多条数据.   
`list_editable` 是 `list` / `tuple` 类型变量, 填写字段名, 表示字段可以在`chang`列表页面编辑多条数据.  
<p align="center">
  <img src="admin-tutorial/AdminFilter/ordering_/imgs/list_editable.jpg" alt="list_editable"/>
</p>


&nbsp;   
&nbsp;   
### search_fields
[admin.ModelAdmin.search_fields](follow-tutorial/mysite/polls/admin.py#L44) 
该属性用于模糊搜索指定字段, 模糊搜索在`sql`中采用的是 `like '%search%'`语法.   
<p align="center">
  <img src="follow-tutorial/mysite/imgs/search_fields.jpg" alt="search_fields"/>
</p>


&nbsp;  
&nbsp; 
### date_hierarchy
[admin.ModelAdmin.date_hierarchy](admin-tutorial/AdminDateHierarchy/simple/admin.py#L8)   
`Django` 提供了一个按[时间分层器](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.date_hierarchy)来筛选数据功能, 从页面中能看到的是一个 `drilldown` 导航栏;  
 当 `change list` 表格的数据的创建时间分布于当月不同时间, 那么时间分层器会显示当月具体日期时间(按所有数据-日-分组所得).     
 当 `change list` 表格的数据的创建时间分布于当年不同时间, 那么时间分层器会显示当年具体月份时间(按所有数据-月-分组所得).    
 当 `change list` 表格的数据的创建时间分布于不同年份, 那么时间分层器会显示不同年份时间(按所有数据-年-分组所得).    
 
`admin.ModelAdmin.date_hierarchy` 支持两种写法:
- [普通字段](admin-tutorial/AdminDateHierarchy/simple/admin.py#L8)
  <p align="center">
    <img src="admin-tutorial/AdminDateHierarchy/simple/imgs/date_hierarchy.jpg" alt="date_hierarchy"/>
  </p>
- [关联字段](admin-tutorial/AdminDateHierarchy/simple_relate/admin.py#L21)
  <p align="center">
    <img src="admin-tutorial/AdminDateHierarchy/simple_relate/imgs/related_hierarchy.jpg" alt="date_hierarchy"/>
  </p>
 
&nbsp;  
&nbsp;  
### save_as
[admin.ModelAdmin.save_as](admin-tutorial/AdminDateHierarchy/simple_relate/admin.py#L60)
该属性表示用编辑的表单数据创建新数据;  
`False` 时, 表单底部显示 'Save and add another' 按钮.    
`True` 时, 表单底部显示 'save as new' 按钮.     
'save as new' 的作用是, 当模块表单字段过多, 新建一条数据时间成本较高时,    
可以采取编辑一条数据, 按需更改几个必要字段后, 点击 'save as new' 完成一条数据的创建.   
<p align="center">
  <img src="admin-tutorial/AdminDateHierarchy/simple_relate/imgs/save_as.jpg" alt="save_as"/>
</p>


&nbsp;  
&nbsp;  
### save_as_continue
[admin.ModelAdmin.save_as_continue](admin-tutorial/AdminDateHierarchy/simple_relate/admin.py#L65)
该属性作用在 `save_as=True` 基础上, 告诉`Django`数据创建完成后, 是进入编辑界面还是返回`change`列表页面.  
`save_as_continue=True` 时, 数据创建完成后， 重定向到编辑页面.
`save_as_continue=False` 时, 数据创建完成后, 重定向到`change`列表页面.

&nbsp;  
&nbsp; 
### save_on_top 
[admin.ModelAdmin.save_on_top](admin-tutorial/AdminDateHierarchy/simple_relate/admin.py#L63) 
开启这个属性, 会出现两行按钮保存栏, 他们分别出现在表单的头部和表单的底部.
<p align="center">
  <img src="admin-tutorial/AdminDateHierarchy/simple_relate/imgs/save_on_top.jpg" alt="save_on_top"/>
</p>


&nbsp;   
&nbsp;  
### preserve_filters
[admin.ModelAdmin.preserve_filters](admin-tutorial/AdminFilter/ordering_/admin.py#L16)  
在已过滤(搜索)的列表中修改、删除、创建数据完成后再次返回到列表页面时, 是否保留搜索状态.  
`preserve_filters` 是 `bool`类型变量, `True`时表示保留搜索状态, `False`时表示不保留搜索状态;  
<p align="center">
  <img src="admin-tutorial/AdminFilter/ordering_/imgs/preserve_filters.jpg" alt="preserve_filters"/>
</p>


&nbsp;  
&nbsp;  
### inlines
[admin.ModelAdmin.inlines](follow-tutorial/mysite/polls/admin.py#L33)
在编辑页面的表单中, 可以将关联表的字段纳入到主表单中, 支持两种方式: 栈排列(StackedInline) , 表格排列(TabularInline) .
<p align="center">
  <img src="follow-tutorial/mysite/imgs/tabularinline.jpg" alt="tabularinline"/>
</p>



&nbsp;  
&nbsp;   

### actions
[admin.ModelAdmin.actions](admin-tutorial/AdminActions/actions/admin.py#L16)
该属性用于控制 `批量操作` 功能的表现;  
默认情况下, `批量操作栏` 会有一个 `delete selected` 功能; 除此之外也可以通过将函数或方法添加到`actions`集合中, 让`批量操作`下拉菜单拥有其他批量操作功能.   

`actions` 的值类型是 `None` 时, 表示不显示批量操作栏.     
`actions` 的值类型是 `list` 或 `tuple` 时, 显示批量操作栏.   
`actions` 的值类型是 `list` 或 `tuple` 时, 同时元素是字符串时, `Django`会通过反射语法来读取`self`的对应方法.
 
 - [`actions = [make_published, ]`](admin-tutorial/AdminActions/actions/admin.py#L16)
    <p align="center">
      <img src="admin-tutorial/AdminActions/actions/imgs/update_field_status.jpg" alt="update_field_status"/>
    </p>

- [`actions = ['make_published', ]`](admin-tutorial/AdminActions/actions_method/admin.py#L14)
    <p align="center">
      <img src="admin-tutorial/AdminActions/actions_method/imgs/update_field_status_by_method.jpg" alt="update_field_status_by_method"/>
    </p>

- [`actions = None`](admin-tutorial/AdminActions/actions_method/admin.py#L12)
    <p align="center">
      <img src="admin-tutorial/AdminActions/actions_method/imgs/hide_batch_operator.jpg" alt="hide_batch_operator"/>
    </p>

&nbsp;  
&nbsp;  
### actions_on_top
[admin.ModelAdmin.actions_on_top](admin-tutorial/AdminActions/actions_method/admin.py#L18)    
[admin.ModelAdmin.actions_on_bottom](admin-tutorial/AdminActions/actions_method/admin.py#L19)   
这两个属性分别控制`change`列表页面的批量操作栏目显示的位置, 它们两通常需要同时配置(一个为`True`, 另外一个为`False`).   
`actions_on_top=True`时, 表示在表单的上方显示批量操作栏目.  
`actions_on_top=False`时, 隐藏表单上方的批量操作栏目.   
`actions_on_bottom=True`时, 表示在表单的下方显示批量操作栏目.   
`actions_on_bottom=False`时, 隐藏表单下方的批量操作栏目.   

- 情况1   
  `actions_on_top=True`   
  `actions_on_bottom=True`   
  当两个属性都是`True`时, 表示在`change`列表的上方和下方都显示批量操作栏目(即: 显示两个一样的批量操作栏目).   
- 情况2
  `actions_on_top=False`      
  `actions_on_bottom=False`   
  当两个属性都是`False`时, 表示在`change`列表页面不显示批量操作栏目.   
- 情况3
  `actions_on_top=True`      
  `actions_on_bottom=False`   
  仅在`change`列表的上方显示操作栏目.   
- 情况4   
  `actions_on_top=True`      
  `actions_on_bottom=False`   
  仅在`change`列表的下方显示操作栏目.
  
  <p align="center">
    <img src="admin-tutorial/AdminActions/actions_method/imgs/action_on_bottom.jpg" alt="action_on_bottom"/>
  </p>
  

&nbsp;  
&nbsp;   
### actions_selection_counter
[admin.ModelAdmin.actions_selection_counter](admin-tutorial/AdminActions/actions_method/admin.py#L16)
该属性用于控制批量操作右侧已选中计数器的显示隐藏开关;     
`actions_selection_counter=True`时, 表示显示已选中的计数.     
`actions_selection_counter=False`时, 表示隐藏已选中的计数.      
<p align="center">
    <img src="admin-tutorial/AdminActions/actions/imgs/selected_counter.jpg" alt="selected_counter"/>
</p>
