"""
Some functions that can be used as 'Nodes' within a
Nipype (fMRI preprocessing) workflow.

Lukas Snoek, University of Amsterdam
"""

from __future__ import division, print_function


def parse_presentation_logfile(in_file, con_names, con_codes, con_design=None,
                               pulsecode=30, write_bfsl=False, verbose=False):
    """ Parses Presentation (Neurobs) logfiles.

    Parses a Presentation-logfile and extracts stimulus/event times and
    durations given their corresponding codes in the logfile.

    Parameters
    ----------
    in_file : str
        Absolute path to .log file
    con_names : list of str
        List of condition names.
    con_codes : list of list (of int or str)
        List of lists, which contain condition codes corresponding to conditon
        names (e.g. [[1, 100], [101, 200], [201, 300]])
    con_design : list of str, {'univar', 'multivar'}
        What 'design' does each condition have? Univar = one regressor
        per condition; multivar = each trial has one regressor.
    pulsecode : int {default: 30}
        Code used for (first) pulse logging.
    write_bfsl : bool
        Whether to write out .bfsl files for each regressor.
    verbose : bool {default: False}
        Whether to print out extra info about process.

    Returns
    -------
    subject_info : 'Bunch' object
        Bunch object (nipype.interfaces.base.Bunch), including information about
        regressor names, duration, and onsets.
    """

    from nipype.interfaces.base import Bunch
    import pandas as pd
    import numpy as np
    import os
    import glob

    if verbose:
        print('Processing %s' % in_file)

    base_dir = os.path.dirname(in_file)
    _ = [os.remove(x) for x in glob.glob(os.path.join(base_dir, '*.bfsl'))]

    if not con_design:
        con_design = ['univar'] * len(con_names)

    df = pd.read_table(in_file, sep='\t', skiprows=3, header=0,
                       skip_blank_lines=True)

    # Convert to numeric and drop all rows until first pulse
    df['Code'] = df['Code'].astype(str)
    df['Code'] = [np.float(x) if x.isdigit() else x for x in df['Code']]
    pulse_idx = np.where(df['Code'] == pulsecode)[0]

    if len(pulse_idx) > 1:
        pulse_idx = int(pulse_idx[0])

    df = df.drop(range(pulse_idx))

    # Clean up unnecessary columns
    df.drop(['Uncertainty', 'Subject', 'Trial', 'Uncertainty.1', 'ReqTime',
             'ReqDur', 'Stim Type', 'Pair Index'], axis=1, inplace=True)

    # pulse_t = absolute time of first pulse
    pulse_t = df['Time'][df['Code'] == pulsecode].iloc[0]
    df['Time'] = (df['Time']-float(pulse_t)) / 10000.0
    df['Duration'] = df['Duration'] / 10000.0

    trial_names = []
    trial_onsets = []
    trial_durations = []

    for i, code in enumerate(con_codes):
        to_write = pd.DataFrame()
        if len(code) > 1:
            if type(code[0]) == int:
                idx = df['Code'].isin(range(code[0], code[1]+1))
        elif len(code) == 1 and type(code[0]) == str:
            idx = [code[0] in x if type(x) == str else False for x in df['Code']]
            idx = np.array(idx)
        else:
            idx = df['Code'] == code

        # Generate dataframe with time, duration, and weight given idx
        to_write['Time'] = df['Time'][idx]
        to_write['Duration'] = df['Duration'][idx]
        to_write['Duration'] = [np.round(x, decimals=2) for x in to_write['Duration']]
        to_write['Weight'] = np.ones((np.sum(idx), 1))
        to_write['Name'] = [con_names[i] + '_%i' % (j+1) for j in range(idx.sum())]

        if con_design[i] == 'univar':
            trial_names.append(to_write['Name'].tolist())
            trial_onsets.append(to_write['Time'].tolist())
            trial_durations.append(to_write['Duration'].tolist())
        elif con_design[i] == 'multivar':
            _ = [trial_names.append([x]) for x in to_write['Name'].tolist()]
            _ = [trial_onsets.append([x]) for x in to_write['Time'].tolist()]
            _ = [trial_durations.append([x]) for x in to_write['Duration'].tolist()]

        if write_bfsl:

            if con_design[i] == 'univar':
                to_write.drop('Name', axis=1, inplace=True)
                name = os.path.join(base_dir, con_names[i] + '.bfsl')
                to_write.to_csv(name, sep='\t', index=False, header=False)

            elif con_design[i] == 'multivar':

                for row in to_write.iterrows():
                    ev_name = row[1]['Name'] + '.bfsl'
                    name = os.path.join(base_dir, ev_name)
                    df_tmp = pd.DataFrame({'Time': row[1]['Time'],
                                           'Duration': row[1]['Duration'],
                                           'Weight': row[1]['Weight']}, index=[0])
                    df_tmp.to_csv(name, index=False, sep='\t', header=False)

    subject_info = Bunch(conditions=con_names,
                         onsets=trial_onsets,
                         durations=trial_durations,
                         amplitudes=None,
                         regressor_names=con_names,
                         regressors=None)

    if verbose:
        print(subject_info)

    return subject_info


# Only for testing
if __name__ == '__main__':

    testfile = '/home/lukas/Nipype_tryout/working_directory/sub003/func_hww/sub003_HWW.log'
    con_names = ['Action', 'Interoception', 'Situation', 'Cue']
    con_codes = [[100, 199], [200, 299], [300, 399], ['Cue']]
    con_design = ['multivar', 'univar', 'univar', 'univar']

    parse_presentation_logfile(testfile, con_names, con_codes, con_design,
                               pulsecode=30, write_bfsl=True, verbose=True)
