import subprocess
import os

def perform_magic(input_file,output_file):

    if not os.path.exists(input_file):
        print(f"File does not exist at '{input_file}'")

    result = subprocess.run([
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        input_file
    ], capture_output=True, text=True)

    print("Return code:", result.returncode)
    print("stdout:", repr(result.stdout))
    print("stderr:", repr(result.stderr))

    duration = float(result.stdout.strip())
    step = 2

    i = 0
    start = 0
    all_list = []
    approx_total = int(duration//2 + 1)

    while start < duration:
        end = start + step
        output = f"part_{i+1}.mp4"
        all_list.append(output)

        if (i+1)%2 == 0:
            subprocess.run([
            "ffmpeg",
            "-y",
            "-i", input_file,
            "-ss", str(start),
            "-to", str(end),
            "-vf", "scale=2*iw:2*ih,crop=iw/2:ih/2:(iw-iw/2)/2:(ih-ih/2)/2",
            "-r", "30",
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "fast",
            "-c:a", "aac",
            output
        ], check=True)
        else:
            subprocess.run([
            "ffmpeg",
            "-y",
            "-i", input_file,
            "-ss", str(start),
            "-to", str(end),
            "-r", "30",
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "fast",
            "-c:a", "aac",
            output
        ], check=True)

        start += step
        i += 1

        print(f"Done : {i}/{approx_total}")

    with open("file.txt","w") as f:
        f.writelines([f"file {file}\n" for file in all_list])

    if(os.path.exists(output_file)):
        os.remove(output_file)

    subprocess.run([
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", "file.txt",
        "-c", "copy",
        output_file
    ], check=True)

    all_list = list(set(all_list))
    for file in all_list:
        os.remove(file)
    os.remove("file.txt")

perform_magic("video.mp4","video-e.mp4")