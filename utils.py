import os
import numpy as np
import scipy
import scipy.io as io
import h5py

def extract_mat_file(filepath):
    """
    Extract BFData and ReconParams from a MATLAB v7.3 .mat file
    """
    # Load the file
    f = h5py.File(filepath, 'r')
    
    # Extract BFData
    BFData_dict = {}
    bfdata_group = f['BFData']
    
    # Get the complex arrays (IQ_xAM and IQ_xBmode)
    for array_name in ['IQ_xAM', 'IQ_xBMode']:
        if array_name in bfdata_group:
            # Load the raw data
            raw_data = bfdata_group[array_name][:]
            
            # Check the dtype and convert appropriately
            if 'complex' in str(raw_data.dtype):
                # Already complex type
                BFData_dict[array_name] = raw_data
            elif raw_data.dtype == np.float64 or raw_data.dtype == np.float32:
                # Real data only
                BFData_dict[array_name] = raw_data
            else:
                # Try to interpret as complex (MATLAB v7.3 stores complex as real+imag in structured dtype)
                try:
                    # Check if it's a structured array with real and imag fields
                    if raw_data.dtype.names is not None:
                        if 'real' in raw_data.dtype.names and 'imag' in raw_data.dtype.names:
                            complex_data = raw_data['real'] + 1j * raw_data['imag']
                            BFData_dict[array_name] = complex_data
                        else:
                            # Try to access fields dynamically
                            fields = list(raw_data.dtype.names)
                            if len(fields) >= 2:
                                complex_data = raw_data[fields[0]] + 1j * raw_data[fields[1]]
                                BFData_dict[array_name] = complex_data
                            else:
                                BFData_dict[array_name] = raw_data
                    else:
                        BFData_dict[array_name] = raw_data
                except:
                    BFData_dict[array_name] = raw_data
            
            print(f"Loaded {array_name} with shape: {BFData_dict[array_name].shape}, dtype: {BFData_dict[array_name].dtype}")
        elif array_name.lower() in [k.lower() for k in bfdata_group.keys()]:
            # Case-insensitive fallback
            actual_name = next(k for k in bfdata_group.keys() if k.lower() == array_name.lower())
            raw_data = bfdata_group[actual_name][:]
            
            # Same conversion logic
            if 'complex' in str(raw_data.dtype):
                BFData_dict[actual_name] = raw_data
            elif raw_data.dtype == np.float64 or raw_data.dtype == np.float32:
                BFData_dict[actual_name] = raw_data
            else:
                try:
                    if raw_data.dtype.names is not None:
                        if 'real' in raw_data.dtype.names and 'imag' in raw_data.dtype.names:
                            complex_data = raw_data['real'] + 1j * raw_data['imag']
                            BFData_dict[actual_name] = complex_data
                        else:
                            fields = list(raw_data.dtype.names)
                            if len(fields) >= 2:
                                complex_data = raw_data[fields[0]] + 1j * raw_data[fields[1]]
                                BFData_dict[actual_name] = complex_data
                            else:
                                BFData_dict[actual_name] = raw_data
                    else:
                        BFData_dict[actual_name] = raw_data
                except:
                    BFData_dict[actual_name] = raw_data
            
            print(f"Loaded {actual_name} with shape: {BFData_dict[actual_name].shape}, dtype: {BFData_dict[actual_name].dtype}")
    
    # Extract ReconParams
    ReconParams_dict = {}
    reconparams_group = f['ReconParams']
    
    for key in reconparams_group.keys():
        item = reconparams_group[key]
        data = item[:] if isinstance(item, h5py.Dataset) else item
        
        # Convert to scalar if it's a 1x1 array
        if isinstance(item, h5py.Dataset) and data.size == 1:
            data = data.item()
        # Remove any extra dimensions
        elif isinstance(data, np.ndarray) and data.size == 1:
            data = data.item()
        
        ReconParams_dict[key] = data

    ReconParams_dict['GridScaleX'] = ReconParams_dict['GridScaleZ'] #manual fix for now
    
    f.close()
    return BFData_dict, ReconParams_dict