from django import template 

register = template.Library() 

@register.filter
def query_count(queryset): 
	return len(queryset.filter(plateform = "imported"))
