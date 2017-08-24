const Nightmare = require('nightmare')
const vo = require('vo')

vo(run)((err, result) => {
    if (err) throw err
})

function* run() {
  const nightmare = Nightmare({ show:true })
  let nextExists = true
  let testIsRunning = false

  yield nightmare
    .goto('http://127.0.0.1:5000/fec9e3fe73e6be021619071e30fc6ecb')

  nextExists = yield nightmare.visible('label');
  while (nextExists) {
      testIsRunning = true
      yield nightmare
          .click('label')
          .wait(501)
      nextExists = yield nightmare.visible('label')
  }
  if (testIsRunning) {
    nightmare.end()
      .then(console.log('Survey has been successfully completed'))
  } else {
    nightmare.end()
      .then(console.log('Survey has not been completed'))
  }
}