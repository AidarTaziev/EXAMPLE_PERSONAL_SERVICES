from django.db import models


class RenderCSS(models.Model):
    css_property = models.CharField(verbose_name="Свойство CSS", max_length=255)
    css_value = models.CharField(verbose_name="Значение свойства CSS", max_length=255)

    class Meta:
        verbose_name = "CSS свойство"
        verbose_name_plural = "CSS свойства"

    def __str__(self):
        return f"{self.css_property}:{self.css_value}"

    def get_data(self):
        return {self.css_property: self.css_value}


class RenderClass(models.Model):
    name = models.CharField(verbose_name="Наименование класса отрисовки", max_length=255)
    styles = models.ManyToManyField(RenderCSS, null=True, blank=True, verbose_name="Стили класса")

    class Meta:
        verbose_name = "Класс отрисовки"
        verbose_name_plural = "Классы отрисовки"

    def __str__(self):
        return self.name

    def get_styles(self):
        result = dict()
        for style in self.styles.all():
            result.update(style.get_data())

        return result


# class RenderTemplate(models.Model):
#     render_classes = models.ManyToManyField(RenderClass)
#     name = models.CharField(verbose_name="Наименование шаблоне", max_length=255)

#     class Meta:
#         verbose_name = "Шаблон отрисовки"
#         verbose_name_plural = "Шаблоны отрисовки"

    
#     def __str__(self):
#         return self.name

