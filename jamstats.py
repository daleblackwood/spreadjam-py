import argparse
import ffmpeg
import os
import datetime
import csv


VIDEO_EXTS = ['.mkv', '.mp4']


class VidStats:
    def __init__(self, name, size, length, date):
        self.name = name
        self.size = size
        self.length = length
        self.date = date


def get_video_files(folder): 
    filepaths = []
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if not os.path.isfile(filepath):
            continue
        name, ext = os.path.splitext(filename)
        if ext not in VIDEO_EXTS:
            continue
        filepaths.append(filepath)
    return filepaths


def get_stats(folder, prev_stats = None):
    result = []
    video_files = get_video_files(folder)
    for video_file in video_files:
        name = os.path.basename(video_file)
        size = os.path.getsize(video_file)
        date = os.path.getmtime(video_file)
        if prev_stats:
            found = None
            for item in prev_stats:
                if item.name == name and item.date == date and item.size == size:
                    found = item
                    break
            if found:
                result.append(found)
                continue    
        print("ffmpeg probing %s..." % video_file)
        info = ffmpeg.probe(video_file)
        if "format" in info and "duration" in info["format"]: 
            length = float(info["format"]["duration"])
            result.append(VidStats(name, size, length, date))
    result.sort(key=lambda x: x.date)
    return result


def get_totals(stats):
    count = 0
    size = 0
    length = 0
    for stat in stats:
        count += 1
        size += stat.size
        length += stat.length
    return count, size, length


def csv_stats(stats):
    with open('stats.csv', mode='w') as employee_file:
        writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        total_size = 0
        total_length = 0
        for stat in stats:
            total_size += stat.size
            total_length += stat.length
            writer.writerow([
                stat.name, 
                format_size(stat.size),
                format_size(total_size),
                format_length(stat.length),
                format_length(total_length)
            ])


def format_size(size):
    return "%dmb" % (round(size / 1024 / 1024 * 100) / 100)


def format_length(length):
    return str(datetime.timedelta(seconds=round(length)))


def main(folder):
    stats = get_stats(folder)
    count, size, length = get_totals(stats)
    size_str = format_size(size)
    length_str = format_length(length)
    print("%d videos are %s, %s in length" % (count, size_str, length_str))
    csv_stats(stats)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Jam Stats')
    parser.add_argument('folder', help='the folder containing your video files')
    args = parser.parse_args()
    main(args.folder)