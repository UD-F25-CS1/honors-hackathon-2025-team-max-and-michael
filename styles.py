SITE_STYLES = """
* {
    box-sizing: border-box;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

body {
    background-color: #F7F7F7;
    margin: 0;
}

.form-step-container {
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

.form-step-center-box-container {
    width: 100%;
    display: flex;
    padding: 25px;
    align-items: center;
    justify-content: center;
}

.form-step-center-box {
    padding: 40px;
    color: white;
    background-color: #00539F;
    text-align: center;
}

.form-step-center-box br {
    margin-top: 10px;
}

.form-step-center-box * {
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
"""
