var respStatus = null
var respOutput = null
var superserverIp = null

/* This variable will be automatically replaced by the replace_ip script */
var fastifyIp = "{fastifyIp}"

function setRespStatus(resp) {
    respStatus = resp
}

function setRespOutput(resp) {
    respOutput = resp
}

function sendRequest(uri, path, method='GET', content={}, callback=setRespStatus) {
    url = `http://${uri}:8080/${path}`
    console.log(`Sending request to: ${url}`)
    var req = new XMLHttpRequest()
    req.open(method, url, true)
    req.setRequestHeader('Content-type', 'application/json');
    //req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    req.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            callback(req.response)
        }
    }
    req.send(JSON.stringify(content))
}

sendRequest(fastifyIp, 'setup_infra', 'POST')

function getInfraStatus() {
    sendRequest(fastifyIp, 'status', 'GET', {}, setRespStatus)
    if (respStatus == null) {
        return null
    } else {
        parsed = JSON.parse(respStatus)
        return parsed.status
    }
}

function getSuperserverIp() {
    sendRequest(fastifyIp, 'outputs/modules/superserver', 'GET', {}, setRespOutput)
    if (respOutput == null) {
        return null
    } else {
        parsed = JSON.parse(respOutput)
        return parsed.output.public_ip
    }
}

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
}

const updateStatus = async() => {
    let st = ''
    while (st !== 'READY') {
        await sleep(1000).then(v => st = getInfraStatus())
        document.getElementById('infra_status').innerHTML = st
    }
}

const waitForIp = async() => {
    while (superserverIp == null) {
        await sleep(1000).then(v => superserverIp = getSuperserverIp())
    }
}

updateStatus().then(() => {
    waitForIp().then(() => {
        document.getElementById('submit').disabled = false
        document.getElementById('scheduling').disabled = false
        document.getElementById('lineage').disabled = false
        document.getElementById('loader').style.visibility = 'hidden'
    })
})

function createPipeline(configs) {
    sendRequest(
        fastifyIp,
        'create_pipeline',
        'POST',
        {"job_info": configs},
        function(dummy){}
    )
}

/* Assign text area to code mirror to highlight SQL syntaxis */
var editableCodeMirror = CodeMirror.fromTextArea(document.getElementById('transform-sql-area'), {
    mode: 'sql',
    indentWithTabs: true,
    lineNumbers: true,
    matchBrackets : true
})

document.getElementById('scheduling').onclick = function () {
    window.open(`http://${superserverIp}:8081`, '_blank')
}

document.getElementById('lineage').onclick = function () {
    window.open(`http://${superserverIp}:8080`, '_blank')
}

document.getElementById('submit').onclick = function () {
    /* Make the SQL query available to the textarea */
    editableCodeMirror.save()

    var jobName = document.getElementById('job-name').value

    var source1Table = document.getElementById('source1-table-name').value
    var source1Path = document.getElementById('source1-path').value
    var source2Table = document.getElementById('source2-table-name').value
    var source2Path = document.getElementById('source2-path').value
    var source3Table = document.getElementById('source3-table-name').value
    var source3Path = document.getElementById('source3-path').value

    var transformSqlQuery = document.getElementById('transform-sql-area').value
    var destTable = document.getElementById('dest-table-name').value

    var cronExpression = document.getElementById('cron-expression').value
    var sourceCount = 1

    if (source1Table === null || source1Path === null) {
        console.log('Error: source1 is mandatory')
        return
    }

    configs = {
        "job_name": jobName,
        "source1_table": source1Table,
        "source1_path": source1Path,
        "sql_query": transformSqlQuery,
        "destination_table": destTable,
        "cron_expr": cronExpression
    }
    if (source2Table.length > 0 && source2Path.length > 0) {
        configs["source2_table"] = source2Table
        configs["source2_path"] = source2Path
        sourceCount = 2
    }
    if (source3Table.length > 0 && source3Path.length > 0) {
        configs["source3_table"] = source3Table
        configs["source3_path"] = source3Path
        sourceCount = 3
    }
    configs["source_count"] = sourceCount

    createPipeline(configs)
}

