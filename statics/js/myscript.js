// document.getElementById("mode-text").innerHTML = "new text mf!!!"

// const toggle_button = '#toggle-button';

f = true

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

function getSecureCookie() {
    var dc = document.cookie;
    return dc.split(';')
}

function setCookie(cname, cvalue, exdays = 2) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    let expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/;NULL,0";
  }

  function toggle_clicked(toggle_button){
    let toggle = document.getElementById("toggle-button")
    if (toggle.checked){
        setCookie('isSecure', 'true')
        secure_design()
    } else {
        setCookie('isSecure', 'false')
        insecure_design()
    }
};

function update_toggle(){
    console.log(getCookie('isSecure'))
    if (getCookie('isSecure') == 'true'){
        document.getElementById("toggle-button").setAttribute("checked", "checked");
        secure_design()
    } else{
        document.getElementById("toggle-button").removeAttribute("checked");
        insecure_design()
    }
}


function secure_design(){
    document.getElementById('topnav').classList.remove("insecure")
    document.getElementById('topnav').classList.add("secure")
    document.getElementById('mode-text').innerHTML = "Mode: Secure";
}

function insecure_design(){
    document.getElementById('topnav').classList.remove("secure")
    document.getElementById('topnav').classList.add("insecure")
    document.getElementById('mode-text').innerHTML = "Mode: Insecure";
}

update_toggle();
