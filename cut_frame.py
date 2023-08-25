import cv2
import os
import sys


if __name__ == '__main__':
    # Open the video file
    # video_path = 'F:/work/0412_video_cut/2_cut/2_6.mp4'
    video_path = sys.argv[1]
    frame_save_path = sys.argv[2]
    video_base_name = os.path.basename(video_path)
    video = cv2.VideoCapture(video_path)

    # Create a directory to store the frames
    # save_path = os.path.dirname(video_path)
    # save_folder_name = os.path.splitext(video_base_name)[0]
    # save_location = save_path + '/' + save_folder_name + '/'
    # os.makedirs(save_location, exist_ok=True)
    # os.makedirs('frame', exist_ok=True)

    # Initialize variables
    frame_count = 0
    success = True

    # Loop through the video and extract frames
    while success:
        # Read a frame from the video
        success, image = video.read()

        # Save the frame as an image
        if success:
            frame_count += 1
            # cv2.imwrite(save_location + str(frame_count) + '.jpg', image)
            # cv2.imwrite('F:/work/0421_video_cut_frame/2_cut/2_6_frame/'+str(frame_count)+'.jpg', image)
            if frame_count % 4 == 0:
                cv2.imwrite(frame_save_path + "/" +
                            str(frame_count) + '.jpg', image)
        else:
            print('Finish')
            # print(type(save_location))
            # print(type(save_location + str(frame_count) + '.jpg'))

    # Release the video file
    video.release()
