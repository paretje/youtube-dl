# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import js_to_json


class EenIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?een\.be/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _TEST = {
        'url': 'http://www.een.be/programmas/dagelijkse-kost/recepten/gemarineerde-makreel-met-guacamole-en-een-tomatensalade',
        'md5': 'efd556da2b7fd151566c72bfcfaee04a',
        'info_dict': {
            'id': 'embed_video_1127512',
            'display_id': 'gemarineerde-makreel-met-guacamole-en-een-tomatensalade',
            'ext': 'mp4',
            'title': 'Eén - Dagelijkse kost - Gemarineerde makreel met guacamole en een tomatensalade',
            'thumbnail': 'http://www.een.be/files/een.be/imagecache/video_image/images/programmas/dagelijkse_kost/2016_voorjaar/dako_160719_zomerkost_julius.png?',
            'duration': 1309.12,
        }
    }

    def _real_extract(self, url):
        display_id = self._match_id(url)

        webpage = self._download_webpage(url, display_id)

        data = self._parse_json(self._search_regex(
            r'(?s){var playerconfig = ({.+?});', webpage, 'player data'), display_id,
            transform_source=js_to_json)

        video_id = data['id']

        formats = self._extract_m3u8_formats(
            data['source']['hls'], display_id, entry_protocol='m3u8_native',
            ext='mp4')

        return {
            'id': video_id,
            'display_id': display_id,
            'title': self._og_search_title(webpage),
            'thumbnail': self._proto_relative_url(data.get('image')),
            'duration': float(data.get('duration')) / 1000000,
            'formats': formats
        }
