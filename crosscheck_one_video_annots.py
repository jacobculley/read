#!/usr/bin/env python3
"""

Author: Gurkirt Singh
Created on 29th April 2019

Please do not distribute it.

"""

import json, os

base_dir = '/home/reza/'
base_dir = '/home/gurkirt/Downloads/annos/'
base_dir = '/home/gurkirt/Downloads/Robot-Car-Annotations/done/'
base_dir = './'


def main(annofile):
    input_labels = ['AV', 'Amber', 'Break', 'Bus', 'BusStop', 'Car', 'Cyc', 'EmVeh', 'Green', 'HazLit', 'IncatLft', 'IncatRht', 'IncomBusLane', 'IncomCycLane', 'IncomLane', 'Jun', 'LarVeh', 'LftParking', 'LftPav', 'MedVeh', 'Mobike', 'Mov', 'MovAway', 'MovLft', 'MovRht', 'MovTow', 'OthTL', 'OutgoBusLane', 'OutgoCycLane', 'OutgoLane', 'Ovtak', 'Pav', 'Ped', 'PushObj', 'Red', 'Rev', 'RhtPav', 'SmalVeh', 'Stop', 'TL', 'TurLft', 'TurRht', 'VehLane', 'Wait2X', 'Xing', 'XingFmLft', 'XingFmRht', 'black', 'parking', 'rightParking', 'xing']
    # AV,Car,SmalVeh,MedVeh,LarVeh,Bus,Mobike,Cyc,Ped,TL,OthTL,EmVeh,Red,Amber,Green,black,MovAway,MovTow,Mov,Rev,Break,Stop,IncatLft,IncatRht,HazLit,TurLft,TurRht,MovRht,MovLft,MerTo,Ovtak,Wait2X,XingFmLft,XingFmRht,Xing,PushObj,OutgoBusLane,IncomBusLane,OutgoCycLane,IncomCycLane,VehLane,OutgoLane,IncomLane,LftPav,RhtPav,Pav,Jun,TL,OthTL,xing,BusStop
    agent_labels = ['AV', 'EmVeh', 'Car', 'SmalVeh', 'MedVeh', 'LarVeh', 'Bus', 'Mobike', 'Cyc', 'Ped', 'TL', 'OthTL']
    action_labels = ['Red', 'Amber', 'Green', 'black', 'MovAway', 'MovTow', 'Mov', 'Rev', 'Break', 'Stop', 'IncatLft', 'IncatRht', 'HazLit', 'TurLft', 'TurRht', 'MovRht', 'MovLft', 'Ovtak', 'Wait2X', 'XingFmLft', 'XingFmRht', 'Xing', 'PushObj']
    loc_labels = ['OutgoBusLane', 'IncomBusLane', 'OutgoCycLane', 'IncomCycLane', 'VehLane', 'OutgoLane', 'IncomLane', 'LftPav', 'RhtPav', 'Pav', 'Jun', 'xing', 'BusStop', 'parking', 'LftParking', 'rightParking']
    core_actions = ['MovAway', 'MovTow', 'Mov', 'Rev', 'Stop', 'XingFmRht', 'XingFmLft']
    core_actions_tl = ['Red', 'Amber', 'Green', 'black']
    print(' # agent tags', len(agent_labels), '# action tags', len(action_labels), ' #loc tags', len(loc_labels), ' # total tags', len(input_labels))

    print('length of action labels', len(action_labels), sorted(action_labels))

    all_actions = dict()
    with open(annofile, 'r') as f:
        db = json.load(f)

    frames = db['frames']
    print('Number of frames annotated', len(frames.keys()))

    frame_keys = [int(f) for f in sorted(frames.keys())]
    # max_num = 10
    count = 0
    for f in sorted(frame_keys):
        annots = frames[str(f)]
        frame_av_actions = []
        for anno in annots:
            width = anno['width']
            height = anno['height']
            box = anno['box']
            tags = anno['tags']
            box_id = anno['id']

            box = [float(box['x1']) / width, float(box['y1']) / height, float(box['x2']) / width,
                   float(box['y2']) / height]
            action_tags = []
            loc_tags = []
            agc = 0;
            alc = 0
            agent_label = ''
            for tag in tags:
                if tag in agent_labels:
                    agent_label = tag
                    agc += 1
                if tag in action_labels:
                    action_tags.append(tag)
                    alc += 1
                if tag in loc_labels:
                    loc_tags.append(tag)

            ####### Correctection Starts here ############
            if agc != 1:
                print('There must/atleast be only one Agent label per box but there are', agc, 'in frame number', f); count += 1
                print(agent_label, action_tags, loc_tags, count)
            if len(loc_tags) == 0 and agent_label not in ['TL', 'AV', 'OthTL']:
                print('There must be at least one location label per box but there are', len(loc_tags), 'in frame number', f); count += 1
                print(agent_label, action_tags, loc_tags, count)

            if len(loc_tags) != 0 and agent_label in ['TL', 'OthTL']:
                print(agent_label, 'should not have a location label but there are', loc_tags, 'in frame number', f); count += 1
                print(agent_label, action_tags, loc_tags, count)

            if agent_label in ['TL', 'AV', 'OthTL'] and len(
                    action_tags) > 1:  ## Traffic lights can only have one action label
                print(agent_label, 'should only have one action label but there are', action_tags, 'in frame number', f); count += 1
                print(agent_label, action_tags, loc_tags, count)

            if len(action_tags) < 1:
                print(agent_label, 'should at least one action label but there is none', action_tags, 'in frame number', f); count += 1
                print(agent_label, action_tags, loc_tags, count)
            if agent_label not in ['AV', 'TL', 'OthTL']:
                core_present = 0
                for act in action_tags:
                    if act in core_actions:
                        core_present += 1
                if core_present != 1:
                    print(agent_label, 'should only have one core action label but there are', core_present, 'in frame number', f, count); count += 1
                    print(agent_label, action_tags, loc_tags)
            if agent_label in ['TL', 'OthTL']:
                core_present = 0
                for act in action_tags:
                    if act in core_actions_tl:
                        core_present += 1
                if core_present != 1:
                    print(agent_label, 'should only have one core action label but there are', core_present, 'in frame number', f, count); count += 1
                    print(agent_label, action_tags, loc_tags)

            if agent_label not in ['AV', 'Ped']:
                if 'Mov' in action_tags:
                    print('Mov action tag can not be labeled on', agent_label, 'in frame number', f, count); count += 1
                    print(agent_label, action_tags, loc_tags)

            if (box[0] + box[2]) / 2 > 0.5:  # box on right of screen
                if 'LftPav' in loc_tags:
                    print('LftPav action tag on right side of the screen in frame number', f, count); count += 1
                for loc_tag in 'OutgoBusLane', 'OutgoCycLane', 'OutgoLane':
                    if loc_tag in loc_tags:
                        print(loc_tag, 'location tag on right side of the screen in frame number', f, count); count += 1

            if (box[0] + box[2]) / 2 < 0.5:
                if 'RhtPav' in loc_tags:
                    print('RhtPav action tag on left side of the screen in frame number', f, count); count += 1
                for loc_tag in 'IngoBusLane', 'IngoCycLane', 'IngoLane':
                    if loc_tag in loc_tags:
                        print(loc_tag, 'location tag on left side of the screen in frame number', f, count); count += 1

            if agent_label == 'Mobike' and 'Rev' in action_tags:
                print('Motorbike in reverse? Frame number', f, count); count += 1

            if 'xing' in loc_tags and agent_label != 'Ped':
                print(agent_label, 'crossing the road? frame number', f, count); count += 1

            # print(len(used_agtaction_tags))
            if agent_label == 'AV':
                frame_av_actions = action_tags

            for act in action_tags:
                if act in all_actions.keys():
                    all_actions[act] += 1
                else:
                    all_actions[act] = 1

        ## Get frame-level action labels
        if len(frame_av_actions) < 1:  # AV must have only one label
            print(
                'AV must have an action label, but there is none, this means the AV is not properly annotated in frame', f, count); count += 1

    cc = 0
    new_str = ""
    for idx, cl in enumerate(sorted(all_actions)):
        if all_actions[cl] > 0:
            print(cc, idx, cl, all_actions[cl])
            cc += 1
            new_str = "{:s},\'{:s}\'".format(new_str, cl)
    print(new_str)


if __name__ == '__main__':
    annofiles = os.listdir(base_dir)
    annofiles = [af for af in annofiles if af.endswith('.json')]
    for annofile in annofiles:
        print('\n\n\n\n\n annofile', annofile, '\n\n\n\n\n\n')
        main(base_dir + annofile)
