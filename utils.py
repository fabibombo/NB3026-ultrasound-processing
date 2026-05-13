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

def extract_subimage(image, depth_range, lateral_range, plot=True, db_range=45, IMG_min=None, IMG_max=None):
    """
    Extract a submatrix from a 2D image defined by index ranges and optionallyenvelope
    plot the original image with the submatrix region highlighted.

    Parameters
    ----------
    image : np.ndarray
        2D array of shape (depth, lateral) = (rows, columns).
    depth_range : tuple (int, int)
        Start and end indices for the depth (row) dimension. Supports
        both inclusive (closed) and half‑open intervals.
    lateral_range : tuple (int, int)
        Start and end indices for the lateral (column) dimension.
        Behaves similarly to depth_range.
    plot : bool, optional
        If True, display the original image with a red rectangle outlining
        the extracted submatrix. Default is True.

    Returns
    -------
    subimage : np.ndarray
        The extracted submatrix as a 2D array.
    """
    # Unpack ranges
    depth_start, depth_end = depth_range
    lat_start, lat_end = lateral_range

    depth_sub = slice(depth_start, depth_end + 1)
    lat_sub = slice(lat_start, lat_end + 1)

    subimage = image[depth_sub, lat_sub]

    #log-compression
    if IMG_max is None:
        IMG_max = np.max(image)
    log_env = 20 * np.log10(image / IMG_max)        # 0 at max    
    if IMG_min is None:
        min_db = -db_range
    else:
        min_db = 20 * np.log10(IMG_min / IMG_max)
    log_image = np.clip(log_env, min_db, 0)

    # Optional plotting
    if plot:
        plt.figure(figsize=(8, 6))
        # Plot the whole image
        plt.imshow(log_image, cmap='bone')
        plt.title("Original image with extracted region")

        # Draw rectangle: rectangle edges defined by (left, top, width, height)
        # Coordinates are in pixel indices.
        left = lat_start
        top = depth_start
        width = lat_end - lat_start + 1
        height = depth_end - depth_start + 1

        rect = plt.Rectangle((left, top), width, height,
                             linewidth=2, edgecolor='r', facecolor='none')
        plt.gca().add_patch(rect)

        # Set aspect to auto to avoid distortion
        plt.gca().set_aspect(2.0)
        plt.show()

    return subimage
