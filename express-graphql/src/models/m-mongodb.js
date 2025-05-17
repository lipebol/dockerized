const { mongoose, mongooseBible, mongooseSpotifEx } = require(process.env.INSTANCE_MONGODB_PATH)


/// Collection MongoDB in bible: 'books'
const M_BOOKS = mongooseBible.model(
    "M_BOOKS", new mongoose.Schema(
        {
            id: { type: mongoose.ObjectId, required: true },
            name: { type: String, required: true },
            abbrev: { type: String, required: true },
            location: { type: String, required: true },
            position: { type: Number, required: true },
            location_position: { type: Number, required: true }
        }
    ),
    "books"
)


/// Collection MongoDB in bible: 'numbers'
const M_NUMBERS = mongooseBible.model(
    "M_NUMBERS", new mongoose.Schema(
        {
            id: { type: mongoose.ObjectId, required: true },
            number: { type: Number, required: true }
        }
    ),
    "numbers"
)


/// Collection MongoDB in bible: 'nvi'
const M_NVI_VERSION = mongooseBible.model(
    "M_NVI_VERSION", new mongoose.Schema(
        {
            id: { type: mongoose.ObjectId, required: true },
            book: { type: mongoose.ObjectId, ref: "M_BOOKS" },
            chapter: { type: mongoose.ObjectId, ref: "M_NUMBERS" },
            verse: { type: mongoose.ObjectId, ref: "M_NUMBERS" },
            text: { type: String, required: true }
        }
    ),
    "nvi"
)


/// Collection MongoDB in spotifEx: 'genre'
const M_GENRES = mongooseSpotifEx.model(
    "M_GENRES", new mongoose.Schema(
        {
            id: { type: mongoose.ObjectId, required: true },
            name: { type: String, required: true },
            url: { type: String, required: true }
        }
    ),
    "genres"
)


/// Collection MongoDB in spotifEx: 'artist'
const M_ARTISTS = mongooseSpotifEx.model(
    "M_ARTISTS", new mongoose.Schema(
        {
            id: { type: mongoose.ObjectId, required: true },
            name: { type: String, required: true },
            profile: { type: String, required: true }
        }
    ),
    "artists"
)


/// Collection MongoDB in spotifEx: 'track'
const M_TRACKS = mongooseSpotifEx.model(
    "M_TRACKS", new mongoose.Schema(
        {
            id: { type: mongoose.ObjectId, required: true },
            trackid: { type: String, required: true },
            length: { type: Number, required: true },
            artUrl: { type: String, required: true },
            album: { type: String, required: true },
            artist: { type: mongoose.ObjectId, ref: "M_ARTISTS" },
            autoRating: { type: Number, required: true },
            discNumber: { type: String, required: true },
            name: { type: String, required: true },
            trackNumber: { type: Number, required: true },
            url: { type: String, required: true },
            genres: [{ type: mongoose.ObjectId, ref: "M_GENRES" }]
        }
    ),
    "tracks"
)


/// Collection MongoDB in spotifEx: 'playlist'
const M_PLAYLISTS = mongooseSpotifEx.model(
    "M_PLAYLISTS", new mongoose.Schema(
        {
            id: { type: mongoose.ObjectId, required: true },
            day: { type: Number, required: true },
            month: { type: Number, required: true },
            year: { type: Number, required: true },
            playlist: [{ type: mongoose.ObjectId, ref: "M_TRACKS" }]
        }
    ),
    "playlists"
)


module.exports = { M_BOOKS, M_NVI_VERSION, M_GENRES, M_ARTISTS, M_TRACKS, M_PLAYLISTS }