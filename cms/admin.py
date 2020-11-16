from django.contrib import admin
from account import models


class SimpleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ['name']


class SubCategoryTableLabelAdmin(admin.ModelAdmin):
    list_filter = ['subcategory__name',]
    ordering = ['subcategory__name', 'priority']


class PolymersAdmin(admin.ModelAdmin):
    change_list_template = "admin/sprav/Polymers/change_list.html"
    list_display = ('shortcode', )
    list_filter = ('subtype__type__name', 'subtype__name', 'plants__name')
    ordering = ['']

class SubCategoryAdmin(admin.ModelAdmin):
    exclude = ('path_download_excel',)
    filter_horizontal = ('page_elements', 'actions')    


class ContentBlockAdmin(admin.ModelAdmin):
    filter_horizontal = ('render_class', )    


class PageElementOptionsAdmin(admin.ModelAdmin):
    list_filter = ['sub_category']
    ordering = ['sub_category__name', 'priority']

# admin.site.register(models.UserCategory)
admin.site.register(models.GroupSubcategory)
admin.site.register(models.Category, SimpleAdmin)
admin.site.register(models.SubCategory, SubCategoryAdmin)
admin.site.register(models.BlockStatus, SimpleAdmin)
admin.site.register(models.SubCategoryAction, SimpleAdmin)
admin.site.register(models.SubCategoryTemplate, SimpleAdmin)
admin.site.register(models.SubCategoryTableLabel, SubCategoryTableLabelAdmin)
admin.site.register(models.BasicAuthentication)
# admin.site.register(models.SubCategoryContentBlock, ContentBlockAdmin)
admin.site.register(models.TableLabelType)
admin.site.register(models.PageElementOptions, PageElementOptionsAdmin)
admin.site.register(models.SearchInputType)
admin.site.register(models.DateDefaultValueType)
admin.site.register(models.ResourceInputParam)
admin.site.register(models.SearchInput)
admin.site.register(models.InputDataType)
admin.site.register(models.PageElement)
admin.site.register(models.SwitchSearchInputPart)
