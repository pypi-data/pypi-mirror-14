from django import template
from django.db.models.loading import get_models, get_model

register = template.Library()

@register.simple_tag
def valor_field(id,valor,aplicacion,modelo):
    mymodel = get_model(app_label=aplicacion, model_name=modelo)
    val_aux=mymodel.objects.filter(id=id).values_list(valor,flat=True)
    return val_aux[0]

@register.filter(name='access')
def access(value, arg):
    return value[arg]



    