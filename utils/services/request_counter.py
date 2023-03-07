from buildings.models import OfficeRequestCounter, StocksRequestCounter, InvestmentObjectsRequestCounter, MainRequestCounter
from django.utils.timezone import now
from auth_user.celery import app


@app.task
def counter(model):

    counter_models = {"Office": OfficeRequestCounter,
                      "Premise": OfficeRequestCounter,
                      "Stock": StocksRequestCounter,
                      "InvestmentObject": InvestmentObjectsRequestCounter,
                      "Main": MainRequestCounter}

    today = now()
    counter_model = counter_models[f'{model}']
    counter_object = counter_model.objects.filter(created_at__year=today.year,
                                                  created_at__month=today.month,
                                                  created_at__day=today.day, )

    if counter_object.exists():
        counter_obj = counter_object.last()
        counter_obj.counter += 1
        counter_obj.save()

    else:
        counter_model.objects.create()
