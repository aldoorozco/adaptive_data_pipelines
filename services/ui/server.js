const fastify = require('fastify')({ logger: true })
const path = require('path')
var infraSetup = false

fastify.register(require('fastify-static'), {
  root: path.join(__dirname, 'resources'),
  prefix: '/resources/',
})

/* Dispatch web page */
fastify.get('/', function (req, reply) {
  reply.sendFile('index.html')
})

var request = require('urllib-sync').request

function sendLocalReq(service, port, path, method='GET', content={}) {
  const url = `http://${service}:${port}/${path}`
  const args = {
      method: method,
      headers: {'Content-Type': 'application/json'},
      content: JSON.stringify(content)
  }
  const res = request(url, args)
  return res.data
}

/* Set up infra */
fastify.post('/setup_infra', function (req, reply) {
  const ip = req.raw.connection.remoteAddress
  const data = sendLocalReq('infrastructure', '5000', 'setup', 'POST', {ip: ip})
  infraSetup = true
  reply
    .code(200)
    .header('Content-Type', 'application/json; charset=utf-8')
    .send(data)
})

/* Get infra status */
fastify.get('/status', function (req, reply) {
  const data = sendLocalReq('infrastructure', '5000', 'status')
  reply
    .code(200)
    .header('Content-Type', 'application/json; charset=utf-8')
    .send(data)
})

/* Get output of specific modules */
fastify.get('/outputs/modules/:params', function (req, reply) {
  const { params: { params } } = req
  fastify.log.info(`Params is ${params}`)
  const data = sendLocalReq('infrastructure', '5000', `outputs/modules/${params}`)
  reply
    .code(200)
    .header('Content-Type', 'application/json; charset=utf-8')
    .send(data)
})

fastify.post('/create_pipeline', function (req, reply) {
  const data = sendLocalReq('job_scheduler', '5001', 'create_pipeline', 'POST', req.body)
  reply
    .code(200)
    .header('Content-Type', 'application/json; charset=utf-8')
    .send({})
})

const start = async () => {
  try {
    await fastify.listen(8080, '0.0.0.0')
    fastify.log.info(`server listening on ${fastify.server.address().port}`)
  } catch (err) {
    fastify.log.error(err)
    process.exit(1)
  }
}
start()
