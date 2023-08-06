Request a converted to mp3 youtube video from youtube-mp3.org.

Depends on: python 2.7.x, requests, docopt


Usage: 

youtube-mp3.py [--autoend] [--chunk=<bytes>] <url> <path>

Examples:

  youtube-mp3.py --autoend https://www.youtube.com/watch?v=YE7VzlLtp-4 ./bunny.mp3

Options:

  -h, --help
  --autoend    auto append ".mp3" to the file if not present.
  --chunk=<bytes>  buffer size when writing to file [default: 2048].


