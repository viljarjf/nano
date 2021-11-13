# Video processing

## Setup

install imagej version 1. I have ImageJ 1.53k, for java 1.8.0_172 64bit.

Install the Mosaic suite for imagej 1, found [here](https://sbalzarini-lab.org/?q=downloads/imageJ)
under the "Can MosaicSuite work  with old ImageJ1 (...)" section.

The script for this experiment is `system_1.py`

## Capturing videos

Do this at the lab, save as `.avi`. Other formats might work, but this is the only one I have tried 

## Tracking

- Open a video as grayscale by dragging the file into imagej and checking the grayscale box.
- Go to plugins->Mosaic->Particle tracker 2D/3D
- These are not 3D data
- The default settings in the particle tracker menu worked great for me: radius 3, cutoff 3, per/abs 0.1, link range 2, displacement 10, dynamics browninan.
- Press ok
- The imageJ window (not the one with the video, just the regular one) will now show the progress for each frame. 
Your computer can easily handle a 200 frame HD video in a couple minutes at most.
- In the results window that eventually pop up, hit "save full report".
- move the txt file you just created to this folder, and run the script once you have all the files.
- Depending on the file name ect, you might want to change the input to the `readfile` function.

## Particle size

- open a video, choose grayscale
- go to image->adjust->threshold
- choose over/under instead of red (not sure if this is strictly necessary)
- the upper bound should be max (255)
- the lower bound should be to the right of the peak. Adjust to show more or less of the edge of the particles
- Without closing the window, go back to the main imagej window
- go to analyze->analyze particles
- 0-infinity for size, and 0-1 for circularity worked fine for me. 
- check "Display results", and hit OK
- you can process all images if you want. I did.
- once the processing is done (takes like 1 second), go to file->save as in the results window
- save the csv
- move the csv to this folder, and run the script. 
- Depending on the file name ect, you might want to change the input to the `get_r` function.