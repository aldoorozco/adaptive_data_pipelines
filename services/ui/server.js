const fastify = require('fastify')({ logger: true })
const path = require('path')

/* fastify.register(require('fastify-http-client')) */

fastify.register(require('fastify-static'), {
  root: path.join(__dirname, 'resources'),
  prefix: '/resources/',
})

/* Dispatch web page */
fastify.get('/', function (req, reply) {
  reply.sendFile('index.html')
})

var request = require('urllib-sync').request

function sendLocalReq(port, path, method, data) {
  var res = request(
      `http://localhost:${port}/${path}`, {
          method: method,
          data: data
      }
  )
  console.out(res.data)
}

/* Get infra status */
fastify.get('/status', function (req, reply) {
  data = sendLocalReq('5000', 'status', 'GET', {})
  reply
    .code(200)
    .header('Content-Type', 'application/json; charset=utf-8')
    .send(data)
})

/* Get output of specific modules */
fastify.get('/outputs/modules/:params', function (req, reply) {
  data = sendLocalReq('5000', `outputs/modules/${req.params}`, 'GET', {})
  reply
    .code(200)
    .header('Content-Type', 'application/json; charset=utf-8')
    .send(data)
})

fastify.post('/create_pipeline', function (req, reply) {
  data = sendLocalReq('5001', 'create_pipeline', 'POST', req.body)
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
