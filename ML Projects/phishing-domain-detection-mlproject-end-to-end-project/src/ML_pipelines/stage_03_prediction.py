import argparse
from src.application_logging.logger import App_Logger
from src.utils.common_utils import read_params, save_model, find_best_model, load_model
from sklearn.preprocessing import StandardScaler
import numpy as np


def prediction(qty_slash_url, length_url, qty_dot_domain, qty_dot_directory, qty_hyphen_directory, file_length,
               qty_underline_directory, asn_ip, time_domain_activation, time_domain_expiration, ttl_hostname,model):
    model = model
    # list = [40, 1000, 20, 15, 20, 10, 10, 10, 15, 10, 10]
    list = []
    list.append(qty_slash_url)
    list.append(length_url)
    list.append(qty_dot_domain)
    list.append(qty_dot_directory)
    list.append(qty_hyphen_directory)
    list.append(file_length)
    list.append(qty_underline_directory)
    list.append(asn_ip)
    list.append(time_domain_activation)
    list.append(time_domain_expiration)
    list.append(ttl_hostname)
    list = np.array(list).reshape(-1, 1)
    Scaled_list = np.array(StandardScaler().fit_transform(list)).T
    result = model.predict(Scaled_list)
    return result[0]


if __name__ == '__main__':
    result = prediction(40, 1000, 20, 15, 20, 10, 10, 10, 15, 10, 10)
    print(result)
