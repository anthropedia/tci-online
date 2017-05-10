casper.test.begin('Error page appear if token is wrong', 1,
        function suite(test) {
    casper.start("http://127.0.0.1:5000/wrongtoken", function() {
        test.assertTrue(casper.getPageContent().search('token is not ' +
            'valid or already used') != -1, 'The error page appear correctly')
    })

    casper.run(function() {
        test.done()
    })
})

casper.test.begin('Error page appear if token does not exist', 1,
        function suite(test) {
    casper.start("http://127.0.0.1:5000", function() {
        test.assertTrue(casper.getPageContent().search('token is not ' +
            'valid or already used') != -1, 'The error page appear correctly')
    })

    casper.run(function() {
        test.done()
    })
})

var childProcess
try {
    childProcess = require("child_process")
} catch (e) {
    this.log(e, "error")
}
if (childProcess) {
    childProcess.execFile("/bin/bash", ["test/ihm/script_token.py"], null, function (err, stdout, stderr) {
        this.log("execFileSTDOUT:", JSON.stringify(stdout), 'debug')
        this.log("execFileSTDERR:", JSON.stringify(stderr), 'debug')
    })
this.log("Done", "debug")
} else {
    this.log("Unable to require child process", "warning")
}

casper.test.begin('Survey is appearing correctly with a good token', 2,
        function suite(test) {
    casper.start("http://127.0.0.1:5000/" + casper.cli.get('token'),
            function() {
        test.assertElementCount('label', 5)
        test.assertElementCount('li', 5)
        casper.echo(casper.cli.get('token'))
    })

    casper.run(function() {
        test.done()
    })
})

// function to click button
casper.Clicker = function () {
    this.click('#answer-1')
    return true
}

//function to wait set time
casper.Waiter = function () {
    // adjust wait time between clicks
    this.wait(600)
    return true
}

casper.test.begin('Survey can be finished', 1, function suite(test) {
    casper.start("http://127.0.0.1:5000/" + casper.cli.get('token'),
            function() {
        for (var i = 0; i < 72; i++) {
            this.waitFor(function check() {
                return this.Clicker()
            })
            this.waitFor(function check() {
                return this.Waiter()
            })
        }
    })

    casper.then(function() {
        test.assertTrue(casper.getPageContent().search('You have completed' +
            ' this test.') != -1, 'The end page appear correctly')
    })

    casper.run(function() {
        test.done()
    })
})
