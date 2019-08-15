import os
import cv2
import json

FONT = cv2.FONT_HERSHEY_SIMPLEX


LABELS = {
    'AV': 'AV',
    'Amber': 'Amber Light',
    'Break': 'Breaking',
    'Bus': 'Bus',
    'BusStop': 'Bus Stop',
    'Car': 'Car',
    'Cyc': 'Cyclist',
    'EmVeh': 'Emergency Vehicle',
    'Green': 'Green Light',
    'HazLit': 'Hazard Lights',
    'IncatLft': 'Indicting Left',
    'IncatRht': 'Indicating Right',
    'IncomBusLane': 'Incoming Bus Lane',
    'IncomCycLane': 'Incom Bike Lane',
    'IncomLane': 'Incoming Lane',
    'Jun': 'Junction',
    'LarVeh': 'Large Vehicle',
    'LftParking': 'Left Parking',
    'LftPav': 'Left Pavement',
    'MedVeh': 'Medium Vehicle',
    'Mobike': 'Motorbike',
    'Mov': 'Moving',
    'MovAway': 'Moving Away',
    'MovLft': 'Moving Left',
    'MovRht': 'Moving Right',
    'MovTow': 'Moving Towards',
    'OthTL': 'Other Traffic Light',
    'OutgoBusLane': 'Outgoing Bus Lane',
    'OutgoCycLane': 'Outgoing Cyclist Lane',
    'OutgoLane': 'Outgoing Lane',
    'Ovtak': 'Overtaking',
    'Pav': 'Pavement',
    'Ped': 'Pedestrian',
    'PushObj': 'Pushing an Object',
    'Red': 'Red Light',
    'Rev': 'Reversing',
    'RhtPav': 'Right Pavement',
    'SmalVeh': 'Small Vehicle',
    'Stop': 'Stopped',
    'TL': 'Traffic Light',
    'TurLft': 'Turning Left',
    'TurRht': 'Turning Right',
    'VehLane': 'Vehicle Lane',
    'Wait2X': 'Waiting to cross',
    'Xing': 'Crossing',
    'XingFmLft': 'Crossing From Left',
    'XingFmRht': 'Crossing From Right',
    'black': 'Black',
    'parking': 'Parking',
    'rightParking': 'Right Parking',
}

COLOURS = {
    'AV': (0, 0, 0),
    'Amber': (255, 191, 0),
    'Break': (255, 0, 0),
    'Bus': (0, 255, 255),
    'BusStop': (0, 0, 0),
    'Car': (0, 255, 0),
    'Cyc': (255, 128, 0),
    'EmVeh': (255, 0, 0),
    'Green': (0, 0, 0),
    'HazLit': (255, 191, 0),
    'IncatLft': (255, 191, 0),
    'IncatRht': (255, 191, 0),
    'IncomBusLane': (0, 0, 0),
    'IncomCycLane': (0, 0, 0),
    'IncomLane': (0, 0, 0),
    'Jun': (0, 0, 0),
    'LarVeh': (0, 255, 255),
    'LftParking': (0, 0, 0),
    'LftPav': (0, 0, 0),
    'MedVeh': (0, 255, 128),
    'Mobike': (255, 255, 0),
    'Mov': (0, 0, 0),
    'MovAway': (0, 0, 0),
    'MovLft': (0, 0, 0),
    'MovRht': (0, 0, 0),
    'MovTow': (0, 0, 0),
    'OthTL': (255, 153, 255),
    'OutgoBusLane': (0, 0, 0),
    'OutgoCycLane': (0, 0, 0),
    'OutgoLane': (0, 0, 0),
    'Ovtak': (255, 0, 0),
    'Pav': (0, 0, 0),
    'Ped': (255, 0, 255),
    'PushObj': (0, 0, 0),
    'Red': (0, 0, 0),
    'Rev': (0, 0, 0),
    'RhtPav': (0, 0, 0),
    'SmalVeh': (255, 0, 127),
    'Stop': (0, 0, 0),
    'TL': (255, 153, 255),
    'TurLft': (0, 0, 0),
    'TurRht': (0, 0, 0),
    'VehLane': (0, 0, 0),
    'Wait2X': (0, 0, 0),
    'Xing': (0, 0, 0),
    'XingFmLft': (0, 0, 0),
    'XingFmRht': (0, 0, 0),
    'black': (0, 0, 0),
    'parking': (0, 0, 0),
    'rightParking': (0, 0, 0),
    'xing': (0, 0, 0),
}


def main(annofile):
    cap = cv2.VideoCapture(annofile[:-5])

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

    out_file = annofile[:-9] + '-out.mp4'
    out = cv2.VideoWriter(out_file, fourcc, 4, (width, height))

    with open(annofile, 'r') as f:
        db = json.load(f)

    frames = db['frames']

    for _ in range(3):
        cap.grab()

    for f in sorted(list(map(int, frames.keys())))[1:]:
        print(f)

        flag, frame = cap.retrieve()
        for _ in range(3):
            cap.grab()

        annots = frames[str(f)]
        for anno in annots:
            box = anno['box']
            tags = anno['tags']

            pt = [int(box['x1']), int(box['y1']), int(box['x2']), int(box['y2'])]
            cv2.rectangle(frame, (pt[0], pt[1]), (pt[2], pt[3]), COLOURS[tags[0]][::-1], 2)
            offset = -5
            for tag in tags:
                cv2.putText(frame, LABELS[tag], (int(pt[0]), int(pt[1]) + offset), FONT, 0.8, COLOURS[tag][::-1], 1, cv2.LINE_AA)
                offset -= 21
        out.write(frame)

        # out_image = '{:s}/{:05d}.png'.format(outdir, f)
        # cv2.imwrite(out_image, frame)

    cv2.destroyAllWindows()
    cap.release()
    out.release()


if __name__ == '__main__':
    annofiles = os.listdir('./')
    annofiles = [af for af in annofiles if af.endswith('.json')]
    for annofile in annofiles:
        print('\n\n\n\n\n annofile ', annofile)
        main(annofile)
