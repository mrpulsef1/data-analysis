"""Reference values that may be used in multiple tests"""


def ensure_data_type(column_dtypes, df):
    for ch in column_dtypes.keys():
        if ch not in df.columns:
            continue
        if df.dtypes[ch] != column_dtypes[ch]:
            raise TypeError(f"Dtype {ch, df.dtypes[ch]} not equivalent to target dtype {column_dtypes[ch]}")


LAP_DTYPES = {'Time': '<m8[ns]',
              'Driver': 'O',
              'DriverNumber': 'O',
              'LapTime': '<m8[ns]',
              'LapNumber': 'float64',
              'Stint': 'float64',
              'PitOutTime': '<m8[ns]',
              'PitInTime': '<m8[ns]',
              'Sector1Time': '<m8[ns]',
              'Sector2Time': '<m8[ns]',
              'Sector3Time': '<m8[ns]',
              'Sector1SessionTime': '<m8[ns]',
              'Sector2SessionTime': '<m8[ns]',
              'Sector3SessionTime': '<m8[ns]',
              'SpeedI1': 'float64',
              'SpeedI2': 'float64',
              'SpeedFL': 'float64',
              'SpeedST': 'float64',
              'IsPersonalBest': 'bool',
              'Compound': 'O',
              'TyreLife': 'float64',
              'FreshTyre': 'bool',
              'Team': 'O',
              'LapStartTime': '<m8[ns]',
              'LapStartDate': '<M8[ns]',
              'TrackStatus': 'O',
              'Position': 'float64',
              # TODO: fix test
              # 'Deleted': 'O',
              'DeletedReason': 'O',
              'FastF1Generated': 'bool',
              'IsAccurate': 'bool',
              }

CAR_DATA_DTYPES = {'Brake': 'bool',
                   'nGear': 'int64',
                   'DRS': 'int64',
                   'Date': '<M8[ns]',
                   'Throttle': 'int64',
                   'RPM': 'int64',
                   'Speed': 'int64',
                   'Source': 'O',
                   'Time': '<m8[ns]',
                   'SessionTime': '<m8[ns]'}

POS_DATA_DTYPES = {'Date': '<M8[ns]',
                   'Status': 'O',
                   'X': 'int64',
                   'Y': 'int64',
                   'Z': 'int64',
                   'Source': 'O',
                   'Time': '<m8[ns]',
                   'SessionTime': '<m8[ns]'}
