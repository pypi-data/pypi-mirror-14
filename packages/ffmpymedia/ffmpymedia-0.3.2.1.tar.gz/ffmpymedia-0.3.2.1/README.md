# FFMPYMEDIA

FFMPYMEDIA is a wrapper library around FFMPEG.
It interfaces with ffmpeg through the shell and interprets the program stdout/stderr to generate it's internal structures.
The following functionality is planned or implemented.

## Media Analysis

It interprets the output of the ffprobe utility and generates it's internal data structures with it.
The MediaAnalyser API exposes the **MediaAnalyser.media_file_difference()** method which returns the difference in media streams layout between a Template and a real file.
It also exposes the **MediaAnalyser.validate_media_file()** which determines if a mediaFile has the same layout as a Template or another media file.

## Future Functionality

It is planned to implement wrappers around the ffmpeg utility for media transcoding and streaming and around ffserver for media stream serving and aggregation.
