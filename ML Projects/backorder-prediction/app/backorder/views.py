import pandas as pd
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from backorder.pipeline import BackorderPredictor
from backorder.utils import get_form_data
from .serializers import ContactUsSerializer

backorder_predictor = BackorderPredictor()
backorder_predictor._load_model_files()


def index(request):
    return render(request, 'backorder/index.html')


@method_decorator(csrf_exempt, name='dispatch')
class PredictView(View):
    http_method_names = ['post', 'get']

    def get(self, request, *args, **kwargs):
        return render(request, 'backorder/predict.html')

    def post(self, request, *args, **kwargs):
        file = self.request.FILES.get('file')
        if file:
            file = request.FILES['file']
            df = pd.read_csv(file)
            y_pred = backorder_predictor.predict(df)
            skus = df['sku'].values.tolist()
            comments = [f"Product {int(sku)} is predicted to be on backorder." if int(
                pred) == 1 else f"Product {int(sku)} is predicted to not be on backorder." for sku, pred in
                        zip(skus, y_pred)]

            context = {
                'comments': comments
            }
            return render(request, 'backorder/result_bulk.html', context)

        elif all(key in request.POST for key in
                 ['sku', 'national_inv', 'lead_time', 'in_transit_qty', 'forecast_3_month', 'forecast_6_month',
                  'forecast_9_month', 'sales_1_month', 'sales_3_month', 'sales_6_month', 'sales_9_month', 'min_bank',
                  'pieces_past_due', 'perf_6_month_avg', 'perf_12_month_avg', 'local_bo_qty']):
            form_data = get_form_data(request)
            df = pd.DataFrame(form_data)

            y_pred = backorder_predictor.predict(df)

            comment = f"The product {int(request.POST.get('sku'))} will be on backorder" if int(
                y_pred[0]) == 1 else f"The product will not be on backorder"
            y_pred = "Yes" if int(y_pred[0]) == 1 else "No"

            context = {
                'y_pred': y_pred,
                'comment': comment,
            }
            return render(request, 'backorder/result_single.html', context)

        else:
            return render(request, 'backorder/predict.html')


def about_us(request):
    return render(request, 'backorder/about_us.html')


def contact_us(request):
    if request.method == 'GET':
        return render(request, 'backorder/contact_us.html')

    if request.method == 'POST':
        data = request.POST.copy()
        serializer = ContactUsSerializer(data=data)
        if serializer.is_valid():
            # Save the data to the database
            serializer.save()
            # Return a success response
            return render(request, 'backorder/contact_us_thanks.html')
        else:
            # Return an error response
            return JsonResponse(serializer.errors, status=400)
    else:
        return render(request, 'backorder/contact_us.html')

    return render(request, 'backorder/contact_us.html', {'serializer': serializer})
