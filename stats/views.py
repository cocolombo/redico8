# from django.shortcuts import render
#
# # Create your views here.
# from django.shortcuts import render
# from evaluations.models import Evaluation
# from django.db.models import Count
# import pandas as pd
# # Create your views here.
# def show_stats(request, redico_id):
#     lst1 = list(Evaluation.objects.filter(redico_id=redico_id, eval__gt=-1).values_list('joueur__username').order_by('-cnt').annotate(cnt=Count('eval')))
#     lst2 = list(Evaluation.objects.filter(redico_id=redico_id, eval=val).values_list('joueur__username').order_by('eval', '-cnt').annotate(cnt=Count('eval')))
#     df1 = pd.DataFrame(lst1, columns=['joueur', 'nb_evals_Total'])
#     df2 = pd.DataFrame(lst2, columns=['joueur', 'nb_evals_' + str(val)])
#     df1['id'] = df1.groupby('joueur').cumcount()
#     df2['id'] = df2.groupby('joueur').cumcount()
#     df = df1.merge(df2, on=['id', 'joueur'], how='outer', suffixes=['_df2', '_df2']).drop('id', axis=1)
#     df['ratio'] = df['nb_evals_' + str(val)] / df.nb_evals_Total
#     df = df.to_html()
#     c = {'stats':df}
#     return render(request, "stats/stats.html", c)
#
#
if __name__ == '__main__':
    pass