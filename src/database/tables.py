import sqlalchemy as sa

metadata = sa.MetaData()

User = sa.Table(
    'user', metadata,
    sa.Column('id', sa.BIGINT, nullable=False, primary_key=True),
    sa.Column('uid', sa.BIGINT, nullable=False, unique=True),
    sa.Column('nickname', sa.Unicode(128), nullable=False),
    sa.Column('last_search', sa.DateTime, nullable=False),
    sa.Column('liked_tracks', sa.Integer, nullable=False),
    sa.Column('liked_artists', sa.Integer, nullable=False),
    sa.Column('liked_albums', sa.Integer, nullable=False)
)

Artist = sa.Table(
    'artist', metadata,
    sa.Column('id', sa.BIGINT(), nullable=False, primary_key=True),
    sa.Column('name', sa.Unicode(128), nullable=False, unique=True),
    sa.Column('image', sa.BLOB(), nullable=False),
    sa.Column('followers', sa.Integer(), nullable=False),
    sa.Column('popularity', sa.Integer(), nullable=False),
)


Album = sa.Table(
    'album', metadata,
    sa.Column('id', sa.BIGINT(), nullable=False, primary_key=True),
    sa.Column('name', sa.Unicode(length=256), nullable=False, unique=True),
    sa.Column('type', sa.String(32), nullable=False),
    sa.Column('release', sa.DateTime(), nullable=False),
    sa.Column('label', sa.String(128), nullable=False),
)


Track = sa.Table(
    'track', metadata,
    sa.Column('id', sa.BIGINT(), nullable=False, primary_key=True),
    sa.Column('name', sa.Unicode(length=128), nullable=False, unique=True),
    sa.Column('image', sa.BLOB(), nullable=False),
    sa.Column('duration', sa.TIMESTAMP(), nullable=False),
    sa.Column('explicit', sa.BOOLEAN(), nullable=False),
    sa.Column('album_id', sa.BIGINT(), sa.ForeignKey('album.id'), nullable=False),
)

Video = sa.Table(
    'video', metadata,
    sa.Column('id', sa.BIGINT(), nullable=False, primary_key=True),
    sa.Column('title', sa.Unicode(256), unique=True, nullable=False),
    sa.Column('url', sa.Unicode(256), unique=True, nullable=False),
    sa.Column('track_id', sa.BIGINT(), sa.ForeignKey('track.id'), nullable=False),
)

Genre = sa.Table(
    'genre', metadata,
    sa.Column('id', sa.BIGINT(), nullable=False, primary_key=True),
    sa.Column('name', sa.String(length=128), nullable=False, primary_key=True),
)


UserTrack = sa.Table(
    'user_track', metadata,
    sa.Column('user_id', sa.BIGINT(), sa.ForeignKey('user.id'), nullable=False),
    sa.Column('track_id', sa.BIGINT(), sa.ForeignKey('track.id'), nullable=False),
)


UserArtist = sa.Table(
    'user_artist', metadata,
    sa.Column('user_id', sa.BIGINT(), sa.ForeignKey('user.id'), nullable=False),
    sa.Column('artist_id', sa.BIGINT(), sa.ForeignKey('artist.id'), nullable=False),
)


UserAlbum = sa.Table(
    'user_album', metadata,
    sa.Column('user_id', sa.BIGINT(), sa.ForeignKey('user.id'), nullable=False),
    sa.Column('album_id', sa.BIGINT(), sa.ForeignKey('album.id'), nullable=False),
)


ArtistTrack = sa.Table(
    'artist_track', metadata,
    sa.Column('artist_id', sa.BIGINT(), sa.ForeignKey('artist.id'), nullable=False),
    sa.Column('track_id', sa.BIGINT(), sa.ForeignKey('track.id'), nullable=False),
)


ArtistAlbum = sa.Table(
    'artist_album', metadata,
    sa.Column('artist_id', sa.BIGINT(), sa.ForeignKey('artist.id'), nullable=False),
    sa.Column('album_id', sa.BIGINT(), sa.ForeignKey('album.id'), nullable=False),
)


GenreArtist = sa.Table(
    'genre_artist', metadata,
    sa.Column('genre_id', sa.BIGINT(), sa.ForeignKey('genre.id'), nullable=False),
    sa.Column('artist_id', sa.BIGINT(), sa.ForeignKey('artist.id'), nullable=False),
)


GenreAlbum = sa.Table(
    'genre_album', metadata,
    sa.Column('genre_id', sa.BIGINT(), sa.ForeignKey('genre.id'), nullable=False),
    sa.Column('album_id', sa.BIGINT(), sa.ForeignKey('album.id'), nullable=False),
)