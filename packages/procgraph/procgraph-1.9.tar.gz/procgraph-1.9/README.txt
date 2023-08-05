ProcGraph ("processing graph") is a Python library for rapid prototyping 
of pipelines for logged and realtime data.

See documentation at:   http://andreacensi.github.com/procgraph/


Installation notes
------------------

The only painful part to install is mencoder and ffmpeg.


### Installation (OS-X)

(June 2015, OS X 10.10) Download from here:

	http://evermeet.cx/pub/ffmpeg/

### Installation (Ubuntu 12.04)
        
Need
 
 	sudo apt-get install x264 libavcodec-extra-53'

to install necessary codecs.

You can see a list of supported presets by using: 'x264 --help'.
        
Other packages that might be helpful: 

	libavdevice-extra-52  libavfilter-extra-0 libavformat-extra-52 libavutil-extra-49
	libpostproc-extra-51 libswscale-extra-0.
         
        
### Installation Ubuntu 14.04 - June 2015

Install mplayer and mencoder:

	sudo apt-get install mencoder mplayer 
	
For installing ffmpeg: (June 2015)

	sudo add-apt-repository ppa:mc3man/trusty-media
	sudo apt-get update
	sudo apt-get install ffmpeg gstreamer0.10-ffmpeg
	