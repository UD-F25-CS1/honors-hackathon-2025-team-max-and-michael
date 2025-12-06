SITE_STYLES = """
* {
    box-sizing: border-box;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

body {
    background-color: #F7F7F7;
    margin: 0;
}

.page-container {
    width: 100%;
    text-align: center;
    background-color: #F7F7F7;
}

.form-step-top-bar {
    width: 100%;
    padding: 10px;
    background-color: #00539F;
    color: #FFCC00;
    font-weight: bold;
}

.page-center-box-container {
    width: 100%;
    display: flex;
    padding: 25px;
    align-items: center;
    justify-content: center;
}

.page-center-box {
    padding: 40px;
    color: white;
    background-color: #00539F;
    text-align: center;
}

.page-center-box span {
    margin-top: 10px;
}

.page-center-box * {
    display: block;
}

select {
    outline: none;
    border: none;
    padding: 10px;
    font-weight: bold;
    margin-top: 15px;
}

button {
    outline: none;
    border: none;
    padding: 10px;
    border-radius: 0;
    background-color: #FFCC00;
    color: #00539F;
    font-weight: bold;
    transition: 0.1s background-color ease-in-out;
    cursor: pointer;
}

button:hover {
    background-color: #DDAA00;
}

#form-next-button {
    margin-top: 10px;
    text-align: center;
}

textarea {
    margin-top: 15px;
}

h1 {
    margin-top: 0;
}

.schedule-container {
    width: 100%;
    display: flex;
}

.schedule-container div {
    flex: 1;
}

.period-block {
    padding: 3px;
}

.period-block-mwf {
    margin-bottom: 4.4px;
}

.period-block-tr {
    margin-bottom: 11px;
}

.center-box h1 {
    margin-top: 30px;
}

.schedule-switching-controls {
    margin-top: 25px;
}

#previous-button {
    margin-right: 10px;
}
"""
