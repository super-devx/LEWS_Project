import pandas as pd
import numpy as np
from login.views import cursor

def prepareQuery(field_name, values):
    if not isinstance(values, list):
        values = [values]
    quoted_values = ["'{}'".format(v) for v in values]
    return f"{field_name} IN ({','.join(quoted_values)})"

def get_sensor_data(sensor_id, from_format, to_format):
    """
    Fetch raw sensor data for a given sensor within a time range.
    """
    query = f"SELECT receive_time, sensor_value FROM sensor_data WHERE "
    query += prepareQuery('sensor_id', [sensor_id])
    query += f" AND receive_time <= (to_timestamp('{to_format}', 'yyyy-mm-dd hh24:mi:ss')) "
    query += f" AND receive_time >= (to_timestamp('{from_format}', 'yyyy-mm-dd hh24:mi:ss')) "
    query += " ORDER BY receive_time"
    
    cursor.execute(query)
    records = cursor.fetchall()
    
    import logging
    # Return as DataFrame
    df = pd.DataFrame(records, columns=['receive_time', 'sensor_value'])
    if not df.empty:
        df['receive_time'] = pd.to_datetime(df['receive_time'], errors='coerce')
        df['sensor_value'] = pd.to_numeric(df['sensor_value'], errors='coerce')
        
        # Drop rows where either timestamp or value is invalid/null
        # This prevents NotImplementedError during time-weighted interpolation later
        valid_rows_before = len(df)
        df = df.dropna(subset=['receive_time', 'sensor_value'])
        dropped_rows = valid_rows_before - len(df)
        
        if dropped_rows > 0:
            logging.warning(f"Sensor {sensor_id}: Dropped {dropped_rows} rows due to NULL or invalid receive_time/sensor_value records.")
            
    return df

def analyze_cross_correlation(sensor_a, sensor_b, from_format, to_format):
    """
    Perform cross-correlation analysis on two sensors.
    """
    try:
        df_a = get_sensor_data(sensor_a, from_format, to_format)
        df_b = get_sensor_data(sensor_b, from_format, to_format)
        
        if df_a.empty or df_b.empty:
            return {'error': 'Insufficient data for one or both sensors.'}
        
        # Set time as index
        df_a.set_index('receive_time', inplace=True)
        df_b.set_index('receive_time', inplace=True)
        
        import logging
        logging.info(f"Selected Sensor A: {sensor_a}, Selected Sensor B: {sensor_b}")
        logging.info(f"Sensor A Records: {len(df_a)}, Sensor B Records: {len(df_b)}")
        
        # Remove duplicate indices
        df_a = df_a[~df_a.index.duplicated(keep='first')].sort_index()
        df_b = df_b[~df_b.index.duplicated(keep='first')].sort_index()
        
        # Merge on timestamp using an outer join to keep all real data points
        df_merged = pd.merge(df_a, df_b, left_index=True, right_index=True, how='outer', suffixes=('_a', '_b'))
        
        # Interpolate missing values by time to align unsynchronized sensor readings
        df_merged = df_merged.interpolate(method='time').dropna()
        
        logging.info(f"Aligned Records: {len(df_merged)}")
        logging.info(f"Sensor A Unique Values: {df_merged['sensor_value_a'].nunique()}, Sensor B Unique Values: {df_merged['sensor_value_b'].nunique()}")
        
        if len(df_merged) < 2:
            return {'error': 'Insufficient overlapping data points after alignment.'}
            
        # Attempt Pearson correlation coefficient
        corr = None
        has_variance = df_merged['sensor_value_a'].nunique() > 1 and df_merged['sensor_value_b'].nunique() > 1
        
        if has_variance:
            corr = df_merged['sensor_value_a'].corr(df_merged['sensor_value_b'], method='pearson')
            
            # Fallback to Spearman if Pearson fails or returns NaN
            if pd.isna(corr):
                logging.info("Pearson correlation failed or returned NaN. Attempting Spearman fallback.")
                corr = df_merged['sensor_value_a'].corr(df_merged['sensor_value_b'], method='spearman')
        else:
            logging.info("Skipping correlation calculation because one or both sensors have constant data.")
            
        # Format interpretation
        interpretation = "No Significant Correlation"
        if pd.notna(corr):
            abs_corr = abs(corr)
            if abs_corr >= 0.8:
                strength = "Strong"
            elif abs_corr >= 0.5:
                strength = "Moderate"
            elif abs_corr >= 0.2:
                strength = "Weak"
            else:
                strength = "No Significant"
                
            if strength != "No Significant":
                direction = "Positive" if corr > 0 else "Negative"
                interpretation = f"{strength} {direction} Correlation"
        else:
            interpretation = "Correlation Unavailable"
            
        # Prepare data for frontend Plotly
        # We want to send back the aligned times and values
        times = df_merged.index.strftime('%Y-%m-%dT%H:%M:%S').tolist()
        values_a = df_merged['sensor_value_a'].tolist()
        values_b = df_merged['sensor_value_b'].tolist()
    except Exception as e:
        import traceback
        import logging
        error_trace = traceback.format_exc()
        logging.error(f"Cross-correlation error during execution:\n{error_trace}")
        return {'error': 'Unable to perform cross-correlation analysis. Please verify that both sensors contain valid time-series data.'}
    
    return {
        'success': True,
        'correlation': float(corr) if pd.notna(corr) else None,
        'interpretation': interpretation,
        'correlation_warning': 'Correlation coefficient could not be calculated reliably for the selected sensors. Time-series comparison is displayed below.' if pd.isna(corr) else None,
        'times': times,
        'values_a': values_a,
        'values_b': values_b
    }
