Request a converted to mp3 youtube video from youtube-mp3.org.

Depends on: python 2.7.x/3.4, requests, docopt


Usage: 

youtube-mp3.py [--autoend] [--chunk=<bytes>] <url> <path>

Examples:

  youtube-mp3.py --autoend https://www.youtube.com/watch?v=YE7VzlLtp-4 ./bunny.mp3

Options:

  -h, --help
  --autoend    auto append ".mp3" to the file if not present.
  --chunk=<bytes>  buffer size when writing to file [default: 2048].


NOTE:

There are limitations to using the service. You cannot download video longer than 20 minutes.
Also, the video could be marked to be not downloadable. 

