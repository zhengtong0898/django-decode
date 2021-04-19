from django.contrib import admin
from .models import Article, Publication, Author, Tag


# Register your models here.
class ArticleModelAdmin(admin.ModelAdmin):

    # SELECT `simplerelate_article`.`id`,
    #        `simplerelate_article`.`headline`,
    #        `simplerelate_article`.`author_id`,
    #        `simplerelate_article`.`tag_id`,
    #        `simplerelate_author`.`id`,
    #        `simplerelate_author`.`name`,
    #        `simplerelate_tag`.`id`,
    #        `simplerelate_tag`.`name`
    # FROM `simplerelate_article`
    #      INNER JOIN `simplerelate_author` ON (`simplerelate_article`.`author_id` = `simplerelate_author`.`id`)
    #      INNER JOIN `simplerelate_tag` ON (`simplerelate_article`.`tag_id` = `simplerelate_tag`.`id`)
    # ORDER BY `simplerelate_article`.`headline` ASC,
    #          `simplerelate_article`.`id` DESC
    list_select_related = ('author', 'tag')
    pass


admin.site.register(Publication, admin.ModelAdmin)
admin.site.register(Article, ArticleModelAdmin)
admin.site.register(Author, admin.ModelAdmin)
admin.site.register(Tag, admin.ModelAdmin)
