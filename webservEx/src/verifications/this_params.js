const dayjs = require(process.env.DAYJS).extend(require(process.env.EXTEND_DAYJS))

class ThisParams {

    constructor() { this.validator = JSON.parse(process.env.ARRAY_EMPTY) }

    isDates(request) {
        try {
            this.params = request.params.dates.split(process.env.SEPARATOR)
            if (this.params[0] === process.env.MAX) { request.params.dates = this.params[0] }
            else {
                this.params.forEach(
                    (value) => {
                        let resDayJs = dayjs(value, process.env.FORMAT_1, true) /// <-- 'true', não passa para o próximo mês
                        if (String(resDayJs.$d) === process.env.INVALID) {
                            if (String(resDayJs.$y) === String(resDayJs.$M)) {
                                this.validator.push('INVALID_FORMAT')
                            } else { this.validator.push('INVALID_DATE') }
                        } else { this.validator.push(true) }
                    }
                )
                this.validator = this.validator.filter((i) => i !== true)
                if (this.validator.length === 0) {
                    if (dayjs(this.params[0]).isAfter(dayjs(this.params[1]))) { return 'END_DATE' }
                } else { return this.validator[0] }
            }
            return request
        } catch (err) { console.log(err) }
    }


    async isMulti(request) {
        try {
            this.params = request.params.multi.split(process.env.SEPARATOR)
            switch (request.filter) {
                case 'nome_query':
                    this.querys = await this.fetchQL(`${process.env.REQUEST_INFO}`)
                    if (this.querys) {
                        this.querys = Array.from(this.querys.data._info).map(value => value.nome_query)
                        this.params.forEach(
                            (value) => {
                                this.querys.includes(value) ?
                                    this.validator.push(value) : this.validator.push(false)
                            }
                        )
                    }
                    break
                case 'referencia':
                    this.params.forEach((value) => {
                        String(dayjs(value, process.env.FORMAT_2, true).$d) === process.env.INVALID ? /// <-- 'true', não passa para o próximo mês
                            this.validator.push(false) : this.validator.push(value)
                    })
                    break
                default:
                    this.validator = request.filter === 'name' || 'abbrev' ?
                        this.fetchBadChar(this.params) : false
            }

            if (this.validator.includes(false)) { return 'INVALID_FIELD' }
            request.params.multi = this.validator
            return request
        } catch (err) { console.log(err) }
    }


    fetchBadChar(params) {
        return params.map(
            (name) => {
                return process.env.BAD_CHARACTERS.split(process.env.PIPE).map(
                    character => name.includes(character) ? true : false
                ).filter(character => character !== false).length === 0 ? name : false
            }
        )
    }

    async fetchQL(query) {
        try {
            return await fetch(
                process.env.GRAPHQL_URL,
                {
                    method: process.env.METHOD_POST,
                    headers: JSON.parse(process.env.CONTENT_TYPE_JSON),
                    body: JSON.stringify({ query })
                }
            ).then((response) => { if (response.status === 200) { return response.json() } })
        } catch (err) {
            console.log(err)
            return false
        }
    }
}

module.exports = { ThisParams }