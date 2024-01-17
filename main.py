import os
import sys
import argparse
from tqdm import tqdm

from urllib.parse import urlparse, parse_qs

import googleapiclient.discovery

from google_auth_oauthlib.flow import InstalledAppFlow


CLIENT_SECRETS_FILE = 'client_secret.json'

SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_local_server()
  return googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials = credentials)


def add_video(youtube, playlist_id, video_id): 
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
          "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
              "kind": "youtube#video",
              "videoId": video_id
            }
          }
        }
    )
    response = request.execute()
    return response


def extract_id(link):
    qs = parse_qs(urlparse(link).query)
    return qs['v'][0]


def parse_args():
    parser = argparse.ArgumentParser(description="read youtube links from stdin and insert them into playlist")
    parser.add_argument("title", type=str, help="title of new playlist to make")
    parser.add_argument("-d", "--description", type=str, default="", help="description of playlist")
    parser.add_argument("-t", "--tags", type=str, nargs="*")
    parser.add_argument("-p", "--privacy", help="privacy status of playlist", type=str, default="private", choices=["public", "unlisted", "private"])
    parser.add_argument("-ns", "--no-skip", help="do not skip links which can't be inserted", action="store_false")

    return parser.parse_args()


def main():
    args = parse_args()
    links = [extract_id(link.strip()) for link in sys.stdin.readlines()]
    
    youtube = get_authenticated_service()

    playlist_response = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": args.title,
                    "description": args.description,
                    "tags": args.description,
                },
                "status": {
                    "privacyStatus": args.privacy
                }
            }).execute()
    playlist_id = playlist_response['id']

    for video_id in tqdm(links):
        try:
            add_video(youtube, playlist_id, video_id)

        except Exception as e:
            if args.no_skip: raise
            print(f"skipping {video_id} due to exception {e}")


if __name__ == "__main__":
    main()
