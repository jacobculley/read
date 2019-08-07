import json, pdb
import cv2, os
base_dir = './'

FONT = cv2.FONT_HERSHEY_SIMPLEX


imagedir = 'images'
outdir = 'plottedimages'

if not os.path.isdir(imagedir):
    os.makedirs(imagedir)

if not os.path.isdir(outdir):
    os.makedirs(outdir)

def main(annofile):

    base_name = annofile[:10]
    video_plot_dir = outdir + '/' + base_name
    vidfile = base_name[:-4]
    
    if not os.path.isdir(video_plot_dir):
        os.makedirs(video_plot_dir)
    
    video_handle = cv2.VideoCapture(vidfile)
    # video_writter_object =  cv2.VideoWriter()

    with open(annofile,'r') as f:
        db = json.load(f)

    # pdb.set_trace()
    color = (0,0,255)
    color1 = (255,0,5)

    frames = db['frames']

    for f in sorted(frames.keys()):
        print(f)
        in_id = int(f)
        # input_image_path = '{:s}/{:05d}.png'.format(imagedir, 3*(in_id-1)+1)
        # import cv2

        color = (0, 0, 255)
        color1 = (255, 0, 5)

        flag, frame = video_handle.retrive()
        
        for i in range(3):
            _, _ = video_handle.retrive()

        annots = frames[f]
        for anno in annots:
            width = anno['width']
            height = anno['height']
            box = anno['box']
            tags = anno['tags']

            pt = [int(box['x1']), int(box['y1']),int(box['x2']),int(box['y2'])]
            cv2.rectangle(frame, (pt[0], pt[1]), (pt[2], pt[3]), color, 2)
            offset = 0
            for tag in tags:
                cv2.putText(frame, tag, (int(pt[0]) , int(pt[1]) + offset), FONT, 1, color, 1, cv2.LINE_AA)
                offset += 21
        out_image = '{:s}/{:05d}.png'.format(outdir, in_id)
        cv2.imwrite(out_image,frame)


if __name__ == '__main__':
    annofiles = os.listdir(base_dir)
    annofiles = [af for af in annofiles if af.endswith('.json')]
    for annofile in annofiles:
            print('\n\n\n\n\n annofile ', annofile, '\n\n\n\n\n\n')
            main(annofile)

