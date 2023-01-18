from redicos.models import Redico
from django.http import HttpResponse
from django.contrib import messages


def peut_effacer_redico(func):
    def wrap(request, *args, **kwargs):
        pk  = kwargs["redico_id"]
        red = Redico.objects.get(id=pk)
        is_createur = request.user == red.createur
        zero_evals  = red.nb_evals() == 0
        # print(f'peut_effacer_redico L12')
        if not (is_createur and zero_evals):
            # print(f'peut_effacer_redico L14')
            messages.success(request, "Vous n'êtes pas autorisé à faire cette opération")
            return HttpResponse()
        return func(request, *args, **kwargs)
    return wrap