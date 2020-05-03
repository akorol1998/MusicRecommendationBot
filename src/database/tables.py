import sqlalchemy as sa

metadata = sa.MetaData()

User = sa.Table(
    'user', metadata,
    sa.Column('id', sa.BIGINT(), nullable=False, primary_key=True),
    sa.Column('uid', sa.BIGINT(), nullable=False, unique=True),
    sa.Column('username', sa.Unicode(128), nullable=False),
    sa.Column('last_search', sa.DateTime, nullable=False),
    sa.Column('liked_tracks', sa.Integer, nullable=False),
    sa.Column('liked_artists', sa.Integer, nullable=False),
    sa.Column('liked_albums', sa.Integer, nullable=False)
)

Artist = sa.Table(
    'artist', metadata,
    sa.Column('id', sa.BIGINT(), nullable=False, primary_key=True),
    sa.Column('uid', sa.Unicode(128), nullable=False, unique=True),
    sa.Column('name', sa.Unicode(128), nullable=False, index=True),
    sa.Column('followers', sa.Integer(), nullable=False),
    sa.Column('popularity', sa.Integer(), nullable=False),
)


Album = sa.Table(
    'album', metadata,
    sa.Column('id', sa.BIGINT(), nullable=False, primary_key=True),
    sa.Column('uid', sa.Unicode(128), nullable=False, unique=True),
    sa.Column('name', sa.Unicode(length=256), nullable=False),
    sa.Column('type', sa.String(32), nullable=False),
    sa.Column('release', sa.DateTime(), nullable=False),
    sa.Column('label', sa.String(128), nullable=False),
    sa.UniqueConstraint('name', 'release', name='uix_name_release')
)


Track = sa.Table(
    'track', metadata,
    sa.Column('id', sa.BIGINT(), nullable=False, primary_key=True),
    sa.Column('uid', sa.Unicode(128), nullable=False, unique=True),
    sa.Column('name', sa.Unicode(length=128), nullable=False, index=True),
    sa.Column('duration', sa.BIGINT(), nullable=False),
    sa.Column('explicit', sa.BOOLEAN(), nullable=False),
    sa.Column('album_id', sa.BIGINT(), sa.ForeignKey('album.id'), nullable=False),
    sa.UniqueConstraint('name', 'album_id', name='uix_name_album_id')
)

Video = sa.Table(
    'video', metadata,
    sa.Column('id', sa.BIGINT(), nullable=False, primary_key=True),
    sa.Column('title', sa.Unicode(256), nullable=False),
    sa.Column('url', sa.Unicode(256), unique=True, nullable=False),
    sa.Column('track_id', sa.BIGINT(), sa.ForeignKey('track.id'), nullable=False),
)


UserTrack = sa.Table(
    'user_track', metadata,
    sa.Column('user_id', sa.BIGINT(), sa.ForeignKey('user.id'), nullable=False),
    sa.Column('track_id', sa.BIGINT(), sa.ForeignKey('track.id'), nullable=False),
    sa.UniqueConstraint('user_id', 'track_id', name='uix_user_track')
)


UserArtist = sa.Table(
    'user_artist', metadata,
    sa.Column('user_id', sa.BIGINT(), sa.ForeignKey('user.id'), nullable=False),
    sa.Column('artist_id', sa.BIGINT(), sa.ForeignKey('artist.id'), nullable=False),
    sa.UniqueConstraint('user_id', 'artist_id', name='uix_user_artist')
)


UserAlbum = sa.Table(
    'user_album', metadata,
    sa.Column('user_id', sa.BIGINT(), sa.ForeignKey('user.id'), nullable=False),
    sa.Column('album_id', sa.BIGINT(), sa.ForeignKey('album.id'), nullable=False),
    sa.UniqueConstraint('user_id', 'album_id', name='uix_user_album_1')
)


ArtistTrack = sa.Table(
    'artist_track', metadata,
    sa.Column('artist_id', sa.BIGINT(), sa.ForeignKey('artist.id'), nullable=False),
    sa.Column('track_id', sa.BIGINT(), sa.ForeignKey('track.id'), nullable=False),
    sa.UniqueConstraint('artist_id', 'track_id', name='uix_artist_track')
)



ArtistAlbum = sa.Table(
    'artist_album', metadata,
    sa.Column('artist_id', sa.BIGINT(), sa.ForeignKey('artist.id'), nullable=False),
    sa.Column('album_id', sa.BIGINT(), sa.ForeignKey('album.id'), nullable=False),
    sa.UniqueConstraint('artist_id', 'album_id', name='uix_artist_album')
)

