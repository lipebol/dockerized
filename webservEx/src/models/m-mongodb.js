const { mongoose, mongooseBible, mongooseSpotifEx } = require(process.env.INSTANCE_MONGODB)


/// Collection MongoDB in spotifEx: 'genre'
const M_GENRE = mongooseSpotifEx.model(
    "M_GENRE", new mongoose.Schema(
        {
            id: { type: Number, required: true },
            name: { type: String, required: true },
            url: { type: String, required: true }
        }
    ),
    "genre"
)


/// Collection MongoDB in spotifEx: 'artist'
const M_ARTIST = mongooseSpotifEx.model(
    "M_ARTIST", new mongoose.Schema(
        {
            id: { type: Number, required: true },
            name: { type: String, required: true },
            profile: { type: String, required: true }
        }
    ),
    "artist"
)


/// Collection MongoDB in spotifEx: 'track'
const M_TRACK = mongooseSpotifEx.model(
    "M_TRACK", new mongoose.Schema(
        {
            id: { type: Number, required: true },
            trackid: { type: String, required: true },
            length: { type: Number, required: true },
            artUrl: { type: String, required: true },
            album: { type: String, required: true },
            artist: { type: mongoose.ObjectId, ref: "M_ARTIST" },
            autoRating: { type: Number, required: true },
            discNumber: { type: String, required: true },
            name: { type: String, required: true },
            trackNumber: { type: Number, required: true },
            url: { type: String, required: true },
            genres: [{ type: mongoose.ObjectId, ref: "M_GENRE" }]
        }
    ),
    "track"
)


/// Collection MongoDB in spotifEx: 'playlist'
const M_PLAYLIST = mongooseSpotifEx.model(
    "M_PLAYLIST", new mongoose.Schema(
        {
            id: { type: Number, required: true },
            day: { type: Number, required: true },
            month: { type: Number, required: true },
            year: { type: Number, required: true },
            playlist: [{ type: mongoose.ObjectId, ref: "M_TRACK" }]
        }
    ),
    "playlist"
)


module.exports = { M_GENRE, M_ARTIST, M_TRACK, M_PLAYLIST }