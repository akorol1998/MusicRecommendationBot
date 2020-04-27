import argparse
import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.config import YouTubeUtils


class YouTubeAPI:
    youtube_api_logger = logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
    youtube = build(
        YouTubeUtils.YOUTUBE_API_SERVICE_NAME,
        YouTubeUtils.YOUTUBE_API_VERSION,
        developerKey=YouTubeUtils.YOUTUBE_DEVELOPER_KEY
        )

    @staticmethod
    def youtube_search_requests(tracks, artists) -> str:
        for track, artist in zip(tracks, artists):
            q_track = track['name']
            q_artist = artist['name']
            yield {
				'link':f"{q_track} {q_artist} - http://localhost",
				'track_uid': track['id']
				}

            # search_response = YouTubeAPI.youtube_search(q_track=q_track, q_artist=q_artist)

            # for idx, search_result in enumerate(search_response['items']):
            #     if search_result['id']['kind'] == 'youtube#video':
            #         video_id = search_result['id']['videoId']
            #         yield YouTubeUtils.VIDEO_BASE_URL + video_id

    @staticmethod
    def youtube_search(*args, **kwargs) -> dict:
        search_response = YouTubeAPI.youtube.search().list(
            q=f'{kwargs["q_artist"]} {kwargs["q_track"]}',
            part=f'{YouTubeUtils.PART_ID},{YouTubeUtils.PART_SNIPPET}',
            maxResults=YouTubeUtils.MAX_RESULTS,
        ).execute()
        return search_response
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default='Google')
    parser.add_argument('--max-results', help='Max results', default=25)
    args = parser.parse_args()

    try:
        YouTubeAPI.youtube_search(args)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))