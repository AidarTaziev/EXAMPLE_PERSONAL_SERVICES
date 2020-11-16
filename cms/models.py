import logging
import datetime
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.contrib.auth.models import Group
from utils.datetime.datetime import add_months
from render import models as render_models

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename=u'erp.log')


class BlockStatus(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование статуса")

    class Meta:
        verbose_name = "Статус Подкатегории"
        verbose_name_plural = "Статусы Подкатегорий"

    def __str__(self):
        return self.name

    def get_data(self):
        return {
            "name": self.name,
        }


class SearchInputType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование типа поискового инпута")
       
    class Meta:
        verbose_name = "Тип поискового инпута"
        verbose_name_plural = "Типы поисковых инпутов"

    def __str__(self):
        return self.name

    def get_data(self):
        return {
            "name": self.name,
        }


class DateDefaultValueType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование типа значения по умолчанию date инпута")
    short_name = models.CharField(max_length=255, default='exact_setup', blank=True, verbose_name="Короткое наименование типа продолжительности date инпута")
    is_special_setup = models.BooleanField(default=True, blank=True, verbose_name='Это специальная настройка? (Настройка, которая может задаваться только из кода)')
    months_setup = models.IntegerField(null=True, blank=True, verbose_name="Настройка месяцев")
    days_setup = models.IntegerField(null=True, blank=True, verbose_name="Настройка дней")
    from_start_month = models.IntegerField(null=True, blank=True, verbose_name="От начала месяца?")

    class Meta:
        verbose_name = "Типы дефолтного значение date инпута"
        verbose_name_plural = "Типы дефолтных значений date инпутов"

    def __str__(self):
        return self.name

    def get_data(self):
        return {
            "name": self.name,
        }


class InputDataType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование типа инпута")
       
    class Meta:
        verbose_name = "Тип параметра"
        verbose_name_plural = "Типы параметров"

    def __str__(self):
        return self.name

    def get_data(self):
        return {
            "name": self.name,
        }


class ResourceInputParam(models.Model):
    #TODO: Добавить ресурс к которому он относится
    input_data_type = models.ForeignKey(InputDataType, on_delete=models.CASCADE, verbose_name="Тип параметра")
    name = models.CharField(max_length=255, verbose_name="Название парамметра") 
    date_duration_type = models.ForeignKey(DateDefaultValueType, on_delete=models.CASCADE, verbose_name="Тип продолжительности date", null=True, blank=True)
    select_get_value = models.CharField(max_length=255, null=True, blank=True, verbose_name="uri откуда брать значение для select") 
    default_string_value = models.CharField(max_length=255, null=True, blank=True, verbose_name="Наименование для заголовка")
    default_date_value = models.DateField(null=True, blank=True, verbose_name='Значение по умолчанию в случае если тип date')
    default_boolean_value = models.BooleanField(default=False, blank=True, verbose_name='Значение по умолчанию в случае если тип boolean')

    class Meta:
        verbose_name = "Входной параметр для внешнего источника"
        verbose_name_plural = "Входные параметры для внешнего источника"
    
    def __str__(self):
        return 'Название входного параметра - {0}|  тип - {1}'.format(self.name, self.input_data_type.name)
    
    @property
    def value(self):
        if self.input_data_type.name == 'date':
            value = self.get_default_date_value()
        elif self.input_data_type.name == 'string':
            value = self.default_string_value
        else:
            value = None
        return value  
    
    def get_data(self):
        return {self.name: self.value}

    def get_default_date_value(self):
        date_now = datetime.date.today()
        num_day = datetime.datetime.now().day

        if self.date_duration_type:
            if self.date_duration_type.is_special_setup:
                if self.date_duration_type.short_name == 'date_now':
                    return date_now
                elif  self.date_duration_type.short_name == 'date_month_ago':
                    return add_months(date_now, -1)
                elif  self.date_duration_type.short_name == 'first_date_half_year':
                    return add_months(date_now, -5) - timedelta(days=(num_day - 1))
                elif  self.date_duration_type.short_name == 'first_date_cur_month':
                    return date_now - timedelta(days=(num_day - 1))
                elif self.date_duration_type.short_name == 'first_date_current_year':
                    return datetime.date(date_now.year, 1, 1)
            else:
                if self.date_duration_type.short_name == 'default':
                    return self.default_date_value
                else:
                    months_setup = self.date_duration_type.months_setup if self.date_duration_type.months_setup else 0
                    days_setup = self.date_duration_type.days_setup if self.date_duration_type.days_setup else 0

                    if self.date_duration_type.from_start_month:
                        return add_months(date_now, months_setup) - timedelta(days=(num_day - 1))
                    else:
                        return add_months(date_now, months_setup) + timedelta(days=days_setup)
        return None


class SwitchSearchInputPart(models.Model):
    description = models.CharField(max_length=255, verbose_name="Описание") 
    display_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Наименование для заголовка") 
    input_params = models.ManyToManyField(ResourceInputParam, null=True, blank=True, verbose_name="Входные параметры")
    selected = models.BooleanField(default=False, blank=True, verbose_name='Выбран ли данный элемент switch')
    priority = models.IntegerField(verbose_name="Приоритет вывода")
    
    class Meta:
        verbose_name = "Часть поискового switch инпута"
        verbose_name_plural = "Части поискового switch инпута"
    
    def __str__(self):
        return self.description

    @property
    def input_params_list(self):
        return [param.get_data() for param in self.input_params.all()]
    
    def get_data(self):
        data = {
            "display_name": self.display_name,
            'values': self.input_params_list
        }
        if self.selected: data['selected'] = self.selected
        return data


class SearchInput(models.Model):
    description = models.CharField(max_length=255, verbose_name="Описание") 
    display_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Наименование для заголовка") 
    search_input_type = models.ForeignKey(SearchInputType, on_delete=models.CASCADE, verbose_name="Тип поискового инпута")
    input_param = models.ForeignKey(ResourceInputParam, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="Входные параметры (Не указывать в случае типа switch)")
    select_get_value = models.CharField(max_length=255, null=True, blank=True, verbose_name="uri откуда брать значение для select (Не указывать в случае типа switch)") 
    switch_parts = models.ManyToManyField(SwitchSearchInputPart, null=True, blank=True, verbose_name="Части switch инпута(Указывается только для типа switch)")
    
    class Meta:
        verbose_name = "Элемент поискового инпута"
        verbose_name_plural = "Элементы поисковых инпутов"
    
    def __str__(self):
        return self.description

    @property
    def switch_parts_list(self):
        return [part.get_data() for part in self.switch_parts.all().order_by('priority')]
    
    def get_data(self):
        data = {
            'type': self.search_input_type.name, 
        }

        if self.search_input_type.name == 'date':
            data['label'] = self.input_param.name
            data['display_name'] = self.display_name
            data['value'] = self.input_param.value
        elif self.search_input_type.name == 'number':
            data['label'] = self.input_param.name
            data['display_name'] = self.display_name
            #TODO: добавить поле числовое по умолчанию
            data['value'] = 12000 * 74 
        elif self.search_input_type.name == 'select':
            data['label'] = self.input_param.name
            data['display_name'] = self.display_name
            data['get_value'] = self.select_get_value
        elif self.search_input_type.name == 'switch':
            data['display_name'] = self.display_name
            data['data'] = self.switch_parts_list

        return data


class SubCategoryAction(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование действия")
    short_name = models.CharField(max_length=255, verbose_name="Короткое наименование действия", default="1")

    class Meta:
        verbose_name = "Действие Подкатегории"
        verbose_name_plural = "Действия Подкатегорий"

    def __str__(self):
        return self.name

    def get_data(self):
        return {
            "short_name": self.short_name,
        }


class SubCategoryTemplate(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование шаблона")

    class Meta:
        verbose_name = "Шаблон Подкатегории"
        verbose_name_plural = "Шаблоны Подкатегорий"

    def __str__(self):
        return self.name


class PageElement(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    template = models.ForeignKey(SubCategoryTemplate, on_delete=models.CASCADE, verbose_name="Шаблон элемента стр.")
    render_class = models.ManyToManyField(render_models.RenderClass, null=True, blank=True, verbose_name="Классы для стилизации элемента стр.")
    priority = models.IntegerField(verbose_name="Приоритет вывода")

    class Meta:
        verbose_name = "Элемент(темлейт) страницы"
        verbose_name_plural = "Элементы(темлейты) страницы"

    def __str__(self):
        return self.title

    @property
    def render_class_list(self):
        return [{"name": a.name, "styles": a.get_styles()} for a in self.render_class.all()]

    def page_element_options_list(self, sub_category):
        labels = []
        page_element_options = list(PageElementOptions.objects.filter(content_block=self,
                                                                      sub_category=sub_category,
                                                                      is_expose=True).\
                                    order_by('priority').values('display_name', 'select_value', 'types__name'))
        for element in page_element_options:
            labels.append({'value': element['display_name'],
                           'value_type': element['types__name'],
                           'select_value': element['select_value']})
        return labels
    
    def get_data(self, sub_category):
        return {
            "type": self.template.name,
            "priority": self.priority,
            "render_classes": self.render_class_list,
            "labels": self.page_element_options_list(sub_category),
        }


class BasicAuthentication(models.Model):
    basic_username = models.CharField(max_length=255, verbose_name="Логин basic-авторизации", blank=True)
    basic_password = models.CharField(max_length=255, verbose_name="Пароль basic-авторизации", blank=True)
    
    class Meta:
        verbose_name = "Basic авторизация"
        verbose_name_plural = "Basic авторизации"

    def __str__(self):
        return self.basic_username


class SubCategory(models.Model):
    lang = models.CharField(max_length=255, default='ru', verbose_name="Язык подкатегории")
    name = models.CharField(max_length=255, verbose_name="Наименование подкатегории")
    status = models.ForeignKey(BlockStatus, models.DO_NOTHING, default=1, verbose_name="Статус блока")
    icon_path = models.ImageField(null=True, blank=True, upload_to='images/', verbose_name="Иконка блока")
    link = models.CharField(max_length=255, verbose_name="Адрес", blank=True)

    basic_authentication = models.ForeignKey(BasicAuthentication, on_delete=models.CASCADE, verbose_name="Аутентификация подкатегории", blank=True, null=True)

    url = models.CharField(max_length=255, verbose_name="URL", blank=True)

    path_get = models.CharField(max_length=255, verbose_name="Путь получения данных в 1С GET", blank=True)
    path_post = models.CharField(max_length=255, verbose_name="Путь отправки данных в 1С POST", null=True, blank=True)
    erp_report_guid = models.CharField(max_length=255, verbose_name="GUID отчета ERP", blank=True)
    path_download_excel = models.CharField(max_length=255, verbose_name="Путь для получения excel файла", null=True,
                                           blank=True)
    description = models.TextField(verbose_name="Описание подкатегории", null=True, blank=True)
    page_elements = models.ManyToManyField(PageElement, blank=True, verbose_name="Элементы(темлпейты) страницы")

    actions = models.ManyToManyField(SubCategoryAction, blank=True, verbose_name="Действия")
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    priority = models.IntegerField('Приоритет вывода', default=1)

    search_inputs = models.ManyToManyField(SearchInput, null=True, blank=True, verbose_name="Поисковые инпуты")

    class Meta:
        verbose_name = "Подкатегория блоков"
        verbose_name_plural = "Подкатегории блоков"

    def __str__(self):
        return self.name + ' | ' + self.description
    
    @property
    def icon_path_url(self):
        return self.icon_path.url if self.icon_path else None

    @property
    def actions_list(self):
        return [action.get_data() for action in self.actions.all()]
    
    @property
    def search_inputs_list(self):
        return [input.get_data() for input in self.search_inputs.all()]
    
    @property
    def table_label_list(self):
        return list(SubCategoryTableLabel.objects.filter(subcategory=self, is_expose=True).order_by('priority').values('name_1c', 'name_display', 'types__name'))
    
    @property
    def template(self):
        print(self.page_elements.all())
        if self.page_elements.filter(template__name="map").exists():
            return "map"
        if self.page_elements.filter(template__name="pieChart").exists():
            return "pieChart"

    @property
    def templates(self):
        return [a.get_data(self) for a in self.page_elements.all().order_by('priority')]

    def get_data(self):
        return {
            "name": self.name,
            "status": self.status.name,
            "priority": self.priority,
            "icon_path": self.icon_path_url,
            "link": self.link,
            "path_get": self.path_get,
            "path_post": self.path_post,
            "path_download_excel": self.path_download_excel,
            "description": self.description,
            "table_labels": self.table_label_list,
            "actions": self.actions_list,
            "inputs": self.search_inputs_list,
            "guid": self.erp_report_guid,
            "templates": self.templates,
        }

    def save(self, *args, **kwargs):
        self.path_download_excel = "/excel{path}".format(path=self.path_get)
        super().save(*args, **kwargs)

    def get_auth_data(self):
        return {
            "username": self.basic_authentication.basic_username if self.basic_authentication else "",
            "password": self.basic_authentication.basic_password if self.basic_authentication else ""
        }

    def get_category(self):
        if Category.objects.filter(links=self).exists():
            category = Category.objects.get(links=self)
            if category.status.id != 3:
                return category
        return None


class TableLabelType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование типа")
    
    class Meta:
        verbose_name = "Тип данных в столбце таблицы"
        verbose_name_plural = "Типы данных в столбце таблицы"

    def __str__(self):
        return self.name


class SubCategoryTableLabel(models.Model):
    subcategory = models.ForeignKey(SubCategory, models.DO_NOTHING, verbose_name="Подкатегория")
    name_1c = models.CharField(max_length=255, verbose_name="Наименование поля в 1с")
    name_display = models.CharField(max_length=255, verbose_name="Наименование у нас")
    priority = models.IntegerField('Приоритет вывода')
    types = models.ForeignKey(TableLabelType, on_delete=models.DO_NOTHING, verbose_name="Тип даннных", null=True)
    is_expose = models.BooleanField(default=True, verbose_name="Используется для показа")

    class Meta:
        verbose_name = "Соотнесение табличных лейблов"
        verbose_name_plural = "Соотнесение табличных лейблов"

    def __str__(self):
        return '{subcategory} - {name_display} - {name_1c}'.format(subcategory=self.subcategory.name,
                                                                   name_display=self.name_display,
                                                                   name_1c=self.name_1c)

    def get_data(self):
        return {
            "name": self.name_display,
            "type": self.types.name if self.types else "string",
        }


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование категории")
    status = models.ForeignKey(BlockStatus, models.DO_NOTHING, default=1, verbose_name="Статус блока")
    description = models.TextField(verbose_name="Описание категории", null=True, blank=True)
    icon_path = models.ImageField(null=True, blank=True, upload_to='images/', verbose_name="Иконка блока")
    link = models.CharField(max_length=255, verbose_name="Адрес")
    links  = models.ManyToManyField(SubCategory, null=True, blank=True)
    priority = models.IntegerField('Приоритет вывода', default=1)

    class Meta:
        verbose_name = "Категория блоков"
        verbose_name_plural = "Категории блоков"

    def __str__(self):
        return self.name

    def get_data(self):
        icon_path = self.icon_path.url if self.icon_path else None
        return {
            "name": self.name,
            "status": self.status.name,
            "priority": self.priority,
            "description": self.description,
            "icon_path": icon_path,
            "link": self.link,
        }

    def get_full_data(self):
        data = self.get_data()
        data["links"] = [link.get_data() for link in self.links.all()]
        return data


class GroupSubcategory(models.Model):
    group = models.ForeignKey(Group, models.DO_NOTHING, unique=True, verbose_name="Группа")
    links = models.ManyToManyField(SubCategory)

    class Meta:
        verbose_name = "Доступ ролей к подкатегориям"
        verbose_name_plural = "Доступ ролей к подкатегориям"

    def __str__(self):
        return self.group.name


class PageElementOptions(models.Model):
    sub_category = models.ForeignKey(SubCategory, models.DO_NOTHING, default=1, verbose_name="Подкатегория")
    content_block = models.ForeignKey(PageElement, models.DO_NOTHING, default=1, verbose_name="Шаблон")
    display_name = models.CharField(max_length=255, verbose_name="Название параметра заголовка")
    select_value = models.CharField(max_length=255, verbose_name="Название параметра откуда беретсся значение для заголовка")
    priority = models.IntegerField('Приоритет вывода')
    types = models.ForeignKey(TableLabelType, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="Тип даннных")
    is_expose = models.BooleanField(default=True, verbose_name="Используется для показа")

    class Meta:
        verbose_name = "Свойства элементов(темплейтов) страницы"
        verbose_name_plural = "Свойства элементов(темплейтов) страницы"

    def __str__(self):
        return 'Подкатегория - {sub_category}| Элемент страницы - {content_block}| Заголовок {display_name}| Значение {select_value}| Приоритет - {priority}, '.format(sub_category=self.sub_category,
               content_block=self.content_block.title,
               display_name=self.display_name,
               select_value=self.select_value,
               priority=self.priority)




