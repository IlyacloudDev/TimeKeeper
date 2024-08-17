from django import template
import markdown


register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    return markdown.markdown(
        text,
        extensions=[
            'fenced_code',  # Поддержка блоков кода
            'codehilite',   # Подсветка синтаксиса
        ],
        extension_configs={
            'codehilite': {
                'linenums': False,  # Включить/выключить номера строк в блоках кода
            }
        }
    )
