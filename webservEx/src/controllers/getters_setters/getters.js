const { set } = require(process.env.SETTERS)

class GetRequestResponse {

    requestREST(request) {
        try {
            let [name, table, column] = set.url(request.originalUrl)
            set.model({ name, table })
            if (request.query && column) {
                set.filter({ name, column })
                set.query(request.query)
                if (request.query.page) { set.page(request.query.page) } else { set.count() }
            }
            return set.finally()
        } catch (err) { console.log(err) }
    }

    requestGraphQL(request) { try { return new GetRequestGraphQL(request).who() } catch (err) { console.log(err) } }

    responseREST(response, content) {
        try {
            this.status = parseInt(process.env[Object.keys(content).toString().toUpperCase()])
            return response.status(this.status ? this.status : 200).json(content)
        } catch (err) { console.log(err) }
    }
}


class GetRequestGraphQL {

    constructor(request) {
        this.request = request
        this.resolver = this.request.query || this.request.about.query
    }

    who() {
        try {
            switch (this.resolver) {
                case 'book':
                    set.model('M_BOOKS')
                    set.filter(this.request.name.length > 3 ? this.request : 'abbrev')
                    set.param(this.request)
                    set.fields(this.request.about.context)
                    break
                case 'nvi':
                    set.model('M_NVI_VERSION')
                    // set.filter(this.request)
                    // set.param(this.request)
                    // set.page(this.request.pagina)
                    set.lookup(['book', 'chapter', 'verse'])
                    break
                case 'genre': /// <-- com 'argumentos' e 'paginação'
                    set.model('M_GENRES')
                    set.filter(this.request)
                    set.param(this.request)
                    set.page(this.request.page)
                    set.fields(this.request.about.context)
                    break
                case 'artist': /// <-- com 'argumentos' e 'paginação'
                    set.model('M_ARTISTS')
                    set.filter(this.request)
                    set.param(this.request)
                    set.page(this.request.page)
                    set.fields(this.request.about.context)
                    break
                case 'track': /// <-- com 'argumentos' e 'paginação'
                    set.model('M_TRACKS')
                    set.filter(this.request)
                    set.param(this.request)
                    set.page(this.request.pagina)
                    set.lookup(['artist', 'genres'])
                    break
            }
            return set.finally()
        } catch (err) { console.log(err) }
    }
}

const get = new GetRequestResponse()

module.exports = { get }