from django.http import HttpRequest
from django.template.context import RequestContext
from django.template import loader
from django import http
from django.utils.html import escapejs
from django.utils.translation import activate


def js_templates(language, templates):
    compiled_js = ""
    activate(language)
    request = HttpRequest()
    request.LANGUAGE_CODE = language
    context = RequestContext(request, {'LANGUAGE_CODE': language})
    for (name, template) in templates.iteritems():
        template = loader.get_template(template_name=template)
        text = template.render(context)
        compiled_js += "underscore_vars['%s'] = '%s';\r\n" % (name, escapejs(text))
    return http.HttpResponse(compiled_js, 'text/javascript')
