import os
import numpy as np
import scipy
import scipy.io as io

def load_mat_parameters(filename_parameters):
    dict_params = {}
    
    data = io.loadmat(filename_parameters)

    dict_params['Microbubble'] = data['Microbubble']
    dict_params['Acquisition'] = data['Acquisition']
    dict_params['SimulationParameters'] = data['SimulationParameters']
    dict_params['Transmit'] = data['Transmit']
    dict_params['Transducer'] = data['Transducer']
    dict_params['Geometry'] = data['Geometry']
    dict_params['Medium'] = data['Medium']
    
    def clean_value(value, field):
        if isinstance(value, np.ndarray):
            if value.size == 0:  # Handle empty arrays
                return ''
            elif value.size == 1:
                # Check if the value is a structured array
                if value.dtype.fields is not None:
                    # Convert structured array to dictionary
                    return {name: clean_value(value[name][0][0], name) 
                           for name in value.dtype.names}
                return value.item()  # Extract scalar for non-structured arrays
            else:
                return value
        return value

    for key in dict_params.keys():
        dict_params[key] = {field: clean_value(data[key][field][0][0], field) for field in data[key].dtype.names}

    return dict_params