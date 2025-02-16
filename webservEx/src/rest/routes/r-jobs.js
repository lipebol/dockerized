const router = require(process.env.EXPRESS).Router()
const { c_ } = require(process.env.CONTROLLER_PATH)



/// 'jobs.website'
router.get(process.env.JOBS_WEBSITE_ENDPOINT, c_.noParams)

/// 'jobs.search'
router.get(process.env.JOBS_KEYWORD_ENDPOINT, c_.noParams)


module.exports = router