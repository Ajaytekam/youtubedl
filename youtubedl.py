#!/usr/bin/python3
#
# github.com/ajaytekam
# use pytube library 
#
import pytube
import subprocess
import os 
import sys
import argparse
import re

def Download(url, qty_ch, type):
    try: 
        print("[+] Searching Video...")
        tg_file = pytube.YouTube(url)
        print("[+] Video Found.")
        print("[+] Title: {}".format(tg_file.title))
        if type == "video":
            qty_vid = tg_file.streams.filter(adaptive=True)
            qty_n = 0 
            for i in range(0, len(qty_vid)):
                searchQ = str(qty_vid[i])
                if re.search("video", searchQ) and re.search("mp4", searchQ):
                    if re.search("1080", searchQ) and (qty_ch==0 or qty_ch==1080):
                        qty_n = i
                        print("[+] Downloading video in 1080p...")
                        break
                    if re.search("720", searchQ) and (qty_ch==0 or qty_ch==720):
                        qty_n = i
                        print("[+] Downloading video in 720p...")
                        break
                    if re.search("360", searchQ) and (qty_ch==0 or qty_ch==360):
                        qty_n = i
                        print("[+] Downloading video in 360p...")
                        break
                    if re.search("240", searchQ) and (qty_ch==0 or qty_ch==240):
                        qty_n = i
                        print("[+] Downloading video in 240p...")
                        break
                    if re.search("144", searchQ) and (qty_ch==0 or qty_ch==144):
                        qty_n = i
                        print("[+] Downloading video in 144p...")
                        break
            name=qty_vid[qty_n].download()
            print("[+] Video Downlaoded Successfully.")
            print("File: {}".format(name))
        else:
            print("[+] Downloading file...wait...")
            video_name = re.sub(" ", "_", tg_file.title)+".mp3"
            dl_name = tg_file.streams.filter(only_audio=True).first().download()
            print("[+] Audio file downlaod successfully...")
    except pytube.exceptions.AgeRestrictedError: 
        print("[!] Video is age restricted, and cannot be accessed without OAuth!!")
        sys.exit(1)
    except pytube.exceptions.ExtractError: 
        print("[!] Data extraction based exception!!")
        sys.exit(1)
    except pytube.exceptions.HTMLParseError: 
        print("[!] HTML could not be parsed!!")
        sys.exit(1)
    except pytube.exceptions.LiveStreamError: 
        print("[!] Video is a live stream!!")
        sys.exit(1)
    except pytube.exceptions.MaxRetriesExceeded: 
        print("[!] Maximum number of retries exceeded!!")
        sys.exit(1)
    except pytube.exceptions.MembersOnly: 
        print("[!] Video is members-only!!")
        sys.exit(1)
    except pytube.exceptions.PytubeError: 
        print("[!] pytube library error!!")
        sys.exit(1)
    except pytube.exceptions.RecordingUnavailable: 
        print("[!] Video Recording is not available!!")
        sys.exit(1)
    except pytube.exceptions.RegexMatchError: 
        print("[!] Regex pattern did not return any matches!!")
        sys.exit(1)
    except pytube.exceptions.VideoPrivate: 
        print("[!] Video is private!!")
        sys.exit(1)
    except pytube.exceptions.VideoRegionBlocked: 
        print("[!] Video region is blocked!!")
        sys.exit(1)
    except pytube.exceptions.VideoUnavailable: 
        print("[!] Video is not available!!")
        sys.exit(1)
    if type == "mp3":
        print("[+] Converting into mp3 file...wait...")
        COMMAND = 'ffmpeg -y -i "{}" "{}"'.format(dl_name, video_name)
        subprocess.run(COMMAND, shell=True, check=True, text=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        os.remove(dl_name) 
    return    
 
def main():
    parser = argparse.ArgumentParser()     
    parser.add_argument("-u", "--url", type=str, help="Youtube video url", default="")
    parser.add_argument("-q", "--quality", type=int, help="Video Quality [1080|720|360|240|144] Default:1080", default=0)
    parser.add_argument("-a", "--audio", help="Convert to mp3", action="store_true")
    args = parser.parse_args()
    if args.url == "":
        parser.print_help()
        sys.exit(0)
    if args.audio:
        # check if ffmpeg library is installed or not
        res = subprocess.run('which ffmpeg', shell=True, capture_output=True, text=True)
        if res.stdout == "":
            print("[!] ffmpeg binary not installed.")
            print("[!] Install it first...")
            sys.exit(1)
        type = "mp3"
    else:
        type = "video"
    Download(args.url, args.quality, type)
    sys.exit(0)

if __name__ == "__main__":
    main()
