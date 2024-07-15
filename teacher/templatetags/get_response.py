from django import template
register = template.Library()

@register.filter
def get_response(responses, pk):
    return responses.response.get(answer_to__pk = pk).answer

@register.filter
def get_response_file(responses, pk):
    return responses.response.get(answer_to__pk = pk).file.url

@register.filter
def get_file_ext(responses, pk):
    return responses.response.get(answer_to__pk = pk).extension()