class FormData:
    def __init__(self):
        self.sku = None
        self.national_inv = None
        self.lead_time = None
        self.in_transit_qty = None
        self.forecast_3_month = None
        self.forecast_6_month = None
        self.forecast_9_month = None
        self.sales_1_month = None
        self.sales_3_month = None
        self.sales_6_month = None
        self.sales_9_month = None
        self.min_bank = None
        self.potential_issue = None
        self.pieces_past_due = None
        self.perf_6_month_avg = None
        self.perf_12_month_avg = None
        self.local_bo_qty = None
        self.deck_risk = None
        self.oe_constraint = None
        self.ppap_risk = None
        self.stop_auto_buy = None
        self.rev_stop = None


def get_form_data(request):
    dict_map_bool = {'True': 'Yes', 'False': 'No'}
    form_data = FormData()
    form_data.sku = [int(request.POST.get('sku'))]
    form_data.national_inv = [int(request.POST.get('national_inv'))]
    form_data.lead_time = [int(request.POST.get('lead_time'))]
    form_data.in_transit_qty = [int(request.POST.get('in_transit_qty'))]
    form_data.forecast_3_month = [int(request.POST.get('forecast_3_month'))]
    form_data.forecast_6_month = [int(request.POST.get('forecast_6_month'))]
    form_data.forecast_9_month = [int(request.POST.get('forecast_9_month'))]
    form_data.sales_1_month = [int(request.POST.get('sales_1_month'))]
    form_data.sales_3_month = [int(request.POST.get('sales_3_month'))]
    form_data.sales_6_month = [int(request.POST.get('sales_6_month'))]
    form_data.sales_9_month = [int(request.POST.get('sales_9_month'))]
    form_data.min_bank = [int(request.POST.get('min_bank'))]
    potential_issue = request.POST.get('potential_issue', 'False')
    form_data.potential_issue = [
        'Yes' if potential_issue in dict_map_bool and dict_map_bool[potential_issue] == 'Yes' else 'No']
    form_data.pieces_past_due = [int(request.POST.get('pieces_past_due'))]
    form_data.perf_6_month_avg = [float(request.POST.get('perf_6_month_avg'))]
    form_data.perf_12_month_avg = [float(request.POST.get('perf_12_month_avg'))]
    form_data.local_bo_qty = [int(request.POST.get('local_bo_qty'))]
    deck_risk = request.POST.get('deck_risk', 'False')
    form_data.deck_risk = ['Yes' if deck_risk in dict_map_bool and dict_map_bool[deck_risk] == 'Yes' else 'No']
    oe_constraint = request.POST.get('oe_constraint', 'False')
    form_data.oe_constraint = [
        'Yes' if oe_constraint in dict_map_bool and dict_map_bool[oe_constraint] == 'Yes' else 'No']
    ppap_risk = request.POST.get('ppap_risk', 'False')
    form_data.ppap_risk = ['Yes' if ppap_risk in dict_map_bool and dict_map_bool[ppap_risk] == 'Yes' else 'No']
    stop_auto_buy = request.POST.get('stop_auto_buy', 'False')
    form_data.stop_auto_buy = [
        'Yes' if stop_auto_buy in dict_map_bool and dict_map_bool[stop_auto_buy] == 'Yes' else 'No']
    rev_stop = request.POST.get('rev_stop', 'False')
    form_data.rev_stop = ['Yes' if rev_stop in dict_map_bool and dict_map_bool[rev_stop] == 'Yes' else 'No']

    return form_data.__dict__
