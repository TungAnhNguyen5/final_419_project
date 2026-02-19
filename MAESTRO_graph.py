from mido import MidiFile
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def MAESTRO_midi_graph(file_name, plot_type='jointplot', axes_=False, 
                       palette='icefire', gridsize=88, figwidth=20, 
                       figheight=10, save_path=None):
    # Import and parse MIDI file using MidiFile from the mido package
    mid = MidiFile(file_name) 
    # Filter out the meta data in Track 0
    message_list = []
    for i in mid.tracks[1][1:-1]: 
        message_list.append(i)   

    # Transform the MIDI messages to strings
    message_strings = [str(x) for x in message_list]

    # Split message strings into attributes
    message_strings_split = [msg.split(" ") for msg in message_strings]

    # Extract message types
    message_type = [item[0] for item in message_strings_split]
    df1 = pd.DataFrame(message_type, columns=['message_type'])

    # Extract attributes into dictionaries
    attributes = [item[1:] for item in message_strings_split]
    attributes_dict = []
    for attr_list in attributes:
        attr_dict = {}
        for attr in attr_list:
            if "=" in attr:
                key, val = attr.split("=")
                attr_dict[key] = val
        attributes_dict.append(attr_dict)

    df2 = pd.DataFrame.from_records(attributes_dict)
    df_complete = pd.concat([df1, df2], axis=1)

    # Convert and clean up
    df_complete['time'] = pd.to_numeric(df_complete['time'], errors='coerce').fillna(0)
    df_complete['time_elapsed'] = df_complete['time'].cumsum()

    df_filtered = df_complete[df_complete['message_type'] == 'note_on'].copy()
    df_filtered = df_filtered[df_filtered['velocity'] != '0']
    df_filtered['note'] = pd.to_numeric(df_filtered['note'], errors='coerce')
    df_filtered = df_filtered.dropna(subset=['note'])
    df_filtered.loc[:, 'note'] = df_filtered['note'].astype(int)

    # Drop unnecessary columns
    drop_cols = ['channel', 'value', 'control', 'program', 'time']
    df_filtered.drop(columns=[col for col in drop_cols if col in df_filtered.columns], inplace=True)

    # Add padding for plot clarity
    first_row = {
        'message_type': 'note_on', 'note': 0, 'velocity': 0,
        'time_elapsed': -df_filtered['time_elapsed'].iloc[-1] * 0.05
    }
    last_row = {
        'message_type': 'note_on', 'note': 127, 'velocity': 0,
        'time_elapsed': df_filtered['time_elapsed'].iloc[-1] * 1.05
    }
    df_final = pd.concat([pd.DataFrame([first_row]), df_filtered, pd.DataFrame([last_row])], ignore_index=True)

    # Plotting
    sns.set_style('white')

    if plot_type == 'kdeplot':
        fig, ax = plt.subplots(1, 1, figsize=(figwidth, figheight))
        g = sns.kdeplot(data=df_final, x='time_elapsed', y='note', cmap=palette, fill=True)
        plt.ylim(16, 113)
        if not axes_:
            ax.set_xlabel('')
            ax.set_ylabel('')
            g.set(xticklabels=[], yticklabels=[])
            plt.axis('off')
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        plt.show()

    elif plot_type == 'jointplot':
        g = sns.jointplot(
            data=df_final,
            x='time_elapsed',
            y='note',
            kind='hex',
            cmap=palette,
            xlim=(df_final['time_elapsed'].min(), df_final['time_elapsed'].max()),
            ylim=(16, 113),
            joint_kws=dict(gridsize=gridsize)
        )
        g.fig.set_figwidth(figwidth)
        g.fig.set_figheight(figheight)
        if not axes_:
            sns.despine(left=True, bottom=True)
            g.set_axis_labels('', '')
            g.ax_marg_x.set_visible(False)
            g.ax_marg_y.set_visible(False)
            g.ax_joint.set_xticklabels([])
            g.ax_joint.set_yticklabels([])
        if save_path:
            g.fig.savefig(save_path, bbox_inches='tight')
        plt.show()
    else:
        raise ValueError("plot_type must be 'jointplot' or 'kdeplot'")