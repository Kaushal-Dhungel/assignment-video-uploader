import subprocess

def get_duration(filename):

    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

def validate_video(size,video_format,duration):
    error_messages = []

    if size > 1024:
        error_messages.append("Video size should not exceed 1 GB.")
    if video_format not in ['mp4','mkv']:
        error_messages.append(f"Files with {video_format} format not supported. Only MP4 or MKV video format supported.")
    if duration > 600:
        error_messages.append('Video length should be less than 10 minutes.')

    return error_messages



# def get_duration_moviepy(filename):
#     from moviepy.editor import VideoFileClip
#     clip = VideoFileClip(filename)
#     duration       = clip.duration
#     return duration

# def get_duration(filename):
#     from subprocess import  check_output, CalledProcessError, STDOUT
#     command = [
#         'ffprobe', 
#         '-v', 
#         'error', 
#         '-show_entries', 
#         'format=duration', 
#         '-of', 
#         'default=noprint_wrappers=1:nokey=1', 
#         filename
#       ]
#     try:
#         output = check_output( command, stderr=STDOUT ).decode()
#     except CalledProcessError as e:
#         output = e.output.decode()

#     return output