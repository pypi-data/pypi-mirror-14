
from constance import config
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import CsrfViewMiddleware

from .utils import DEFAULT_MARKUP_TYPES


class EpicEditorView(generic.TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):

        if not config.LEONARDO_EPICEDITOR_PUBLIC:
            reason = CsrfViewMiddleware().process_view(request, None, (), {})
            if reason:
                return JsonResponse({})

        return super(EpicEditorView, self).dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        return JsonResponse({})

    def post(self, *args, **kwargs):

        if 'text' in self.request.POST:

            if 'type' in self.request.POST:

                for type in DEFAULT_MARKUP_TYPES:
                    if type[0] == self.request.POST['type']:
                        text = type[1](self.request.POST['text'])

            else:
                text = self.request.POST['text']

            return JsonResponse(
                {'text': text})

        raise Exception
